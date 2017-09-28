from event_parser import events_today
from habitica_api import Habitica
from auth import apikey,tagid , uid

api = Habitica(uid, apikey)

for e in events_today():
    api.add_todo(e.name, [tagid])

