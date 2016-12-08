#!/usr/bin/env python

import requests
import json
import sys
import getopt
import boto3

def main(argv):

   pattern = ''
   profile = ''
   snsarn = ''

   try:
      opts, args = getopt.getopt(argv,"hp:P:s:",["help"])
   except getopt.GetoptError:
      print 'create_alarm_for_SQS_DLQ.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'create_alarm_for_SQS_DLQ.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
         sys.exit()
      elif opt in ('-p'):
         pattern = arg
      elif opt in ('-P'):
         profile = arg
      elif opt in ('-s'):
         snsarn = arg


   if pattern == '':
      print 'create_alarm_for_SQS_DLQ.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(1)

   if profile == '':
      print 'create_alarm_for_SQS_DLQ.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(1)

   if snsarn == '':
      print 'create_alarm_for_SQS_DLQ.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(1)

   session = boto3.session.Session(profile_name=profile)

   client = session.client('cloudwatch')

   response = client.list_metrics(
   Namespace='AWS/SQS',
   MetricName='NumberOfMessagesReceived'
   )

   for metric in response['Metrics']:

	for l in metric["Dimensions"]:	

		if "dlq" in l["Value"]:

   			response = client.put_metric_alarm(
   			    AlarmName=l["Value"]+': Message in DLQ',
   			    AlarmDescription='There is message in DLQ.',
   			    ActionsEnabled=True,
   			    OKActions=[
   			        snsarn,
   			    ],
   			    AlarmActions=[
   			        snsarn,
   			    ],
                            Statistic='Average',
   			    MetricName='NumberOfMessagesReceived',
   			    Namespace='AWS/SQS',
   			    Dimensions=[
   			        {
   			            'Name': l["Name"],
   			            'Value': l["Value"]
   			        },
   			    ],
   			    Period=300,
   			    EvaluationPeriods=1,
   			    Unit='Count',
   			    Threshold=0,
   			    ComparisonOperator='GreaterThanThreshold'
   			)	

   sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])

