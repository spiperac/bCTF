import time
from datetime import timedelta

START_TIME = time.time()
# ...
def GET_UPTIME():
    """
    Returns the number of seconds since the program started.
    """
    # do return startTime if you just want the process start time
    time_passed = time.time() - START_TIME
    print(time_passed)
    uptime = timedelta(seconds=round(time_passed))
    return uptime