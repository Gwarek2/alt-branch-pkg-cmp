# alt-branch-pkg-cmp

## About
A command line interface tool for comparing packages from two different branches of ALT Linux. Package lists for branches are fetched from [ALT Linux repo API](https://rdb.altlinux.org/api/).

## Requirements
- [python3](https://www.python.org/downloads/)
- pip
- [virtualenv](https://pypi.org/project/virtualenv/)
- [build tool](https://pypi.org/project/build/)

## Setup for development
1. Clone the repository
2. From project root directory run next commands:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run tool
```
cd src
python3 cli.py
```

Run unit tests:
```
cd src
python3 -m unittest discover tests
```

## Installation
```
python3 -m build -w
pip install dist/alt_branch_pkg_cmp-0.1-py3-none-any.whl
```

## Usage
Run tool:
```
alt-branch-pkg-cmp <branch1> <branch2>
```
