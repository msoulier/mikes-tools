#!/bin/bash

OPTIONS="--info=inline --print-query --bind=ctrl-space:print-query,tab:replace-query"

command=$(bins | fzf $OPTIONS | tail -1)

exec 1>$HOME/log/frun.$$
exec 2>&1
exec setsid "$command"
