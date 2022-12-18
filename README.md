# Aircraft Collision Avoidance System

This project's objective is to create a centralized aircraft controller operating in 3-D with the primary goal being to avoid aircraft collisions.


## Contents

* [Authors](#authors)
* [Background](#background)
* [Setup](#setup)
* [Usage](#usage)
## Authors

- [@EthanMayer](https://github.com/EthanMayer)


## Background

This is the Hybrid and Embedded Systems final software project.

## Setup

This project, by default, should not need any external dependencies. All includes are either native to Python or written by me. If you do not have Python installed, you can install Python 3.10.5 with Homebrew:

`brew install python@3.10.5`

This project uses Python Environments to manage dependencies (.venv). If it works properly, you probably don't even need to install python. However, I would suggest running this via VSCode on a Windows machine. After you have cloned the repository, and you have the Python VSCode plugin (https://marketplace.visualstudio.com/items?itemName=ms-python.python) launch VSCode and click on the "Open Folder" option under "File" and select wherever you cloned this project. Once opened, click `ctrl + shift + P` to open the VSCode command palette. Type `Python: Select Interpreter` until you see it. Once you do, select:

`Python 3.10.5 ('.venv.': venv)`

Once you have select this, click on the `driver.py` file and click the play button at the top right to proceed with the project's demo

**Additional Information**

This project was implemented using the latest version of VSCode with Python 3.10.5 on Windows 10 running on an x86_64 machine. It has been cloned to a Windows 10 machine and it worked. It has also been cloned to a MacBookPro M1 (ARM) running Python 3.9 and it worked.
## Usage

The program has built-in demos for you to use. First, run the driver to the simulation either by using the play button in VSCode (recommended) or by typing into the console:

`python3 driver.py`

Once the driver has launched, it will prompt you which demo you would like to run. There are three built-in demos with random coordinates for the planes. To use demo 3, for example, just type:

`3`

You will then begin seeing visual output in the from of ASCII graphs. This way, you can visually verify that the controller is working as intended. Feel free to run all of the demos.

