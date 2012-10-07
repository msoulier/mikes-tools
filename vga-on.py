#!/usr/bin/python

"""This utility is for turning off the LCD on my netbook and turning a
connected external monitor at 1024x768 resolution. I use this for
presentations. I've found that I can't have both on, on my ASUS EEEPc.

I did this as a Python script because it was simpler to do an alarm handler to
implement the 30 second timeout if I don't see anything. I could do it in
shell though if I really wanted to."""

import signal, os

timeout = 30

def alarm_handler(signum, frame):
    pass

def go_projector():
    print "Disabling LCD..."
    os.system('xrandr --output LVDS1 --off')
    print "Setting display to VGA1 at 1024x768"
    os.system('xrandr --output VGA1 --mode "1024x768"')

def go_local():
    print "Going to local LCD"
    os.system('xrandr --auto')
    os.system('xrandr --output VGA1 --off')
    os.system('xrandr --output LVDS1 --mode "1024x600"')

def wait_timeout():
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)
    try:
        msg = "Press <Enter> to keep this setting - timeout in %d seconds" \
            % timeout
        resp = raw_input(msg)
        signal.alarm(0)
    except EOFError:
        print "\nTimeout waiting for input."
        go_local()
    else:
        print "Keeping display setting"

def main():
    go_projector()
    wait_timeout()

if __name__ == '__main__':
    main()
