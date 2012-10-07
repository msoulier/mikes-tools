#!/bin/sh
# This script changes the video configuration for when I'm unplugging the vga
# cable from an external monitor, going back to my netbook's native
# resolution. I run this on my ASUS EEEPc.

xrandr --auto
xrandr --output VGA1 --off
xrandr --output LVDS1 --mode "1024x600"
