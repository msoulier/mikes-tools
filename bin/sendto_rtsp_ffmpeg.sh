#!/bin/sh

if [ $# -lt 2 ]; then
    echo "Usage: $0 <filename> <hostname:port>" 1>&2
    echo "    Readable at rtsp://<hostname:554/<channel>"
    echo "    where channel is filename"
    echo "    ie. $0 john_wick.mp4 localhost:5545"
    echo "    listenable at: rtsp://localhost:554/john_wick.mp4"
    exit 1
fi

filename=$1
hostname_port=$2
channel=$(basename $filename)

command="ffmpeg -re -i $filename -c copy -f rtsp rtsp://$hostname_port/$channel"

echo "Running command: $command"
exec $command
