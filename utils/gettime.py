import datetime
from pytz import timezone


def get_time() -> datetime.datetime:
    return datetime.datetime.now(timezone("Asia/Seoul"))
