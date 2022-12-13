#! /root/miniconda3/bin/python

import sys
import os
import shutil
import argparse


# create arguments - file/ directory and flag for remove directories

parser = argparse.ArgumentParser(
                    prog='rm analog',
                    description='Program remove file or directory',
                    epilog='Text at the bottom of help')

parser.add_argument('directories', nargs='+')
parser.add_argument('-r', '--recursive', action='store_true')

args = parser.parse_args()

if len(args.directories) == 0:                                                        # check attendence of argument
    print('rm: missing operand')
else:
    for directories in args.directories:
        if not os.path.exists(directories):                                           # check file existence
            print('rm: cannot remove ', directories, ': No such file or directory')
        elif os.path.isfile(directories):                                             # remove files
            os.remove(directories)
        elif os.path.isdir(directories) and args.recursive:                           # remove directories
            shutil.rmtree(directories)
        else:
            print('rm: cannot remove ', directories, ': Is a directory')              # warning if user forgot flag
