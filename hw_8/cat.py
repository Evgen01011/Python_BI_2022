#! /root/miniconda3/bin/python

import sys
import os
import shutil
import argparse

# create arguments - files for reading

parser = argparse.ArgumentParser(
                    prog='cat analog',
                    description='Program read file',
                    epilog='Text at the bottom of help')

parser.add_argument('files', nargs='*')

args = parser.parse_args()

# read from stdin in the case of files absence 
if len(args.files) == 0:
    for line in sys.stdin:
        print(line.strip())
# read from files
else:
    for files in args.files:
        if not os.path.exists(files):                          # check files existence
            print(files, ': No such file or directory')
        else:
            with open(files, 'r') as reading:
                for line in reading:                           # line by line in stdout
                    print(line.strip())
