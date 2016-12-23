#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import getopt
import boto3
import requests

def main(argv):

   conffile=''
   syslogdir=''
   profile=''
   bucketlog=''

   try:
      opts, args = getopt.getopt(argv,"hc:s:p:b:",["help","conffile=","syslogdir=","profile=","bucketlog="])
   except getopt.GetoptError:
      print 'purge_local.py -c <conffile> -s <syslogdir> -p <profile> -b <bucketlog>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'purge_local.py -c <conffile> -s <syslogdir> -p <profile> -b <bucketlog>'
         sys.exit(1)
      elif opt in ("-c", "--conffile"):
         conffile = arg
      elif opt in ("-s", "--syslogdir"):
         syslogdir = arg
      elif opt in ("-p", "--profile"):
         profile = arg
      elif opt in ("-b", "--bucketlog"):
         bucketlog = arg

   if (conffile == '') or (syslogdir == '') or (profile == '') or (bucketlog == ''):
      print 'purge_local.py -c <conffile> -s <syslogdir> -p <profile> -b <bucketlog>'
      sys.exit(1)
  
   def getinstanceID():
       url =  'http://169.254.169.254/latest/meta-data/instance-id'
       r = requests.get(url)
       return r.text.encode('utf-8')
 
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': Begin local purge\n')
   sys.stdout.flush()
  
   try: 
      with open(conffile) as rdk:
      
          now = time.time()
      
          for line in rdk:
              line = line.split('=')
              line[0] = line[0].strip()
              if line[0] == 'rdeck.base':
                  rdeckbase = re.sub(r'[]\[\' ]','', line[1].strip()).split(',')
      
          try:
             dirtopurge=rdeckbase[0] + '/logs/rundeck'
          except:
             print("ERROR: No rdeck.base variable found in configuration file provided.")
             sys.exit(1)
   
          for root, dirs, files in os.walk(dirtopurge, topdown=False):
              for name in files:
                  if os.stat(os.path.join(root, name)).st_mtime < now - 60:
                     os.remove(os.path.join(root, name))
                     sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': File '+os.path.join(root, name)+' has been deleted.\n')
                     sys.stdout.flush()
      
   except IOError:
      print("ERROR: File "+conffile+" not found.")
      sys.exit(1)

   try:
      session = boto3.Session(profile_name=profile)
      s3 = session.client('s3')
   
      for root, dirs, files in os.walk(syslogdir, topdown=False):
         for name in files:
            if not re.search("^.*log$", name):
               with open(os.path.join(root, name), 'rb') as data:
                  s3.upload_fileobj(data, bucketlog, getinstanceID()+'/'+name)
               os.remove(os.path.join(root, name))
               sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': File '+os.path.join(root, name)+' has been copied to S3 bucket '+bucketlog+'/'+getinstanceID()+' and deleted from local system.\n')
   except:
      print("ERROR: Issue with local system log files purge.")
      sys.exit(1)

   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': End local purge\n')
   sys.stdout.flush()
   
   sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])

