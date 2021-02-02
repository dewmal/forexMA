from datetime import datetime


def log_time(logger, log_off=False):
    def wrapper(func, *args, **kwargs):
        async def wrapped(*args, **kwargs):
            if not log_off:
                start_time = datetime.now()
                res = await func(*args, **kwargs)
                time_elapsed = datetime.now() - start_time
                logger.info('Time elapsed {}'.format(time_elapsed))
            else:
                res = await func(*args, **kwargs)
            return res

        return wrapped

    return wrapper
