#!/usr/bin/python

import requests, json
import sys, getopt

def main(argv):
   token = ''
   try:
      opts, args = getopt.getopt(argv,"ht:",["help","token="])
   except getopt.GetoptError:
      print 'PD-ListIntegrationKeys.py -t <token>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'PD-ListIntegrationKeys.py -t <token>'
         sys.exit()
      elif opt in ("-t", "--token"):
         token = arg

   if token == '':
      print 'PD-ListIntegrationKeys.py -t <token>'
      sys.exit(1)


   urlServices = 'https://api.pagerduty.com/services?time_zone=UTC&sort_by=name'
   headers = { "Accept": "application/vnd.pagerduty+json;version=2", "Authorization": "Token token=" + token + "" }
   responseServices = requests.get(urlServices, headers=headers)
   
   ListServices = responseServices.json()
   
   for service in ListServices['services']:
      
      for integration in service["integrations"]:
   
         if integration["type"] != u"generic_events_api_inbound_integration_reference" and integration["type"] != u"event_transformer_api_inbound_integration_reference":
            continue
         
         urlIntegration =  'https://api.pagerduty.com/services/' + service["id"] +'/integrations/' + integration["id"]
         responseIntegrations = requests.get(urlIntegration, headers=headers)
   
         Integration = responseIntegrations.json()
         
         print "Service Name: " + service["name"] + "\n   Integration Key: " + Integration["integration"]["integration_key"]

   sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])

