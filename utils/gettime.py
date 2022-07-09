import datetime
from pytz import timezone


def get_time():
    return datetime.datetime.now(timezone("Asia/Seoul"))
