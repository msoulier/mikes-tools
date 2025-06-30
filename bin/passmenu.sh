#!/bin/sh

TERMINAL=${TERMINAL:-alacritty}

$TERMINAL -T passmenu -e "pass show $(pass show | awk '{print $2}' | dmenu); read foo"

exit 0
