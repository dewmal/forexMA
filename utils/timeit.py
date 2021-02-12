import traceback
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


def error_log(logger):
    def wrapper(func, *args, **kwargs):
        async def wrapped(*args, **kwargs):
            try:
                await func(*args, **kwargs)
            except Exception as ex:
                ex_traceback = ex.__traceback__
                tb_lines = [line.rstrip('\n') for line in
                            traceback.format_exception(ex.__class__, ex, ex_traceback)]
                logger.info(tb_lines)

        return wrapped

    return wrapper
