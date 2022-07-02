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
  -t num, --tasks num  number of concurrent tasks (default: 30) # dynamic, based on cpu threads * 2.5
```

```
Cores	Threads	  Default Tasks	
2	4	  10	
4	8	  20	
6	12	  30	
8	16	  40	
10	20	  50	
12	24	  60	
14	28	  70	
16	32	  80	
18	36	  90	
20	40	  100	
```

## Examples

**Sweeping 254 hosts (really fast, just a couple of seconds)**

`pingsweep.py 192.168.1.0/24`

**Redirect output to a file (using --quiet flag to only print ip-addresses)**

`pingsweep.py 172.31.0.0/16 -q -t 50 > output.log`
