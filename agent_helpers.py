import logging

log = logging.getLogger("AGENT_HELPERS")


def message_filter(message_type, param_name):
    def wrapper(func, *args, **kwargs):
        async def wrapped(*args, **kwargs):
            try:
                message = kwargs[param_name]
                if type(message) == message_type:
                    return await func(*args, **kwargs)
            except Exception as e:
                log.exception(e)

        return wrapped

    return wrapper
