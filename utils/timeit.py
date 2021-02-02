from datetime import datetime


def log_time(logger):
    def wrapper(func, *args, **kwargs):
        async def wrapped(*args, **kwargs):
            start_time = datetime.now()
            res = await func(*args, **kwargs)
            time_elapsed = datetime.now() - start_time
            logger.info('Time elapsed {}'.format(time_elapsed))
            return res
        return wrapped
    return wrapper