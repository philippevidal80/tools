#!/usr/bin/env python

import time
import sys
import logging
import psutil

script = ''

try:
   opts, args = getopt.getopt(argv,"hs:",["help","script="])
except getopt.GetoptError:
   print 'check_script_presence.py -s <script>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'check_script_presence.py -s <script>'
      sys.exit()

if script == '':
      print 'check_script_presence.py -s <script>'
      sys.exit(1)

for pid in psutil.pids():
    p = psutil.Process(pid)
    if p.name() == "python" and len(p.cmdline()) > 1 and scirpt in p.cmdline()[1]:
        sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': ERROR - SCRIPT '+script+' ALREADY LAUNCHED.\n')
        sys.stdout.flush()
        sys.exit("ERROR - SCRIPT "+script+" ALREADY LAUNCHED.\n")

sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': INFO - SCRIPT '+scirpt+' NOT RUNNING.\n')
sys.stdout.flush()
sys.exit(0)
