#!/bin/sh

if [ $# -lt 1 ]; then
    echo "Usage: $0 <directory>" 1>&2
    exit 1
fi

dir=$1

delay=10

if [ ! -d $dir ]; then
    echo "ERROR: $dir is not a directory" 1>&2
    exit 1
fi

while true
do
    # Note: only looking for jpgs, and spaces in names will break this
    for pic in $(find $dir -type f -name "*.jpg" | sort -R)
    do
        feh --bg-scale $pic
        sleep $delay
    done
done
