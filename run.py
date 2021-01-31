import asyncio
import datetime
import json
import os
import pickle

import aioredis
import click
from importlib.machinery import SourceFileLoader

from aioredis import Redis
import logging
from rlog import RedisHandler

import pymongo

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("RAKUN-MAS")

DEBUG = False


class AgentWrapper:

    async def display(self, msg):
        try:
            await self.display_pub(self._agent_, msg)
        except Exception as e:
            log.exception(e)

    def __init__(self, id, agent, publish, db, exit, display_pub):
        self.display_pub = display_pub
        self.id = id
        self.publish = publish
        self.exit = exit

        self.storage = db
        self._agent_ = agent
        self._agent_.storage = self.storage
        self._agent_.exit = self.exit
        self._agent_.publish = self.publish
        self._agent_.display = self.display

    async def start_agent(self):
        if self._agent_.start:
            try:
                await self._agent_.start()
            except Exception as e:
                log.exception(e)

    async def stop_agent(self):
        if self._agent_.stop:
            try:
                log.info(f"AGENT CLOSE REQUEST {self.id}")
                await self._agent_.stop()
            except Exception as e:
                log.exception(e)

    async def execute_agent(self):
        if self._agent_.execute:
            try:
                await self._agent_.execute()
            except Exception as e:
                log.exception(e)

    async def accept_message(self, channel, message):
        try:
            await self._agent_.accept_message(agent=channel, message=message)
        except Exception as e:
            log.exception(e)


class PubSub:

    def __init__(self, pub: Redis = None, sub: Redis = None, channel: aioredis.Channel = None,
                 display_publisher=None, display_channel_name=None) -> None:
        self.display_channel_name = display_channel_name
        self.channel = channel
        self.display_publisher = display_publisher
        self.pub = pub
        self.sub = sub

    async def display(self, agent, message):
        agent = agent.__class__.__name__ if type(agent) != str else agent
        data = {
            "agent": agent,
            "message": message
        }
        await self.display_publisher.publish(f"{self.display_channel_name}", json.dumps(data))

    async def publish(self, agent, message):
        channel_name = agent.__name__ if type(agent) != str else agent
        if DEBUG:
            log.info(f"Outgoing Message received:{datetime.datetime.now()}")
            log.info(f"Outgoing Message To Channel:{channel_name}")
            log.info(f"Outgoing Message Data:{message}")
        data = {
            "channel": self.channel.name.decode("utf8"),
            "message": message
        }
        await self.pub.publish(f"{channel_name}", pickle.dumps(data))

    async def subscribe(self, receiver):
        while await self.channel.wait_message():
            msg = await self.channel.get()
            data = pickle.loads(msg)
            sender_channel = data['channel']
            sender_message = data['message']
            if DEBUG:
                log.info(f"Incoming Message received:{datetime.datetime.now()}")
                log.info(f"Incoming Message Sender:{sender_channel},Reciver :{self.channel.name}")
                log.info(f"Incoming Message Data:{sender_message}")
            await receiver(sender_channel, sender_message)


@click.command()
@click.option('--stack-name', help='Agent Stack Name')
@click.option('--comm-url', help='Rakun Stack Communication URL')
@click.option('--id', help='Agent ID')
@click.option('--name', help='Agent Name')
@click.option('--source', help='Agent Source')
@click.option("--init-params", multiple=True, default=[("name", "agent_init")], type=click.Tuple([str, str]))
def run(stack_name, comm_url, id, name, source, init_params):
    PLATFORM_CH_NAME = f"{stack_name}_PLATFORM"
    PLATFORM_DISPLAY_CH_NAME = f"{stack_name}_PLATFORM_DISPLAY"
    PLATFORM_CTRL_CH_NAME = f"{stack_name}_PLATFORM_CTRL"

    START_COMMAND = f"{id}:START"
    EXIT_COMMAND = f"{id}:EXIT"

    log.addHandler(
        RedisHandler(channel=f'{stack_name}_PLATFORM_LOG', host=comm_url.split(":")[0],
                     port=int(comm_url.split(":")[1])))
    log.info("Initiate")

    log.info(f"Agent Stack Name {stack_name}")
    log.info(f"Communication URL {comm_url}")
    log.info(f"Agent ID {id}")
    log.info(f"Agent Name {name}")
    log.info(f"Agent Source {source}")

    agent_source_code = SourceFileLoader("", f"{os.getcwd()}/{source}").load_module()
    agent_class = getattr(agent_source_code, name)
    agent_obj = agent_class(init_params=init_params)

    channel_name = agent_class.__name__

    async def start_app():
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client[stack_name.lower()]
        log.info(f"DB Name {db}")
        # for c in db.list_collection_names():
        #     db[c].drop()
        pub = await aioredis.create_redis(f'redis://{comm_url}')
        sub = await aioredis.create_redis(f'redis://{comm_url}')
        sub_agent = await aioredis.create_redis(f'redis://{comm_url}')
        display_pub_agent = await aioredis.create_redis(f'redis://{comm_url}')
        #
        platform_ch_res = await sub.subscribe(PLATFORM_CH_NAME)
        platform_ch: aioredis.Channel = platform_ch_res[0]

        res = await sub_agent.subscribe(f'{channel_name}')
        ch1: aioredis.Channel = res[0]

        async def exit():
            await pub.publish(PLATFORM_CTRL_CH_NAME, f"EXIT:{id}")

        pub_sub = PubSub(pub=pub, sub=sub, channel=ch1, display_publisher=display_pub_agent,
                         display_channel_name=PLATFORM_DISPLAY_CH_NAME)

        agent = AgentWrapper(id=id, agent=agent_obj,
                             publish=pub_sub.publish, db=db, exit=exit, display_pub=pub_sub.display)

        async def accept_platform_command():
            while await platform_ch.wait_message():
                msg = await platform_ch.get(encoding="utf8")
                msg = str(msg)
                if str(msg) == EXIT_COMMAND:
                    try:
                        # sub.unsubscribe(channel=ch1)
                        # sub_agent.unsubscribe(channel=platform_ch)
                        await agent.stop_agent()
                        # for task in asyncio.Task.all_tasks(loop=asyncio.get_event_loop()):
                        #     # cancel all tasks other than this signal_handler
                        #     if task is not asyncio.Task.current_task():
                        #         task.cancel()
                    except Exception as e:
                        log.exception(e)

        async def start_agent():
            await agent.start_agent()
            tasks = [pub_sub.subscribe(agent.accept_message), agent.execute_agent(), accept_platform_command()]
            tsk = asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
            await tsk
            await agent.stop_agent()

        await pub.publish(PLATFORM_CTRL_CH_NAME, f"INIT:{id}")
        # Platform handling commands
        while await platform_ch.wait_message():
            msg = await platform_ch.get(encoding="utf8")
            msg = str(msg)
            log.info(f"PLATFORM COMMAND REQUEST {msg=}")
            if str(msg) == START_COMMAND:
                agent_start_task = asyncio.wait([start_agent()],
                                                return_when=asyncio.ALL_COMPLETED)
                await agent_start_task

        sub.close()
        pub.close()

    asyncio.run(start_app())


if __name__ == '__main__':
    run()
