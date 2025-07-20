#!/usr/bin/env bash

screenres=$(xrandr |awk '/\*/ {print $1}')
screenheight=$(echo $screenres | awk -Fx '{print $2}')
screenwidth=$(echo $screenres | awk -Fx '{print $1}')
halfwidth=$((($screenwidth / 2) - 128))
halfheight=$((($screenheight / 2) - 128))

icon="$HOME/lockicon"
tmpbg='/tmp/screen.png'
rm -f $tmpbg

(( $# )) && { icon=$1; }

scrot "$tmpbg"
convert "$tmpbg" -scale 10% -scale 1000% "$tmpbg"
convert "$tmpbg" "$icon" -geometry 256x256+$halfwidth+$halfheight -composite -matte "$tmpbg"
convert "$tmpbg" "$icon" -geometry 256x256+$screenwidth+$screenheight -composite -matte "$tmpbg"
i3lock -i "$tmpbg"
