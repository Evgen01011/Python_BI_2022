#! /root/miniconda3/bin/python

import sys
import os
import argparse

# create arguments - file/ directory

parser = argparse.ArgumentParser(
                    prog='sort analog',
                    description='Program returns sorting file or input',
                    epilog='Text at the bottom of help')

parser.add_argument('directories', nargs='*')

args = parser.parse_args()

input_list = []

if len(args.directories) == 0:                      # sort from stdin
    for line in sys.stdin:
        input_list.append(line)
else:
    for file in args.directories:                   # sort from file
        with open(file, 'r') as reading:
            for line in reading:
                input_list.append(line.split())

for element in sorted(input_list):                  # sorting
    print(*element)
