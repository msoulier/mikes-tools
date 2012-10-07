#!/usr/bin/python

"""This is my weather plugin to Conky, pulling the latest forecast for Ottawa
from Environment Canada's RSS feed."""

import urllib, sys, textwrap
from xml.etree.ElementTree import parse
from optparse import OptionParser

rssfeed = 'http://www.weatheroffice.gc.ca/rss/city/on-118_e.xml'

def parse_options():
    usage="weather [options]"
    parser = OptionParser(usage=usage)
    parser.add_option('-v',
                      '--verbose',
                      action='store_true',
                      default=False,
                      help='upgrade logging from info to debug')
    parser.add_option('-l',
                      '--lines',
                      help="number of lines to output (default: all)",
                      action="store",
                      dest="lines",
                      type=int,
                      default=0)
    parser.add_option('-w',
                      '--wrap',
                      help="number of columns to wrap at (default: 80)",
                      action="store",
                      dest="wrap",
                      type=int,
                      default=80)

    options, args = parser.parse_args()

    return options

options = parse_options()
wrapper = textwrap.TextWrapper(width=options.wrap, subsequent_indent="    ")
count = 0
for elem in parse(urllib.urlopen(rssfeed)).findall('channel/item/title'):
    s = elem.text.encode('utf8', 'ignore')
    lines = wrapper.wrap(s)
    for line in lines:
        count += 1
        if options.lines and count > options.lines:
            break
        else:
            print line
    else:
        continue
    break

sys.exit(0)
