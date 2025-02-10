#!/usr/bin/python3

"""This is my weather plugin to Conky, pulling the latest forecast for Ottawa
from Environment Canada's RSS feed."""

import urllib.request, sys
from xml.etree.ElementTree import parse
from optparse import OptionParser

rssfeed = 'http://weather.gc.ca/rss/city/on-118_e.xml'
ns = {'rss': 'http://www.w3.org/2005/Atom'}

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
count = 0
tree = parse(urllib.request.urlopen(rssfeed))
for elem in parse(urllib.request.urlopen(rssfeed)).findall('rss:entry/rss:title', ns):
    print(elem.text)

sys.exit(0)
