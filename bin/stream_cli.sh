#!/bin/sh

rtsp_port=1234

cvlc=$(which cvlc)
if [ "x$cvlc" = "x" ]; then
    echo "ERROR: no cvlc command found" 1>&2
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

cvlc -vvv $1 \
    :sout=#rtp{sdp=rtsp://:$rtsp_port/} :no-sout-all :sout-keep
