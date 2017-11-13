#!/usr/bin/env python3

"""
 TODO
# insert delemeter entry when starting and ending session
# cmd/web interface
# variable to enable/disable log
# show recent tasks
# write to database

"""

from sys import argv
from datetime import datetime, timedelta
from os.path import realpath, dirname, join
from signal import signal, SIGINT
from urllib.request import urlopen
from subprocess import check_output

from time import strftime, sleep
import sys

from habitica_api import Habitica
from auth import apikey, uid

if len(argv) == 1:
    argv.append(input("enter your task below\n"))

TASK_NAMES = (argv[1], "break")
LENGTHS = (20, 5)
LENGTHS = [60 * itm for itm in LENGTHS]
LOG_FILE = join(realpath(dirname(argv[0])), "timeslot.log")
print(LOG_FILE)

NOTIFY_URL = "http://192.168.1.4:5001/"

COLOR = {"green": "\033[92m",
         "cyan": "\033[96m",
         "clear": "\033[0m"
         }

def exit_and_delete(signal, frame):
    if last_task_id:
        print("\ndeleting last task")
        API.delete_task(last_task_id)
    urlopen(NOTIFY_URL + "f")
    print("exiting")
    sys.exit(0)


API = Habitica(uid, apikey)

last_task_id = None

def printi(s):
    '''print string inline'''
    print(s, end='\r')


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
        printi(f"{COLOR['green']}{(dt - now).total_seconds() / 60:.2f} mins remaining.{COLOR['clear']}")
        if now > dt:
            column = check_output(("stty", "size")).split()[1]
            printi(" " * int(column))
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
    signal(SIGINT, exit_and_delete)
    for _ in range(4):
        for title, length in zip(TASK_NAMES, LENGTHS):
            til = get_time_after(length)
            txt = "{}{}{} till {:02d}:{:02d}".format(COLOR['cyan'],
                                                      title,
                                                      COLOR['clear'],
                                                      til.hour,
                                                      til.minute)
            todo = "{} till {:02d}:{:02d}".format(title,
                                                  til.hour,
                                                  til.minute)
            print(txt)
            global last_task_id
            last_task_id = API.add_todo(todo)["data"]["id"]
            sleep_till(til)
            urlopen(NOTIFY_URL + "o")
            if not wait_checkoff(last_task_id):
                # taks deleted by user
                print("task deleted by user, exiting.")
                urlopen(NOTIFY_URL + "f")
                exit(0)
            urlopen(NOTIFY_URL + "f")
            # insert slip entry if > 1 min
            logtofile(title, length)
            slip = (datetime.today() - til).seconds
            if slip > 60:
                logtofile("_slip", slip)
                print(f"slip {int(slip/60)} mins")

if __name__ == "__main__":
    run()
