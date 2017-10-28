#!/usr/bin/env python3

"""
 TODO: print inline
# allow 1 minute for user to switch task
# insert delemeter entry when starting and ending session
# cmd/web interface
# delect current task when user press CTRL-C
# print count down
# print slip
    variable to enable/disable log
"""

from sys import argv
from datetime import datetime, timedelta
from os.path import realpath, dirname, join

from time import strftime, sleep

from habitica_api import Habitica
from auth import apikey, uid


TASK_NAMES = (argv[1], "break")
LENGTHS = (60 * 20, 60 * 10)
LOG_FILE = join(realpath(dirname(argv[0])), "timeslot.log")
print(LOG_FILE)


API = Habitica(uid, apikey)


def get_time_after(sec):
    """ get datetime object sec seconds latter, rounded to nearest minute"""
    now = datetime.today()
    ns = now.second
    sec += (60 - ns) if ns >= 30 else -ns
    til = now + timedelta(seconds=sec)
    return til


def sleep_till(dt):
    """ sleep until the current time is greater than dt,
        checks every .5 second"""
    while True:
        now = datetime.today()
        if now > dt:
            break
        sleep(.5)


def logtofile(task, length, file=LOG_FILE):
    '''write a log to the file specified'''
    with open(file, "a") as f:
        txt = "{}\t{}\t{}\n".format(strftime("%x %X"), task, length)
        f.write(txt)


def wait_checkoff(tid):
    """ wait till user check off todo, return False when task not found"""
    while True:
        tskobj = API.get_task(tid)
        if not tskobj["success"]:
            if tskobj["error"] == "NotFound":
                return False
            raise NotImplementedError("error: {}".format(tskobj))

        if tskobj["data"]["completed"]:
            return True
        sleep(5)

def run():
    '''main funtion'''
    for _ in range(4):
        for title, length in zip(TASK_NAMES, LENGTHS):
            til = get_time_after(length)
            txt = "{} till {:02d}:{:02d}".format(title, til.hour, til.minute)
            print(txt)
            tid = API.add_todo(txt)["data"]["id"]
            sleep_till(til)
            if not wait_checkoff(tid):
                # taks deleted by user
                print("task deleted by user, exiting.")
                exit(0)
            # insert slip entry if > 1 min
            logtofile(title, length)
            slip = (datetime.today() - til).seconds
            if slip > 60:
                logtofile("_slip", slip)
                print(f"slip {int(slip/60)} mins")

if __name__ == "__main__":
    run()
