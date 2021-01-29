import json
import logging
import traceback

import websockets

log = logging.getLogger("WEBSOCKET_HELPER")


def log_app_error(e: BaseException, level=logging.ERROR) -> None:
    e_traceback = traceback.format_exception(e.__class__, e, e.__traceback__)
    traceback_lines = []
    for line in [line.rstrip('\n') for line in e_traceback]:
        traceback_lines.extend(line.splitlines())
    log.log(level, traceback_lines.__str__())


async def websocket_connect(uri, payload, consumer):
    websocket = await websockets.connect(uri, ssl=True)
    if payload:
        await websocket.send(json.dumps(payload))
    while True:
        if not websocket.open:
            try:
                log.info('Websocket is NOT connected. Reconnecting...')
                websocket = await websockets.connect(uri, ssl=True)
                await websocket.send(payload)
            except Exception as e:
                log_app_error(e)
                log.info('Unable to reconnect, trying again.')
        try:
            async for message in websocket:
                if message is not None:
                    try:
                        await consumer(message)
                    except Exception as e:
                        log_app_error(e)
                        continue
        except Exception as e:
            log_app_error(e)
            log.info('Error receiving message from websocket.')
