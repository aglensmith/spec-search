```python
    if options.copy:
        specs = find_swagger(options.dir, excludes=EXCLUDES)
        for s in specs:
            dest = os.getcwd() + "/sperch-results" + s.split(options.dir)[-1]
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
```

# sperch

Python script that searches locaz repositories for YAML and JSON Open API Specification (OAS) files (AKA Swagger), copies them, identifies changes, and generates reports.

## Requirements
* python 3.x

## Installation

```bash
# clone the repo
git clone https://github.com/aglensmith/sperch.git

# copy to script to somewhere in your path
cp -v sperch/sperch.py ~/bin

# make script executable
chmod +x ~/bin/sperch.py

sperch.py --help
```

Alternatively, instead of using `cp` to copy the script, you can use a hard link:

```bash
git clone https://github.com/aglensmith/sperch.git

# create a hard link in your bin to the script
ln sperch/sperch.py ~/bin/sperch.py

# make script executable
chmod +x sperch/sperch.py

sperch.py --help
```

Then you can update the executable in `~/bin` by pulling the upstream branch: 

```bash
cd sperch/

git pull
```

## Usage

By default, `sperch.py` searches the current working directory for spec files:

```bash
cd sperch

sperch.py

# output:
../sperch/samples/repo1/pets.yaml
../sperch/samples/repo1/store.yaml
../sperch/samples/repo2/users.yaml
```

Save the default output using bash:

```bash
sperch.py >> results.txt
```

Or the switch: 

```bash
sperch.py --write files
```

sperch can also aggregate a list of paths from all the files:

```
sperch --print paths
```


```bash
usage: sperch [-h] [--dir DIR] [--write {files,paths,report,all,none}]
                   [--print {files,paths,report,all,none}] [--out OUT OUT OUT]
                   [--version]

Find OAS files in many repos

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR             Directory to recursively search; defaults to CWD.
  --write {files,paths,report,all,none}
                        Writes chosen results to a file
  --print {files,paths,report,all,none}
                        Prints chosen results
  --out OUT OUT OUT     Optionally list outfiles for --write
  --version             show program's version number and exit
```