#!/bin/sh

DEFSINK=$(pactl get-default-sink)

while true
do
    if pactl get-sink-mute $DEFSINK | grep -q yes
    then
        MUTED="(Muted)"
    else
        MUTED=""
    fi
    VOL=$(pactl get-sink-volume $DEFSINK | awk '{print $5}')
    ROOTDISK=$(df -h / | tail -1 | awk '{print $5}')
    DATETIME=$(date +"%A %b %e %Y %H:%M:%S %z")
    BAT=$(acpi)
    LINE="Vol $VOL $MUTED | / $ROOTDISK | $BAT | $DATETIME"
    xsetroot -name "$LINE"
    sleep 2
done
