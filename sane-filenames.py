#!/usr/bin/python

"""The purpose of this script is to recursively traverse a directory tree
pointed to as a command-line argument, and convert any files found
to have no upper-case or spaces in the name. Upper-case is converted to
lower-case, and one or more spaces are converted to a single underscore.
Parentheses are removed, as well as single and double quotes, ampersands."""

import os, sys, re
from optparse import OptionParser

error = sys.stderr.write
directories = []

def process_directories(directories, options):
    """This function takes an array of directories, and performs the same
    operations done to fix file names on the directories, renaming them to be
    more amenable."""
    # Reverse the directory listing, so we work from the bottom up. 
    directories.reverse()
    for dir in directories:
        head, tail = os.path.split(dir)
        newtail = fixname(tail)
        newdir = os.path.join(head, newtail)
        if newdir != dir:
            if options.test:
                print "Test mode: would rename %s to %s" % (dir, newdir)
            else:
                print "Renaming directory %s to %s" % (dir, newdir)
                try:
                    os.rename(dir, newdir)
                except OSError, err:
                    error("Failed to rename %s: %s\n" % (dir, str(err)))

def fixname(oldname):
    """This function takes the name of a file or directory, and 'cleans' it,
    removing or transforming undesirable characters, and returns the new
    name."""
    # FIXME - hardcoded skiplist
    if oldname.endswith('.rpm'):
        return oldname
    if oldname == '.DS_Store':
        return oldname
    newname = oldname.lower()
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

def visit(options, dirname, names):
    """This function's purpose is to act upon every directory traversed
    by the os.path.walk function. It performs the actual conversion of 
    the files."""
    global directories
    if not dirname:
        dirname = '.'

    if options.directories:
        directories.append(dirname)
    if not options.files:
        return

    files = filter(lambda x: os.path.isfile(dirname + os.sep + x), names)

    for oldfile in files:
        newfile = fixname(oldfile)
        if oldfile != newfile:
            if options.test:
                print "Test mode: would rename %s to %s" % (oldfile, newfile)
            else:
                print "Renaming %s to %s" % (oldfile, newfile)
                try:
                    os.rename(dirname + os.sep + oldfile, 
                              dirname + os.sep + newfile)
                except OSError, err:
                    error("Failed to rename %s: %s\n" % (oldfile, str(err)))

def main():
    """This is the main function, responsible for validating the command-line
    arguments and dispatching any events."""
    usage = "sane-filenames [-d|--directories] [-n|--nofiles] " + \
            "[-t|--test] <paths>"
    parser = OptionParser(usage=usage)
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
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    for path in args:
        if os.path.isdir(path):
            os.path.walk(path, visit, options)
        else:
            # If it's not a directory, it's a file - fix it
            # call visit() on the file
            fname = os.path.basename(path)
            visit(options, os.path.dirname(path), [fname])
    if options.directories:
        process_directories(directories, options)
    sys.exit(0)

if __name__ == '__main__':
    main()
