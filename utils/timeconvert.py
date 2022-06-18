import time
import datetime


def datetime_to_unix(n: datetime.datetime):
    return int(time.mktime(n.timetuple()))
