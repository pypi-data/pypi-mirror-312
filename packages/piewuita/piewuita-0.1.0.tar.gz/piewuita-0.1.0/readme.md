# Piewuita

This is a library to init a python projects.

## Features

* Automatically create a project directory with:
    * main.py
    * readme.md
    * .gitignore
* Initializes a virtual environment (venv) in the project.
* Installs specified python modules and generates a `requirements.txt` file.
* Sets up Git in the project directory.

## Installation

### Pip with repo

``` bash
pip install git+https://github.com/Fuan200/piewuita.git
```

### Install the library

Comming soon

## Usage

The `piewuita` CLI simplifies project initialization. Use the following command to create a new project:

``` bash
piewuita -n <project_name> [-m <module1> <module2> ...]
```

* `-n, --name` (required): The name of the project.
* `-m, --modules` (optional): A space-separated list of Python modules/libraries to install in the `venv`.

#### Examples

``` bash
piewuita -n new_project
```

``` bash
piewuita -n new_project -m Flask requests pandas
```

## Requirements

* Python 3
* Git

## OS

* Linux
* Windows (comming soon)

## Author

:blue_heart: **Juan Antonio Díaz Fernández** - [Fuan200](https://github.com/Fuan200)