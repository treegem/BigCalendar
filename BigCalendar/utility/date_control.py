import datetime


def date_to_unixtime(year, month, day):
    date = datetime.datetime(year=year, month=month, day=day)
    return date.timestamp()
