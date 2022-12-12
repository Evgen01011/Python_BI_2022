#! /root/miniconda3/bin/python

import sys
import os
import argparse

parser = argparse.ArgumentParser(
                    prog='ls analog',
                    description='Program returns contains of directory',
                    epilog='Text at the bottom of help')

parser.add_argument('-a', action='store_true')
parser.add_argument('directories', nargs='*')

args = parser.parse_args()


if args.a == 0:
    if len(args.directories) == 0:
        print(*list(filter(lambda x: x[0] != '.', os.listdir())), sep='\n')
    else:
        for directories in args.directories:
            print(*list(filter(lambda x: x[0] != '.', os.listdir(directories))), sep='\n')
else:
    if len(args.directories) == 0:
        print('.', '..', sep='\n')
        print(*os.listdir(), sep='\n')
    else:
        print('.', '..', sep='\n')
        for directories in args.directories:
            print(*os.listdir(directories), sep='\n')
