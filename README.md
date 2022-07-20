![Python 3.10](http://img.shields.io/badge/python-3.10-blue.svg)
[![MIT License](http://img.shields.io/badge/license-MIT%20License-blue.svg)](https://github.com/njordice/pingsweep/blob/main/LICENSE)

Asynchronous ping sweeper made using Python! 🚀

## Installation

Windows:

```bash
git clone https://github.com/njordice/pingsweep.git
cd pingsweep
pip install -r requirements.txt
```

Linux:

```bash
git clone https://github.com/njordice/pingsweep.git
cd pingsweep
pip3 install -r requirements.txt
```
## Usage

```bash
usage: pingsweep.py [-h] [-q] [-w sec] [-t num] ip_range

positional arguments:
  ip_range             ip range of the network, e.g. 192.168.1.0/24

options:
  -h, --help           show this help message and exit
  -q, --quiet          quiet output, only print ip-addresses to screen
  -w sec, --wait sec   timeout in seconds to wait for each reply (default: 1s)
  -t num, --tasks num  number of concurrent tasks (default: dynamic, cpu threads * 2.5)
```

## Example
`pingsweep.py 192.168.1.0/24`
