from gcsa.google_calendar import GoogleCalendar
import datetime
import os

Gcalanderid = os.getenv("calanderid")
GeventID = os.getenv("eventid")

async def getdates(num :int) -> list:
    calander = GoogleCalendar(default_calendar=Gcalanderid,credentials_path="./data/credentials.json")
    events = list(calander.get_instances(GeventID)) 
    eventlist= []
    for e in events[:num]:
            time = e.start
            t_in_seconds = int(datetime.datetime.fromisoformat(str(time)).timestamp())
            eventlist.append(f"<t:{t_in_seconds}:F> <t:{t_in_seconds}:R>")
    return(eventlist)