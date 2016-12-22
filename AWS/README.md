## AWS

- **_findIAMUserByAccesskey.bash_**

This script allows you to retrieve the IAM user that owns the accesskeys sent as arguments.
It take its credentials from ~/.aws directory.

```
findIAMUserByAccesskey.bash -p profile[,profile,...] -a accesskey[,accesskey,...] [-h] -- program to search IAM user associate to an accesskey

where:
    -p  AWS profiles to use (DEFAULT=default). It means the AWS account to search in.
    -a  Accesskeys to search.
    -h  This help.
```
- **_create_alarm_for_SQS.py_**

This take three arguments, a pattern, an AWS Profile and a SNS ARN.
It allow to create alarm on SQS's pattern when a message is visible.

```
create_alarm_for_SQS.py -p <pattern> -P <AWS_profile> -s <SNS_ARN>

<pattern> is the pattern that must be found in SQS name
<AWS_profile> is the profile name for AWS API Calls
<SNS_ARN> is the SNS's ARN used to notify in case of Alarm or OK state.
```


