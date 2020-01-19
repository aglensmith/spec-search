#!/usr/bin/env python3

import json
import os
import enum
import os.path
import argparse
import fnmatch
import re
import yaml
import shutil
import sys
from datetime import datetime
from .sperch import *

def color(text, options):
    choices = {
        "red": '\033[95m',
        "blue": '\033[94m',
        "green": '\033[92m',
        "yellow": '\033[93m',
        "red": '\033[91m',
        "bold": '\033[1m',
        "underline": '\033[4m',
    }
    for option in options:
        text = choices[option] + text 
    return text + '\033[0m'

def get_parser():
    parser = argparse.ArgumentParser(prog="sperch", description="Find OAS files in many repos", epilog="...awesomely")
    subparsers = parser.add_subparsers(help='Sub-commands')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    search = subparsers.add_parser('search', help='Recursively search a specified dir for swagger and OAS files')
    search.add_argument('--dir', type=str, default=os.getcwd(), help="Directory to recursively search; defaults to CWD.")
    search.add_argument('--print_only', choices=['files', 'paths', 'report', 'all', False], default=False, help="Print results")
    return parser

def main():
    
    parser = get_parser()
    options = parser.parse_args()
    
    default = True

    if not options.print_only:
        print(options.dir)
        print_paths(options.dir)
        default = False
    else:
        print("else")

if __name__ == '__main__':
    main()