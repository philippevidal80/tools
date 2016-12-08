#!/usr/bin/env python

import requests
import json
import sys
import getopt
import time
import sys
import xml.etree.ElementTree as ET
import tarfile
import boto3
import os
import logging

def main(argv):

   token = ''
   bucket = ''
   profile = ''

   

   try:
      opts, args = getopt.getopt(argv,"ht:p:b:",["help","token=","profile=","bucket="])
   except getopt.GetoptError:
      print 'backup_rundeck_ng.py.py -t <token> -p <profile> -b <bucket>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'backup_rundeck_ng.py.py -t <token> -p <profile> -b <bucket>'
         sys.exit()
      elif opt in ("-t", "--token"):
         token = arg
      elif opt in ("-p", "--profile"):
         profile = arg
      elif opt in ("-b", "--bucket"):
         bucket = arg

   if token == '':
      print 'backup_rundeck_ng.py.py -t <token> -p <profile> -b <bucket>'
      sys.exit(1)

   if profile == '':
      print 'backup_rundeck_ng.py.py -t <token> -p <profile> -b <bucket>'
      sys.exit(1)

   if bucket == '':
      print 'backup_rundeck_ng.py.py -t <token> -p <profile> -b <bucket>'
      sys.exit(1)

   requests.packages.urllib3.disable_warnings()
   session = boto3.Session(profile_name=profile)

   logging.basicConfig(filename='/var/log/rundeck/rundeck.backup.log.'+time.strftime("%Y-%m-%d"), level=logging.INFO)
   logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': BACKUP LAUNCHED.')
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': BACKUP LAUNCHED.\n')
   sys.stdout.flush()


   filenametar = u"rundeck_"+time.strftime("%Y-%m-%d")+".tar.gz"

   logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': TAR file '+filenametar+' creation...')
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': TAR file '+filenametar+' creation...\n')
   sys.stdout.flush()

   with tarfile.open(filenametar, "w:gz") as tar:
   
      logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': Found and list Projects...')
      sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': Found and list Projects...\n')
      sys.stdout.flush()

      urlProjects = 'https://localhost:8443/api/1/projects'
      headers = { "Accept": "application/json", "X-RunDeck-Auth-Token": str(token) }
      responseProjects = requests.get(urlProjects, headers=headers, verify=False)
      
      ListProjects = responseProjects.json()
   
      # DEBUG
      #print(json.dumps(ListProjects, sort_keys=True, indent=4))
      
      logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': Creation of Jobs lists...')
      sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': Creation of Jobs lists...\n')
      sys.stdout.flush()

      for project in ListProjects:
   
         urlJobs = "https://localhost:8443/api/14/project/"+project['name']+"/jobs"
         headers = { "Accept": "application/json", "X-RunDeck-Auth-Token": str(token) }
         responseJobs = requests.get(urlJobs, headers=headers, verify=False)
         
         listJobs = responseJobs.json()

         filename = u"rundeck_"+project['name']+"_jobs_definition_"+time.strftime("%Y-%m-%d")+".xml"
   
         logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': XML '+project['name']+' Jobs Definitions file in progress...')
         sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': XML '+project['name']+' Jobs Definitions file in progress...\n')
         sys.stdout.flush()

         with open(filename, "w") as definitionsFile:
      
            # DEBUG
            #print json.dumps(listJobs, sort_keys=True, indent=4)
            
            xml = ET.Element('joblist')
            doc = ET.ElementTree(xml)
            
            for job in listJobs:
               
               urlJob = "https://localhost:8443/api/1/job/"+job['id']+""
               headers = { "Accept": "application/xml", "X-RunDeck-Auth-Token": str(token) }
               responseJob = requests.get(urlJob, headers=headers, verify=False)
      
   
               job = ET.fromstring(responseJob.text.encode('utf-8'))
               
               #DEUG
               #print job
   
               for item in job.findall('job'):
   
                 jobelement = xml.append(item)
   
            doc.write(definitionsFile)
         
         logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': Add XML file to tar archive...')
         sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': Add XML file to tar archive...\n')
         sys.stdout.flush()

         tar.add(filename, arcname="/tmp/"+filename)
         os.remove(filename)

      logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': Add Rundeck configurations files (/etc/rundeck/ & /var/rundeck/)...')
      sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': Add Rundeck configurations files (/etc/rundeck/ & /var/rundeck/)...\n')
      sys.stdout.flush()
   
      tar.add("/etc/rundeck", recursive=True)   
      tar.add("/var/rundeck", recursive=True)

   s3 = session.resource('s3')
 
   currentbucket = s3.Bucket(bucket)
   exists = True

   logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': Send tar file '+filenametar+' to AWS S3 bucket: '+bucket+'.')
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': Send tar file '+filenametar+' to AWS S3 bucket: '+bucket+'.\n')
   sys.stdout.flush()

   try:
      s3.Object(bucket, filenametar  ).put(Body=open(filenametar, 'rb'))
    
   except botocore.exceptions.ClientError as e:
      # If a client error is thrown, then check that it was a 404 error.
      # If it was a 404 error, then the bucket does not exist.
      error_code = int(e.response['Error']['Code'])
      if error_code == 404:
          exists = False
          logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': ERROR WITH AWS S3.')
          sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': ERROR WITH AWS S3.\n')
          sys.stdout.flush()

   
   os.remove(filenametar) 

   logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': END OF BACKUP.')
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': END OF BACKUP.\n')
   sys.stdout.flush()

   sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])

