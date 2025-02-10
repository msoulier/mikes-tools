#!/usr/bin/python

import sys, os
from smtplib import SMTP
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from optparse import OptionParser

server = 'localhost'

# TODO
# https://pymotw.com/2/smtplib/
# - authentication and encryption
# - command line args for from, to, server

def send_email(email, options):
    to_addrs = options.to_addr.split(',')
    from_addr = options.from_addr
    if options.attachment:
        msg = MIMEMultipart()
        msg.attach(MIMEText(email))
        for path in options.attachment.split(','):
            with open(path, "r") as attachfile:
                part = MIMEApplication(attachfile.read(),
                                    Name=os.path.basename(path))
                part['Content-Disposition'] = 'attachment; filename="%s"' \
                    % os.path.basename(path)
                msg.attach(part)
    else:
        msg = MIMEText(email)
    msg['To'] = ', '.join(to_addrs)
    msg['From'] = from_addr
    msg['Subject'] = options.subject

    s = SMTP()
    #s.set_debuglevel(1)
    s.connect(server)
    #s.login('msoulier','MYPASSWORD')
    try:
        s.sendmail(from_addr, to_addrs, msg.as_string())
    finally:
        s.quit()

def main():
    usage = '%s [options]' % sys.argv[0]
    parser = OptionParser(usage=usage)
    parser.add_option('-a',
                      '--attachment',
                      action='store',
                      dest='attachment',
                      help='file MIME attachments, comma-separated',
                      default=None)
    parser.add_option('-f',
                      '--file',
                      action='store',
                      dest='file',
                      help='file to read email from (- for stdin, which is the default)',
                      default='-')
    parser.add_option('-s',
                      '--subject',
                      action='store',
                      dest='subject',
                      help='email subject)',
                      default='')
    parser.add_option('-F',
                      '--from',
                      action='store',
                      dest='from_addr',
                      help='sender email address (do-not-reply@digitaltorque.ca)',
                      default='do-not-reply@digitaltorque.ca')
    parser.add_option('-t',
                      '--to',
                      action='store',
                      dest='to_addr',
                      help='recipient email address (msoulier@digitaltorque.ca), comma-separated',
                      default='msoulier@digitaltorque.ca')
    (options, args) = parser.parse_args()
    if options.file == '-':
        email = sys.stdin.read()
    else:
        with open(options.file, "r") as emailfile:
            email = emailfile.read()

    send_email(email, options)

main()
