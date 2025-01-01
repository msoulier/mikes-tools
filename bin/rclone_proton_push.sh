#!/bin/sh

echo "copying Sync to google"
echo -n "proton 2fa code: "
read code
echo "Using $code"
$GOPATH/bin/rclone --progress sync --create-empty-src-dirs --protondrive-2fa=$code Sync proton:Sync
