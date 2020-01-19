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

###############################################################################
# CONFIG
###############################################################################

# for dirs and files
EXCLUDES = [
    "*node_modules*",
    "spec-search-results*"
]

###############################################################################
# CODE
###############################################################################

def find_swagger(directory, includes=None, excludes=None):
    swagger = []

    if includes is None:
        includes = ['*.yaml', '*.yml', '*.json'] # for files only

    # transform glob patterns to regular expressions
    includes = r'|'.join([fnmatch.translate(x) for x in includes])
    excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

    for root, dirs, files in os.walk(directory):
        
        # exclude dirs
        dirs[:] = [os.path.join(root, d) for d in dirs]
        dirs[:] = [d for d in dirs if not re.match(excludes, d)]

        # exclude/include files
        files = [os.path.join(root, f) for f in files]
        files = [f for f in files if not re.match(excludes, f)]
        files = [f for f in files if re.match(includes, f)]

        for file in files:
            # print(os.path.join(root, file))
            if is_swagger(os.path.join(root, file)):
                # print(os.path.join(folder, file))
                swagger.append(os.path.join(root, file))
    return swagger        

def get_all_paths(swagger_parsed_list):
    paths = []
    for s in swagger_parsed_list:
        for k,v in s["paths"].items():
            paths.append(k)
    return paths

def parse_all_swagger(swagger_list):
    parsed_swagger = []
    for s in swagger_list:
        parsed = parse_swagger(s)
        if type(parsed) == dict:
            parsed_swagger.append(parsed)
    return parsed_swagger

def parse_swagger(file_path):
    return parse_yaml(file_path)

def parse_yaml(file_path):
    with open(file_path, 'r') as stream:
        return yaml.safe_load(stream)

def build_report(swagger):
    report = [
        f'## Spec Search Report',
        f'* **Report Date**: {datetime.now().strftime("%c")}',
        f'* **Number of Files**: {len(swagger)}'
    ]
    return report

###############################################################################
# HELPERS
###############################################################################

def is_swagger(file):
    with open(file, 'r', encoding="utf8") as f:
        next_line = f.readline().lower()
        if len(next_line) < 2:
            next_line = f.readline().lower()
        if "openapi" in next_line or "swagger" in next_line:
            return True
    return False    

def is_operation(k):
  return k.lower() in [
    "post",
    "put",
    "delete",
    "get",
    "patch"
  ]

def copy_swagger(swagger, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(swagger, dest)

def print_swagger_paths(swaggers_paths):
    """prints the file names"""
    for path in swaggers_paths:
        print(path)

def print_all_paths(swagger_parsed):
    for p in get_all_paths(swagger_parsed):
        print(p)

def write_list(list, filename):
    """writes each element in a list to a new line in a file"""
    with open(filename, "w") as file:
        for x in list:
            file.write(str(x) + "\n")

###############################################################################
# CLI
###############################################################################
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
    p = argparse.ArgumentParser(prog="spec-search", description="Find OAS files in many repos", epilog="...awesomely")
    p.add_argument('--dir', type=str, default=os.getcwd(), help="Directory to recursively search; defaults to CWD.")
    p.add_argument('--write', choices=['files', 'paths', 'report', 'all', 'none'], default='none', help="Writes chosen results to a file")
    p.add_argument('--print', choices=['files', 'paths', 'report', 'all', 'none'], default='none', help="Prints chosen results")
    p.add_argument('--copy', action="store_true", help="copy and aggregate files into a single dir")
    p.add_argument('--out', type=str, nargs=3,  action="append", default=['files.txt','paths.txt', 'report.md'],help="Optionally list outfiles for --write")
    p.add_argument('--version', action='version', version='%(prog)s 2.0')
    return p

def print_paths(dir):
    swagger_files = find_swagger(dir, excludes=EXCLUDES)
    paths = get_all_paths(parse_all_swagger(swagger_files))
    for p in paths:
        print(p)

def process_options(options):

    default = True

    if options.copy:
        specs = find_swagger(options.dir, excludes=EXCLUDES)
        for s in specs:
            dest = os.getcwd() + "/spec-search-results" + s.split(options.dir)[-1]
            print(dest)
            copy_swagger(s, dest)
        default = False
    if options.write == "files":
        specs = find_swagger(options.dir, excludes=EXCLUDES)
        write_list(specs, options.out[0])
        default = False
    if options.write == "paths":
        swagger_files = find_swagger(options.dir, excludes=EXCLUDES)
        swagger_parsed = parse_all_swagger(swagger_files)
        all_paths = get_all_paths(swagger_parsed)
        write_list(all_paths, options.out[1])
        default = False
    if options.write == "report":
        default = False
    if options.write == "all":
        default = False
    if options.print == "report":
        for i in build_report(["test", "test2"]):
            print(i)
        default = False
    if options.print == "paths":
        print_paths(options.dir)
        default = False
    if default:
        specs = find_swagger(options.dir, excludes=EXCLUDES)
        print_swagger_paths(specs)

if __name__ == "__main__":
    parser = get_parser()
    process_options(parser.parse_args())
