from datetime import datetime, timedelta


def timestamp_format(timestamp: int, timezone: bool = False):
    delta = datetime.fromtimestamp(timestamp / 1000)
    if timezone:
        return delta - timedelta(hours=3)
    else:
        return delta
