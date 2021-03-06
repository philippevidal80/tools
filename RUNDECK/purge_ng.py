#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET
import time
import sys
import logging
import getopt

def main(argv):
   
   API_KEY=''
   RUNDECKSERVER=''
   RUNDECKPORT=''
   PROJECT=''
   RETENTION='' #days
   LOT=''

   try:
      opts, args = getopt.getopt(argv,"ha:r:p:P:R:l:",["help","apikey=","rundeckserver=","rundeckport=","project=","retention=","lenghtbatch="])
   except getopt.GetoptError:
      print 'purge_ng.py -a <api_key> -r <http://FQDN_rundeck_server> -p <port_rundeck_server> -P <project> -R <days_of_retention> -l <lenght_of_batch>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'purge_ng.py -a <api_key> -r <http://FQDN_rundeck_server> -p <port_rundeck_server> -P <project> -R <days_of_retention> -l <lenght_of_batch>'
         sys.exit()
      elif opt in ("-a", "--apikey"):
         API_KEY = arg
      elif opt in ("-r", "--rundeckserver"):
         RUNDECKSERVER = arg
      elif opt in ("-p", "--rundeckport"):
         RUNDECKPORT = arg
      elif opt in ("-P", "--project"):
         PROJECT = arg
      elif opt in ("-R", "--retention"):
         RETENTION = arg
      elif opt in ("-l", "--lenghtbatch"):
         LOT = arg

   if (API_KEY == '') or (RUNDECKSERVER == '') or (RUNDECKPORT == '') or (PROJECT == '') or (RETENTION == '') or (LOT == ''):
      print 'purge_ng.py -a <api_key> -r <http://FQDN_rundeck_server> -p <port_rundeck_server> -P <project> -R <days_of_retention> -l <lenght_of_batch>'
      sys.exit(1)

   requests.packages.urllib3.disable_warnings()

   def deleteExecution(executions_id):
       url =  RUNDECKSERVER +':'+RUNDECKPORT+'/api/12/executions/delete?ids='+executions_id
       headers = {'X-RunDeck-Auth-Token': API_KEY }
       r = requests.post(url, headers=headers, verify=False)    
       return r
   
   def listExecutionsToDelete():
       url =  RUNDECKSERVER +':'+RUNDECKPORT+'/api/14/project/'+PROJECT+'/executions'
       playload = {'max': LOT, 'count': LOT, 'olderFilter': RETENTION+'d'}
       headers = {'X-RunDeck-Auth-Token': API_KEY }
       r = requests.post(url, headers=headers, params=playload, verify=False)
       return r.text.encode('utf-8')
   
   # Just for test.
   #time.sleep(600)
   
   logging.basicConfig(filename='/var/log/rundeck/rundeck.purge.execution.log.'+time.strftime("%Y-%m-%d"), level=logging.INFO)
   
   logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': PURGE LAUNCHED.')
   logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': Batch of '+LOT+' executions to be deleted if completed time is over '+RETENTION+' days.')
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': PURGE LAUNCHED.\n')
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': Batch of '+LOT+' executions to be deleted if completed time is over '+RETENTION+' days.\n')
   sys.stdout.flush()
   
   while 'true':
       ids = ""
       listToDelete = listExecutionsToDelete()
       root = ET.fromstring(listToDelete)
       count = root.get('count')
           
       if count == LOT:
           for execution in root:
               ids = ids + "," + execution.get('id')
       else:
           logging.error(time.strftime("%Y/%m/%d-%H:%M:%S")+': ERROR. LESS THAN '+LOT+' EXECUTIONS THAT CAN BE DELETED FOUND.')
           sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': ERROR. LESS THAN '+LOT+' EXECUTIONS THAT CAN BE DELETED FOUND.\n')
           sys.stdout.flush()
           sys.stderr.write("No more executions to delete. End of purge")
           sys.exit(0)
   
       ids = ids[1:]
       logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': List of Executions to be deleted: '+ids)
       sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': List of Executions to be deleted: '+ids+'\n')
       sys.stdout.flush()
       r = deleteExecution(ids)
       logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+":    Response : "+str(r.status_code)+" "+r.text.encode('utf-8'))
       sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+":    Response : "+str(r.status_code)+" "+r.text.encode('utf-8')+"\n")
       sys.stdout.flush()
   
   logging.info(time.strftime("%Y/%m/%d-%H:%M:%S")+': FIN DE LA PURGE.')
   sys.stdout.write(time.strftime("%Y/%m/%d-%H:%M:%S")+': FIN DE LA PURGE.\n')
   sys.stdout.flush()

if __name__ == "__main__":
   main(sys.argv[1:])
