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


