from habitica_api import Habitica
from auth import apikey, uid
from time import sleep
from sys import argv
from datetime import datetime, timedelta

TASK_NAMES = (argv[1], "break")
LENGTHS = (60 * 20, 60 * 10)


api = Habitica(uid, apikey)


def get_time_after(sec):
    """ get datetime object sec seconds latter, rounded to nearest minute"""
    now = datetime.today()
    ns = now.second
    sec += 60 - ns if ns >= 30 else -ns
    til = now + timedelta(seconds=sec)
    return til


def sleep_till(dt):
    """ sleep until the current time is greater than dt, checks every second"""
    while True:
        now = datetime.today()
        if now > dt:
            break
        sleep(.5)


for _ in range(4):
    for title, length in zip(TASK_NAMES, LENGTHS):
        til = get_time_after(length)
        api.add_todo("{} till {:02d}:{:02d}".format(title, til.hour, til.minute))
        sleep_till(til)
