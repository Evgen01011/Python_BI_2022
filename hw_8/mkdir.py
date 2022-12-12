#! /root/miniconda3/bin/python

import sys
import os
import shutil
import argparse

parser = argparse.ArgumentParser(
                    prog='mkdir analog',
                    description='Program create directory',
                    epilog='Text at the bottom of help')

parser.add_argument('-p', '--parents', action='store_true')
parser.add_argument('directories', nargs='+')

args = parser.parse_args()

for directories in args.directories:
    if args.parents:
        creation = os.path.join(os.getcwd(), directories)
        os.makedirs(creation)
    else:
        try: 
            creation = os.path.join(os.getcwd(), directories)
            os.mkdir(creation)
        except:
            print('No way - mkdir: cannot create directory', directories)


