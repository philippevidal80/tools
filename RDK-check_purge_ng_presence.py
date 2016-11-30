#!/usr/bin/env python

import time
import sys
import logging
import psutil

for pid in psutil.pids():
    p = psutil.Process(pid)
    if p.name() == "python" and len(p.cmdline()) > 1 and "purge_ng.py" in p.cmdline()[1]:
        sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': ERROR - PURGE ALREADY LAUNCHED.\n')
        sys.stdout.flush()
        sys.exit("ERROR - PURGE ALREADY LAUNCHED.\n")

sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': INFO - NO PURGE RUNNING.\n')
sys.stdout.flush()
sys.exit(0)

