#!/usr/bin/python3

"""The purpose of this script is to recursively traverse a directory tree
pointed to as a command-line argument, and convert any files found
to have no upper-case or spaces in the name. Upper-case is converted to
lower-case, and one or more spaces are converted to a single underscore.
Parentheses are removed, as well as single and double quotes, ampersands."""

import os
import sys
import re
from optparse import OptionParser

assert( sys.version_info.major == 3 )

error = sys.stderr.write

def fixname(oldname: str) -> str:
    """This function takes the name of a file or directory, and 'cleans' it,
    removing or transforming undesirable characters, and returns the new
    name."""
    # FIXME - hardcoded skiplist
    if oldname.endswith('.rpm'):
        return oldname
    newname: str = oldname.lower()
    newname = re.sub('\s+', '_', newname)
    newname = re.sub('-', '_', newname)
    newname = re.sub('[@?]', '_', newname)
    newname = re.sub(r'&', 'and', newname)
    newname = re.sub('[^a-z0-9_.]', '', newname)
    newname = re.sub(r'_+', '_', newname)
    # If an underscore is next to a period, remove it.
    newname = re.sub(r'_*\._*', '.', newname)
    # If the file ends in .mp3.\d+, remove the digits.
    newname = re.sub(r'\.mp3\.\d+$', '.mp3', newname)
    # Remove any non-alphanumeric prefixes
    newname = re.sub(r'^[^a-z0-9]+', '', newname)
    return newname

def fixdir(options, root: str, dirname: str):
    newname: str = fixname(dirname)
    if newname != dirname:
        oldpath: str = os.path.join(root, dirname)
        newpath: str = os.path.join(root, newname)
        if options.test:
            print("Test mode: would rename directory", oldpath, "to", newpath)
        else:
            print("Renaming directory", oldpath, "to", newpath)
            os.rename(oldpath, newpath)

def visit(options, dirname: str, files: list[str]):
    """Walk the tree at path."""
    for oldfile in files:
        newfile: str = fixname(oldfile)
        if oldfile != newfile:
            oldpath: str = os.path.join(dirname, oldfile)
            newpath: str = os.path.join(dirname, newfile)
            if options.test:
                print("Test mode: would rename", oldpath, "to", newpath)
            else:
                print("Renaming", oldpath, "to", newpath)
                if not options.force and os.path.exists(newpath):
                    error("%s exists already, use --force option to force overwrite" % newpath)
                    continue
                try:
                    os.rename(oldpath, newpath)
                except OSError as err:
                    error("Failed to rename %s: %s\n" % (oldfile, str(err)))

def main():
    """This is the main function, responsible for validating the command-line
    arguments and dispatching any events."""
    usage: str = "sane-filenames [-d|--directories] [-n|--nofiles] " + \
                 "[-t|--test] <paths>"
    parser: OptionParser = OptionParser(usage=usage)
    parser.add_option('-d',
                      '--directories',
                      action='store_true',
                      dest='directories',
                      help='process directories too',
                      default=False)
    parser.add_option('-n',
                      '--nofiles',
                      action='store_false',
                      dest='files',
                      help='do not process files',
                      default=True)
    parser.add_option('-t',
                      '--test',
                      action='store_true',
                      dest='test',
                      help='test run, make no changes',
                      default=False)
    parser.add_option('-f',
                      '--force',
                      action='store_true',
                      dest='force',
                      help='force overwriting of existing files',
                      default=False)
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    for path in args:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path, topdown=False):
                visit(options, root, files)
                if options.directories:
                    for d in dirs:
                        fixdir(options, root, d)
            fixdir(options, os.path.dirname(path), os.path.basename(path))
        else:
            # If it's not a directory, it's a file - fix it
            # call visit() on the file
            fname: str = os.path.basename(path)
            visit(options, os.path.dirname(path), [fname])
    sys.exit(0)

if __name__ == '__main__':
    main()
