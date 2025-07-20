#!/bin/sh

export HOME=/home/msoulier
#export DISPLAY=:0
#export XAUTHORITY=/run/user/1000/gdm/Xauthority

echo "Running $0" | tee -a $HOME/hotplug.log

set -e
hc() {
    $HOME/bin/herbstclient $1
}

echo "Running xrandr"
xrandr --auto

# This is only for herbstluftwm
if ps -ef | grep -v grep | grep -q herbstluftwm
then
    echo "Found herbstluftwm running" | tee -a $HOME/hotplug.log
else
    echo "Did not find herbstluftwm running - quitting" | tee -a $HOME/hotplug.log
    exit 0
fi

{
    hc reload

    hc list_monitors
} 2>&1 | tee -a $HOME/hotplug.log

exit 0
