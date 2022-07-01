![Python 3.10](http://img.shields.io/badge/python-3.10-blue.svg)
[![MIT License](http://img.shields.io/badge/license-MIT%20License-blue.svg)](https://github.com/njordice/pingsweep/blob/main/LICENSE)

pingsweep is a easy to use asynchronous ping sweeper made using Python!

## Installation

Windows:

`git clone https://github.com/njordice/pingsweep.git && cd pingsweep`

`pip install -r requirements.txt`

Linux:

`git clone https://github.com/njordice/pingsweep.git && cd pingsweep`

`pip3 install -r requirements.txt`

## Usage

`usage: pingsweep.py [-h] [-q] [-w sec] [-t num] ip_range`

| Arguments           | Description                                                               |
|---------------------|---------------------------------------------------------------------------| 
| ip_range            | ip range of the network, example: 192.168.1.0/24                          | 
| -h, --help          | show help message and exit                                                |
| -q, --quiet         | quiet output, only print ip-addresses to the screen                       |
| -w sec, --wait sec  | timeout in seconds to wait for each reply (default: 1s)                   |
| -t num, --tasks num | number of concurrent tasks (default: dynamic, based on cpu threads * 2.5) |

## Examples

**Sweeping 254 hosts (really fast, just a couple of seconds)**

`pingsweep.py 192.168.1.0/24`

**Redirect output to a file (using --quiet flag to only print ip-addresses)**

`pingsweep.py 172.31.0.0/16 -q -t 50 > output.log`
