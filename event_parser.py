from re import compile as rcompile
from datetime import datetime as dt
from datetime import timedelta
from time import time


RE_TITLE = rcompile(r"SUMMARY:(\w+\s\w+)")
RE_TIME = rcompile(r"DATE-TIME:(\d{8}T\d{6})")
TIMEFORMAT = "%Y%m%dT%H%M%S"
TIME_TABLE_ICS="timetable.ics"

class _Event:
    def __init__(self, name, start, end, week=None):
        self.name = name
        self.start = start
        self.end = end
        self.week = week


def _parse_icstime(t):
    return dt.strptime(RE_TIME.search(t).group(1), TIMEFORMAT)

# def _week_of_semaster:





def _all_events(f=TIME_TABLE_ICS):
    with open(f, "r") as f:
        done = False
        while not done:
            line = f.readline()
            if line == "BEGIN:VEVENT\n":
                titleline = f.readline()
                startline = f.readline()
                endline = f.readline()

                title = RE_TITLE.search(titleline).group(1)
                start = _parse_icstime(startline)
                end = _parse_icstime(endline)
                yield _Event(title, start, end)

            elif not line:
                done = True

def next_event(time_offset):
    cutoff = dt.now() + time_offset
    future = filter(lambda e: e.end > cutoff, _all_events())
    return min(future, key=lambda e: e.end)


def events_today():
    return events_on_date(dt.now())

def events_on_date(date):
    return (e for e in _all_events() if e.end.day == date.day)


#ofs = timedelta(hours=5)
#print(next_event(ofs).start)

#for e in events_today():
    #print(e.name)
#for e in _all_events():
#    print(e.start)
#print(list(_all_events())[-2].start)

