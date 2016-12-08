# TOOLS

My useful tools.

## AWS

- **_AWS-FindIAMUserByAccesskey.bash_**

This script allows you to retrieve the IAM user that owns the accesskeys sent as arguments.
It take its credentials from ~/.aws directory.

```
AWS-FindIAMUserByAccesskey.bash -p profile[,profile,...] -a accesskey[,accesskey,...] [-h] -- program to search IAM user associate to an accesskey

where:
    -p  AWS profiles to use (DEFAULT=default). It means the AWS account to search in.
    -a  Accesskeys to search.
    -h  This help.
```
- **_create_alarm_for_SQS.py_**

This take two arguments, an AWS Profile and an SNS ARN.
It allow to create alarm on SQS's pattern when a message is received.

```
create_alarm_for_SQS.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>

<pattern> is the pattern that must be found in SQS name
<AWS_profile> is the profile name for AWS API Calls
<SNS_ARN> is the SNS's ARN used to notify in case of Alarm or OK state.
```

## PAGERDUTY

- **_PD-ListIntegrationKeys.py_**

This script allows you to extract all the Integration Keys from the Pagerduty account associated with the token in argument.

```
PD-ListIntegrationKeys.py -t <token>
```

## RUNDECK

- **_RDK-PagerDutyNotification.groovy_**

This plugin allows you to send notifications from Rundeck to a Pagerduty service.

```
/var/lib/rundeck/libext/PagerDutyNotification.groovy
```

You have to copy this plugin to **/var/lib/rundeck/libext/** and remove **"RDK_"** from the name of the plugin.

It's a fork of [pagerduty-notification](https://github.com/rundeck-plugins/pagerduty-notification).

Now with this version you can and must specify the Integration Key in each job (with a default value you have to modify in the plugin).

You also have in the default notification Title the link to the execution at the origin of the call.

- **_RDK-purge_ng.py_**

This script purge executions with completed time older than RETENTION variable.

```
./purge_ng.py -a <api_key> -r <http://FQDN_rundeck_server> -p <port_rundeck_server> -P <project> -R <days_of_retention> -l <lenght_of_batch>'
```

You have to copy this script on your Rundeck server(s) (remove RDK_).
You have to configure these variable:

°API_KEY

°RUNDECKSERVER

°RUNDECKPORT

°PROJECT

°RETENTION

°LOT

And create a job to launch this script only on one server.
You can create previously a job to check current purge running that won't permit purge launched.

- **_GLOBAL-check_script_presence.py_**

This script check that script in argument is currently running or not.

```
./check_script_presence.py -s <script>
```

You have to copy this script on your Rundeck server(s).

Example of use in Rundeck:

Create a job that launched this script on ALL Rundeck servers.

Use this newly created job first step in the Rundeck Purge Executions job.

- **_RDK-backup_rundeck_ng.py_**

This script backup jobs definitions per project and configuration files (/etc/rundeck/ & /var/rundeck/) in a TAR.GZ compressed archive and send it to S3.

A token with good permission is mandatory.

```
./backup_rundeck_ng.py -t <token> -p <profile> -b <bucket>
```

You have to copy this script on your Rundeck server(s) without RDK_.
Create a job that launched this script on only ONE Rundeck server once a day.
