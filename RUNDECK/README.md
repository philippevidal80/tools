## RUNDECK

- **_PagerDutyNotification.groovy_**

This plugin allows you to send notifications from Rundeck to a Pagerduty service.

```
/var/lib/rundeck/libext/PagerDutyNotification.groovy
```

You have to copy this plugin to **/var/lib/rundeck/libext/**.

It's a fork of [pagerduty-notification](https://github.com/rundeck-plugins/pagerduty-notification).

Now with this version you can and must specify the Integration Key in each job (with a default value you have to modify in the plugin).

You also have in the default notification Title the link to the execution at the origin of the call.

- **_purge_ng.py_**

This script purge executions with completed time older than RETENTION variable.

```
./purge_ng.py -a <api_key> -r <http://FQDN_rundeck_server> -p <port_rundeck_server> -P <project> -R <days_of_retention> -l <lenght_of_batch>'
```

You have to copy this script on your Rundeck server(s).
You have to configure these variable:

°API_KEY

°RUNDECKSERVER

°RUNDECKPORT

°PROJECT

°RETENTION

°LOT

And create a job to launch this script only on one server.
You can create previously a job to check current purge running that won't permit purge launched.

- **_check_script_presence.py_**

This script check that script in argument is currently running or not.

```
./check_script_presence.py -s <script>
```

You have to copy this script on your Rundeck server(s).

Example of use in Rundeck:

Create a job that launched this script on ALL Rundeck servers.

Use this newly created job first step in the Rundeck Purge Executions job.

- **_backup_rundeck_ng.py_**

This script backup jobs definitions per project and configuration files (/etc/rundeck/ & /var/rundeck/) in a TAR.GZ compressed archive and send it to S3.

A token with good permission is mandatory.

```
./backup_rundeck_ng.py -t <token> -p <profile> -b <bucket>
```

You have to copy this script on your Rundeck server(s).
Create a job that launched this script on only ONE Rundeck server once a day.

