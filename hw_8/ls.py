#! /root/miniconda3/bin/python

import sys
import os
import argparse

# create arguments - directory and flag for hidden files 

parser = argparse.ArgumentParser(
                    prog='ls analog',
                    description='Program returns contains of directory',
                    epilog='Text at the bottom of help')

parser.add_argument('-a', action='store_true')
parser.add_argument('directories', nargs='*')

args = parser.parse_args()

# output of explicit file
if not args.a: 
    if len(args.directories) == 0:                                                           # output for current directory
        print(*list(filter(lambda x: x[0] != '.', os.listdir())), sep='\n')
    else:
        for directories in args.directories:                                                 # output for other directories
            print(*list(filter(lambda x: x[0] != '.', os.listdir(directories))), sep='\n')            
# output of hidden file            
else:
    if len(args.directories) == 0:                                                           # output for current directory
        print('.', '..', sep='\n')
        print(*os.listdir(), sep='\n')
    else:                                                                                    # output for other directories
        print('.', '..', sep='\n')
        for directories in args.directories:
            print(*os.listdir(directories), sep='\n')
