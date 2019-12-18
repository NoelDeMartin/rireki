from time import time

testing_now = None


def now():
    global testing_now

    return testing_now or int(time())


def set_testing_now(time):
    global testing_now

    testing_now = time
