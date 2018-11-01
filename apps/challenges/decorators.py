import time
from config.config import read_config

def ctf_ended(function):
    def wrap(request, *args, **kwargs):
        cfg = read_config()
        print(time.time())
        if cfg.ctf.start_time or cfg.ctf.end_time == None:
            return False
        elif time.time() > cfg.ctf.end_time:
            return True
        else:
            return False

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap