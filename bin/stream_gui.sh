#!/bin/sh

rtsp_port=1234

vlc=$(which vlc)
if [ "x$vlc" = "x" ]; then
    echo "ERROR: no vlc command found" 1>&2
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: $0 <input file>" 1>&2
    exit 1
fi

infile=$1

if [ ! -e $infile ]; then
    echo "ERROR: input file not found: $infile" 1>&2
    exit 1
fi

vlc -vv $1 \
    :sout=#duplicate{dst=rtp{sdp=rtsp://:${rtsp_port}/},dst=display} :no-sout-all :sout-keep
