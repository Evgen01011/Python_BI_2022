#! /root/miniconda3/bin/python

import sys
import os
import shutil
import argparse

parser = argparse.ArgumentParser(
                    prog='cp analog',
                    description='Program copy file and directories',
                    epilog='Text at the bottom of help')

parser.add_argument('-r', '-R', action='store_true')
parser.add_argument('directories', nargs='+')

args = parser.parse_args()

for file in args.directories[:-1]:
    if os.path.isfile(file) and not args.r:
        shutil.copy(file, args.directories[-1])
    elif os.path.isdir(file) and args.r:
        shutil.copytree(file, args.directories[-1])
    else:
        sys.stderr.write('Error: type and flags do not match\n')
