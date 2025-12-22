#!/bin/sh

hostname=$(hostname -f | awk -F. '{print $1}')

case $hostname in
    affogato)
        id="DELL0A20:00 06CB:CE65 Touchpad"
        ;;
    ramirez)
        id="ASUE1412:00 04F3:3285 Touchpad"
        ;;
    *)
        echo "Unknown host: $hostname" 1>&2
        exit 1
esac

xinput set-prop "$id" "libinput Tapping Enabled" 1

xinput set-prop "$id" "libinput Natural Scrolling Enabled" 1

xinput set-prop "$id" "libinput Disable While Typing Enabled" 1
