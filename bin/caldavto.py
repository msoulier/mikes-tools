#!/home/msoulier/.pyenv/versions/3.12.11/envs/caldav/bin/python

import caldav
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import os
from typing import Dict

#########################################################################
# Office 365
url = "http://localhost:1080/users/michael.soulier@mitel.com/calendar/"
username = "michael.soulier@mitel.com"
password = os.environ.get("MITELPASS", "")
assert( password != "" )
#########################################################################

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
output_format = "org"

def fill_event(component, calendar) -> Dict[str, str]:
    cur = {}
    cur["calendar"] = f"{calendar}"
    cur["summary"] = component.get("summary")
    cur["description"] = component.get("description")
    cur["start"] = component.start
    endDate = component.get("dtend")
    if endDate and endDate.dt:
        cur["end"] = endDate.dt.strftime("%m/%d/%Y %H:%M")
    cur["datestamp"] = component.get("dtstamp").dt.strftime("%m/%d/%Y %H:%M")
    return cur

def main():
    mytz = ZoneInfo('America/Montreal')
    with caldav.DAVClient(url=url,
                          username=username,
                          password=password) as client:
        my_principal = client.principal()
        calendars = my_principal.calendars()
        for cal in calendars:
            now = datetime.now()
            one_month = timedelta(days=28)
            one_month_from_now = now + one_month
            fetched_events = cal.search(
                start=now,
                end=one_month_from_now,
                event=True,
                expand=True)
            events = []
            for event in fetched_events:
                for component in event.icalendar_instance.walk():
                    if component.name != "VEVENT":
                        continue
                    events.append(fill_event(component, cal))

            for event in events:
                start = event["start"]
                try:
                    start = start.astimezone(mytz)
                    #start = start.replace(tzinfo=mytz)
                except:
                    start = datetime.combine(start.today(), datetime.min.time())
                    start = start.astimezone(mytz)
                    #start = start.replace(tzinfo=mytz)
                if output_format == "remind":
                    print("REM %s AT %s MSG %%\"%s%%\", %%b, %%2" %
                        (start.strftime("%b %d"), start.strftime("%H:%M"), event["summary"]))
                elif output_format == "org":
                    print("* %s <%s>" % (
                        event["summary"],
                        start.strftime("%Y-%m-%d %H:%M")))
                    print("#+PROPERTY: calendar=%s" % cal.name)
                    
                else:
                    raise AssertionError("unsupported format")

main()
