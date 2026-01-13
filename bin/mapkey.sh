#!/bin/sh

map=truecrypt1
mountpoint=/mnt/secret

action="help"
if [ "x$1" != "x" ]; then
    action=$1
fi

tcplay=$(which tcplay)
if [ "x$tcplay" = "x" ]; then
    echo "tcplay binary not found" 1>&2
    exit 1
fi

case $action in
    help)
        echo "Usage: $0 <help|mount|unmount>"
        ;;
    mount)
        if [ -e /dev/mapper/$map ]; then
            echo "It looks like $map is already mounted"
        else
            sudo tcplay --map=$map --device=/dev/sda2 || exit 1
        fi
        if [ ! -d $mountpoint ]; then
            echo "$mountpoint does not exist - creating"
            sudo mkdir -p $mountpoint
        fi
        sudo mount /dev/mapper/$map $mountpoint || exit 1
        echo "Mounted at $mountpoint"
        ;;
    unmount)
        sudo umount $mountpoint || exit 1
        sudo tcplay --unmap=$map || exit 1
        echo "Umounted - removing $mountpoint"
        sudo rmdir $mountpoint || exit 1
        echo "Done"
        ;;
    *)
        echo "Unknown action: $action"
        exit 1
        ;;
esac

exit 0
