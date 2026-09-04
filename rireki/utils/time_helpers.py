from time import time

testing_now = None
DAY_SECONDS = 24 * 60 * 60
YEAR_SECONDS = 365 * DAY_SECONDS


def now():
    return testing_now or int(time())


def set_testing_now(time):
    global testing_now

    testing_now = time
