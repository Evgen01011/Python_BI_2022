#! /root/miniconda3/bin/python

import sys
import os
import argparse

parser = argparse.ArgumentParser(
                    prog='wc analog',
                    description='Program returns statistics of contains',
                    epilog='Text at the bottom of help')

parser.add_argument('-l', '--line', action='store_true')
parser.add_argument('-w', '--words', action='store_true')
parser.add_argument('-c', '--bytes', action='store_true')
parser.add_argument('files', nargs='*')

args = parser.parse_args()

output = [0, 0, 0]
switch = 1
current_list = []

if len(args.files) == 0:
    for line in sys.stdin:
        output[0] += 1
        output[1] += len(line)
        output[2] += len(line.encode('utf-8'))
else:
    for file in args.files:
        if not os.path.exists(file):
            print(file, ': No such file or directory')
        else:
            line_number = 0
            word_number = 0
            bites_number = 0
            with open(file, 'r') as reading:
                for line in reading.readlines():
                    line_number += 1
                    word_number += len(line.split())
                    bites_number += len(line.encode('utf-8'))
                output[0] += line_number
                output[1] += word_number
                output[2] += bites_number
                if {args.line, args.words, args.bytes} <= {0}:
                    print(line_number, word_number, bites_number, file)
                else: 
                    if args.line is True:
                        current_list.append(line_number)
                    if args.words is True:
                        current_list.append(word_number)
                    if args.bytes is True:
                        current_list.append(bites_number)
                    print(*current_list, file)
                    current_list = []

ultimate_list = []
if {args.line, args.words, args.bytes} <= {0}:
    print(*output, 'Total')
else:
    if args.line is True:
        ultimate_list.append(output[0])
    if args.words is True:
        ultimate_list.append(output[1])
    if args.bytes is True:
        ultimate_list.append(output[2])

if len(ultimate_list) > 0:
    print(*ultimate_list, 'Total')
