#!/usr/bin/python3

import sys

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <string key> [string plaintext]\n" % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) > 2:
        if len(sys.argv[1]) != len(sys.argv[2]):
            sys.stderr.write("input strings must be the same length\n")
            sys.exit(1)

    print("char-encoded string key:")
    for c in sys.argv[1]:
        sys.stdout.write("0x%X, " % ord(c))
    sys.stdout.write("\n")

    if len(sys.argv) > 2:
        print("string plaintext xor'd with string key:")
        for i, c1 in enumerate(sys.argv[1]):
            c2 = sys.argv[2][i]
            c3 = ord(c1) ^ ord(c2)
            sys.stdout.write("0x%X, " % c3)
        sys.stdout.write("\n")

main()
