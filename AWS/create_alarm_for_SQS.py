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
      print 'create_alarm_for_SQS.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'create_alarm_for_SQS.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
         sys.exit()
      elif opt in ('-p'):
         pattern = arg
      elif opt in ('-P'):
         profile = arg
      elif opt in ('-s'):
         snsarn = arg


   if pattern == '':
      print 'create_alarm_for_SQS.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(1)

   if profile == '':
      print 'create_alarm_for_SQS.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(1)

   if snsarn == '':
      print 'create_alarm_for_SQS.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>'
      sys.exit(1)

   session = boto3.session.Session(profile_name=profile)

   client = session.client('cloudwatch')

   response = client.list_metrics(
   Namespace='AWS/SQS',
   MetricName='ApproximateNumberOfMessagesVisible'
   )

   for metric in response['Metrics']:

	for l in metric["Dimensions"]:	

		if pattern in l["Value"]:

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
   			    MetricName='ApproximateNumberOfMessagesVisible',
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

#   			#DELETE ALARM
#   			response = client.delete_alarms(
#   			    AlarmNames=[
#   			        l["Value"]+': Message in DLQ',
#   			    ]
#   			)
#
   			print "Status of alarm creation for "+l["Value"]+" is "+str(response["ResponseMetadata"]["HTTPStatusCode"])+"."

#   			#DELETE ALARM
#   			print "Status of alarm deletion for "+l["Value"]+" is "+str(response["ResponseMetadata"]["HTTPStatusCode"])+"."
   sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])

