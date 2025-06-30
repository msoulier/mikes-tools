#!/bin/sh

# Common stuff to start on login.
echo "Starting Emacs in daemon mode"
nohup emacs --daemon &
