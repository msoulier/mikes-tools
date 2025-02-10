#!/usr/bin/python3

import argparse
import sys

def parse_options():
    parser = argparse.ArgumentParser(description="Non UTF-8 character handler")
    parser.add_argument('-c',
                        '--convert',
                        dest='convert',
                        action='store_true',
                        default=False,
                        help='Output to stdout with conversion')
    parser.add_argument('files',
                        action='append',
                        nargs='+',
                        default=[],
                        help="Input files")
    options = parser.parse_args()
    return options

def main():
    options = parse_options()

    files = options.files[0]
    rv = 0
    for input_file in files:
        lineno = 0
        error_list = []
        with open(input_file, "rb") as ifile:
            while True:
                bline = ifile.readline()
                if not bline:
                    break
                lineno += 1
                try:
                    uline = bline.decode('utf-8')
                except UnicodeDecodeError as err:
                    if options.convert:
                        uline = bline.decode('utf-8', 'replace')
                    else:
                        error_list.append(lineno)

                if options.convert:
                    sys.stdout.write(uline)

        if error_list:
            sys.stderr.write("Non UTF-8 characters found on the following lines:\n")
            for error_line in error_list:
                sys.stderr.write(f"    line {error_line}\n")
            rv = 1

    sys.exit(rv)

main()
