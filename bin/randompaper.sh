#!/bin/sh

cd $HOME || exit 1

r=$( od -An -N2 -i /dev/urandom )
npics=$(find $HOME/Pictures/ -type f | grep -v '\.git' | wc -l)
npic=$(( r%npics ))

count=0
for pic in $(find $HOME/Pictures -type f | grep -v '\.git')
do
    if [ $npic -eq $count ]; then
        ln -sf $pic paper
        break
    fi
    count=$(( $count+1 ))
done

feh --bg-scale $HOME/paper || exit 1

exit 0
