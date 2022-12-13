#! /root/miniconda3/bin/python

import sys
import os
import shutil
import argparse

# create arguments - directory/ files for copy and appropriate flag 

parser = argparse.ArgumentParser(
                    prog='cp analog',
                    description='Program copy file and directories',
                    epilog='Text at the bottom of help')

parser.add_argument('-r', '-R', action='store_true')
parser.add_argument('directories', nargs='+')

args = parser.parse_args()

for file in args.directories[:-1]:                                   # iterate on every directory/ files for copy except last
    if os.path.isfile(file) and not args.r:                          # copy files
        shutil.copy(file, args.directories[-1])
    elif os.path.isdir(file) and args.r:                             # copy directories
        shutil.copytree(file, args.directories[-1])
    else:
        sys.stderr.write('Error: type and flags do not match\n')     # stderr in the case inconsistency of type and flags 
