from habitica_api import Habitica
from auth import apikey, uid
from time import sleep
from sys import argv
from datetime import datetime, timedelta
from os.path import expanduser

from time import strftime
log = True

TASK_NAMES = (argv[1], "break")
LENGTHS = (60 * 20, 60 * 10)
LOG_FILE = expanduser("~/wk/habitica_task_gen/timeslot.log")


api = Habitica(uid, apikey)


def get_time_after(sec):
    """ get datetime object sec seconds latter, rounded to nearest minute"""
    now = datetime.today()
    ns = now.second
    sec += (60 - ns) if ns >= 30 else -ns
    til = now + timedelta(seconds=sec)
    return til


def sleep_till(dt):
    """ sleep until the current time is greater than dt, checks every .5 second"""
    while True:
        now = datetime.today()
        if now > dt:
            break
        sleep(.5)

def logtofile(task, length, f=LOG_FILE):
    with open(f, "a") as f:
        txt = "{}\t{}\t{}\n".format(strftime("%x %X"), task, length)
        f.write(txt)




for _ in range(4):
    for title, length in zip(TASK_NAMES, LENGTHS):
        til = get_time_after(length)
        txt = "{} till {:02d}:{:02d}".format(title, til.hour, til.minute)
        logtofile(title, length)
        print(txt)
        api.add_todo(txt)
        sleep_till(til)
