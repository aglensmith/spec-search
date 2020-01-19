# spec-search

Python script that searches local repositories for YAML and JSON Open API Specification (OAS) files (AKA Swagger), copies them, identifies changes, and generates reports.

## Requirements
* python 3.x

## Installation

```bash
# clone the repo
git clone https://github.com/aglensmith/spec-search.git

# copy to script to somewhere in your path
cp -v spec-search/spec-search.py ~/bin

# make script executable
chmod +x ~/bin/spec-search.py

spec-search.py --help
```

Alternatively, instead of using `cp` to copy the script, you can use a hard link:

```bash
git clone https://github.com/aglensmith/spec-search.git

# create a hard link in your bin to the script
ln spec-search/spec-search.py ~/bin/spec-search.py

# make script executable
chmod +x spec-search/spec-search.py

spec-search.py --help
```

Then you can update the executable in `~/bin` by pulling the upstream branch: 

```bash
cd spec-search/

git pull
```

## Usage

By default, `spec-search.py` searches the current working directory for spec files:

```bash
cd spec-search

spec-search.py

# output:
../spec-search/samples/repo1/pets.yaml
../spec-search/samples/repo1/store.yaml
../spec-search/samples/repo2/users.yaml
```

Save the default output using bash:

```bash
spec-search.py >> results.txt
```

Or the switch: 

```bash
spec-search.py --write files
```

spec-search can also aggregate a list of paths from all the files:

```
spec-search --print paths
```


```bash
usage: spec-search [-h] [--dir DIR] [--write {files,paths,report,all,none}]
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