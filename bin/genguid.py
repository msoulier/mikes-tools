#!/usr/bin/python3

import hashlib, os, time, base64

guid_urandom_bytes = 128

def genguid():
    input = b""
    if os.path.exists('/dev/urandom'):
        fd = os.open('/dev/urandom', os.O_RDONLY)
        randbytes = os.read(fd, guid_urandom_bytes)
        os.close(fd)
        input += base64.b64encode(randbytes)
    input += bytes(str(time.time()), 'utf-8')
    input += bytes(str(time.time()), 'utf-8')
    return hashlib.sha1(input).hexdigest()

print(genguid())
