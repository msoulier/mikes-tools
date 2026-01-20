#!/usr/bin/python3

import caldav
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import os
from typing import Dict
import argparse
import logging

logging.basicConfig()
log = logging.getLogger('caldavto')
log.setLevel(logging.INFO)

#########################################################################
# Office 365
url = "http://localhost:1080/users/michael.soulier@mitel.com/calendar/"
username = "michael.soulier@mitel.com"
password = os.environ.get("MITELPASS", "")
assert( password != "" )
#########################################################################

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

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

def parse_options():
    parser = argparse.ArgumentParser(description="Pull calendar from offlice365")
    parser.add_argument('-f',
                        '--format',
                        dest='format',
                        action='store',
                        default='org',
                        help='Format to output in [org|remind] (org)')
    parser.add_argument('-d',
                        '--debug',
                        dest='debug',
                        action='store_true',
                        default=False,
                        help='Verbose logging output')
    options = parser.parse_args()

    if options.format != "org" and options.format != "remind":
        sys.stderr.write("Unsupported format: %s\n" % options.format)
        parser.print_help()
        sys.exit(1)

    if options.debug:
        log.setLevel(logging.DEBUG)

    return options

def main():
    options = parse_options()

    log.debug("connecting as user %s to url %s", username, url)
    mytz = ZoneInfo('America/Montreal')
    with caldav.DAVClient(url=url,
                          username=username,
                          password=password) as client:
        my_principal = client.principal()
        calendars = my_principal.calendars()
        for cal in calendars:
            log.debug("looping on calendar %s", cal)
            now = datetime.now()
            one_month = timedelta(days=28)
            one_month_from_now = now + one_month
            log.debug("fetching events out one month")
            fetched_events = cal.search(
                start=now,
                end=one_month_from_now,
                event=True,
                expand=True)
            events = []
            log.debug("filtering results")
            for event in fetched_events:
                for component in event.icalendar_instance.walk():
                    if component.name != "VEVENT":
                        continue
                    events.append(fill_event(component, cal))

            for event in events:
                log.debug("looping on event %s", event)
                start = event["start"]
                try:
                    start = start.astimezone(mytz)
                except:
                    start = datetime.combine(start.today(), datetime.min.time())
                    start = start.astimezone(mytz)
                if options.format == "remind":
                    print("REM %s AT %s MSG %%\"%s%%\", %%b, %%2" %
                        (start.strftime("%b %d"), start.strftime("%H:%M"), event["summary"]))
                elif options.format == "org":
                    print("* %s <%s>" % (
                        event["summary"],
                        start.strftime("%Y-%m-%d %H:%M")))
                    print("#+PROPERTY: calendar=%s" % cal.name)
                    
                else:
                    raise AssertionError("unsupported format")

main()
