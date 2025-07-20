#!/bin/sh

# davmail running?
if ps -ef | grep -v grep | grep -q davmail
then
    :
else
    echo "davmail is not running" 1>&2
    exit 1
fi

. $HOME/.bash_functions

mitelinit

eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"

pyenv activate caldav

python caldavto.py > ~/pim/org/workcal.org || exit 1

exit 0
