#! /root/miniconda3/bin/python

import sys
import os
import argparse

# create arguments - file and flags

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
current_list = []

# wc from stdin
if len(args.files) == 0:
    for line in sys.stdin:
        output[0] += 1
        output[1] += len(line)
        output[2] += len(line.encode('utf-8'))
# wc from files        
else:
    for file in args.files:
        if not os.path.exists(file):                                # check file existence 
            print(file, ': No such file or directory')
        else:
            line_number = 0
            word_number = 0
            bites_number = 0
            with open(file, 'r') as reading:
                for line in reading.readlines():                    # collect statistics by every line
                    line_number += 1
                    word_number += len(line.split())
                    bites_number += len(line.encode('utf-8'))
                output[0] += line_number                            # collect total statistics
                output[1] += word_number
                output[2] += bites_number
                
                # different outpyt option
                if {args.line, args.words, args.bytes} <= {0}:
                    print(line_number, word_number, bites_number, file)
                else: 
                    # determine every flags
                    if args.line is True: 
                        print(line_number, end=' ')
                    if args.words is True:
                        print(word_number, end=' ')
                    if args.bytes is True:
                        print(bites_number, end=' ')
                    print(file)
                    
# total output
if {args.line, args.words, args.bytes} <= {0}:
    print(*output, 'Total')
else:
    if args.line is True:
        print(output[0], end=' ')
    if args.words is True:
        print(output[1], end=' ')
    if args.bytes is True:
        print(output[2], end=' ')
    print('Total')
