#!/usr/bin/python2

"""vacation.py

$Id: vacation.py,v 1.3 2007/02/22 04:50:07 msoulier Exp msoulier $

This program is a simple auto-responder for email. It works with any email
system that can pipe incoming email to a program, without expecting said
program to perform mail delivery. It has so far been tested with qmail
dotfiles and with procmail.

To use it, set up a $HOME/vacation.msg file with the auto-response that you
want to send. The program will populate $HOME/vacation.cache with email
addresses that it has seen, to ensure that it only responds to each sender
once. It also populates $HOME/vacation.log with a log of its work. It will try
not to respond to mailing lists (ie. anything with bulk or junk precedence),
and will not respond unless your address is in the To field. Change the ME
variable below to your address.

Todo List:
    - Command line options
        - receiver email address
        - logging levels

    Ask me there's a feature that you'd like. The worst that I can do is say
    no. Or, implement it and send me a patch.

Copyright (C) 2006 Michael P. Soulier

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import rfc822
import sys, os
import re
import smtplib
import time
from fcntl import *

CACHE = os.environ['HOME'] + '/vacationpy.cache'
LOG = os.environ['HOME'] + '/vacationpy.log'
RESPONSE = os.environ['HOME'] + '/vacationpy.msg'
ME = 'michael_soulier@mitel.com'
SMTPHOST = 'localhost'

def main():
    msg = rfc822.Message(sys.stdin)
    cachefile = open(CACHE, "a+")
    flock(cachefile, LOCK_EX)
    logfile = open(LOG, "a")
    sys.stdout = logfile
    sys.stderr = logfile
    print "\n"

    for header in msg.headers:
        print header,

    fromaddr = msg.getheader('From').lower()
    print "Message from", fromaddr
    fromname, fromaddr = rfc822.parseaddr(fromaddr)
    print "Just the address is", fromaddr

    if not incache(fromaddr, cachefile):
        send_auto_answer(fromaddr, msg, cachefile)

    flock(cachefile, LOCK_UN)
    cachefile.close()
    logfile.close()
    sys.exit(0)

def incache(faddr, cfile):
    cfile.seek(0)
    for addr in cfile.readlines():
        addr = addr.strip()
        faddr = faddr.strip()
        if faddr == addr:
            print "found address in cache"
            return 1
    print "did not find address in cache"
    return 0

def send_auto_answer(faddr, msg, cfile):
    print "going to send auto_reply to", faddr
    # Don't send it to mailing lists
    precedence = msg.getheader('Precedence')
    print "precedence is %s" % precedence
    if precedence and re.search('list|bulk|junk', precedence, re.I):
        print "Mailing list, not sending response."
        return
    # Only send if I'm in the To field
    toaddr = msg.getheader('To')
    print "To addresses are: %s" % toaddr
    if toaddr:
        if not re.search(ME, toaddr, re.I):
            print "I'm not in the To field. Not sending response."
            return

    cfile.seek(0, 2)
    cfile.write(faddr + "\n")

    subject = msg.getheader('Subject')
    if not subject: subject = 'no subject'

    response = open(RESPONSE, "r").read()
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    message = '''\
To: %(to)s
From: %(from)s
Subject: Vacation Alert (re: %(subject)s)
Date: %(date)s

%(body)s''' % {
                'to':       faddr,
                'from':     ME,
                'subject':  subject,
                'date':     date,
                'body':     response
              }

    print "About to send this:"
    print message

    server = smtplib.SMTP(SMTPHOST)
    server.set_debuglevel(1)
    server.sendmail(ME, faddr, message)
    server.quit()

if __name__ == '__main__':
    main()

"""
$Log: vacation.py,v $
Revision 1.3  2007/02/22 04:50:07  msoulier
Added support for Date header.

Revision 1.2  2006/01/03 03:04:37  msoulier
Added RCS tags and GPL.

"""
