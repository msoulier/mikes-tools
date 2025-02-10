#!/bin/sh

while true
do
    echo "Starting conky read loop"
    conky | while read LINE; do xsetroot -name "$LINE"; done
    echo "ERROR: conky died - restarting" 1>&2
    sleep 2
done
