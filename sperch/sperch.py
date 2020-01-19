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


_CONFIG = yaml.safe_load(open("sperch/sperch.yaml"))
_EXCLUDES = _CONFIG['excludes']

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

def print_paths(dir):
    swagger_files = find_swagger(dir, excludes=_EXCLUDES)
    paths = get_all_paths(parse_all_swagger(swagger_files))
    for p in paths:
        print(p)