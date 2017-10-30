
# TODO
# produce weekly monthly report
# show weekly breakdown
# show daily breakdown
# show task breakdown
# show time of the day breakdown
# show accumative breakdown

from datetime import datetime as dt, timedelta


class Time_stat:

    def __init__(self, logfile):
        self.logfile = logfile

    def _getlogs(self):
        """ return an generator that yeilds all log objects in logfile"""
        with open(self.logfile, "r") as f:
            for l in f:
                if not l or l == "\n":
                    continue
                lsp = l.split("\t")
                yield {"time": dt.strptime(lsp[0], "%x %X"),
                       "name": lsp[1],
                       "length": int(lsp[2])}

    def printall(self):
        for itm in self._getlogs():
            print(itm)

    def get_weekly_total(self):
        td = dt.today().replace(hour=0, minute=0, second=0, microsecond=0)
        start = td - timedelta(days=td.weekday())
        end = td + timedelta(days=6 - td.weekday())
        return self.get_total(start, end)

    def get_total(self, start, end):
        """ return a dict with the (task, task total) key value pair"""
        rlt = {"total": 0}
        for log in self._getlogs():
            if log['time'] > start and log['time'] < end:
                if log['name'] in rlt:
                    rlt[log['name']] += log['length']
                else:
                    rlt[log['name']] = log['length']
                rlt["total"] += log['length']
        return rlt

    @staticmethod
    def _to_percentage(total_dict):
        total = total_dict["total"]
        if not total:
            return {"total": 100.0}
        rlt = {}
        for k in total_dict:
            rlt[k] = total_dict[k] / total * 100
        return rlt

weekly_total = Time_stat("timeslot.log").get_weekly_total()
weekly_percentage = Time_stat._to_percentage(weekly_total)
YELLOW = "\33[93m"
CLEAR = "\33[0m"
for k in weekly_percentage:
    print(f"{YELLOW}{k:>8}{CLEAR}:\t{weekly_total[k]/60}\t{weekly_percentage[k]:.2f}")

