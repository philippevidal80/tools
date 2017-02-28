#!/bin/bash
#
# Requirements:
# - Need at least awscli (1.10.59)
#
# Description:
#   It allows you to vendor a list of profiles and accesskeys and search for matches.
#

# HELP

usage="$(basename "$0") -p profile[,profile,...] -a accesskey[,accesskey,...] [-h] -- program to search IAM user associate to an accesskey

where:
    -p  AWS profiles to use (DEFAULT=default). It means the AWS account(s) to search in. Commat separated.
    -a  Accesskeys to search. Commat separated.
    -l  List profiles
    -h  This help."

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:

profile="default"
accesskey=""
p_flag=0
a_flag=0
user=""
check=""
found=0
remainingkey=()
tempkey=()
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

# Manage options

if [[ ! $@ =~ ^\-.+ ]]
then
  echo "Missing arguments."
  echo "$usage"
  exit 1
fi

while getopts ':p:a:lh' option; do
  case "$option" in
    h) echo "$usage"
       exit 0
       ;;
    p) set -f
       IFS=,
       profile=($OPTARG)
       p_flag=1
       ;;
    a) set -f
       IFS=,
       accesskey=($OPTARG)
       a_flag=1
       ;;
    l) echo -e "User list of profile configured:\n"
       awk '{if ($0 ~ /^\[/ ) print $0}' ~/.aws/credentials | sed 's/\[//g;s/\]//g'
       exit 0
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

# Check that both profile and accesskey switches are in-use.

if [ ! $p_flag == 1 ] || [ ! $a_flag == 1 ]
then
  echo "$usage"
  exit 1
fi

# START.

remainingkey=("${accesskey[@]}")
list_check=()

echo ""
echo "SEARCH STARTED..."
echo ""
echo " * List of matching accesskey(s):"
echo ""

for i in "${profile[@]}"
do
  tempkey=()
  user=`aws --output text iam list-users --profile $i | awk '{print $NF}' | xargs -P10 -n1 aws --output text iam list-access-keys --user-name --profile $i`
  
  for j in "${remainingkey[@]}"
  do
    for k in "$user"
    do
      check=`echo -n $k | awk -v key=$j '{ if ($2 == key) print $5 }'`
      if [ "$check" == "" ]
      then
        tempkey+=($j)
        continue
      else
        found=1
	list_check+=($check)
        echo " We found that accesskey ${green}$j${reset} is linked to user ${red}$check${reset} from account profile ${green}$i${reset}."
      fi
    done
  done
  remainingkey=("${tempkey[@]}")
done

echo ""
echo " * List of non-matching accesskey(s):"
echo ""

if [ $found == 0 ]
then
  echo " Accesskey(s) ${green}${accesskey[@]}${reset} not linked with any IAM user from account profile in ${green}${profile[@]}${reset}."
  echo ""
  echo " ${red}BE CAREFUL, AWS root user is not checked and cannot be.${reset}"
  exit 1
elif [ ${#remainingkey[@]} -ne 0 ]; then
  echo " Accesskey(s) ${green}${remainingkey[@]}${reset} not linked with any IAM user from account profile in ${green}${profile[@]}${reset}."
  echo ""
  echo " ${red}BE CAREFUL, AWS root user is not checked and cannot be.${reset}"
fi

echo ""
echo " * List of accounts that match at least one of provided accesskey(s):"
echo ""

if [[ $list_check[@] == "" ]]
then
  echo " No match found."
else
	echo " List of user(s) found corresponding with input accesskey(s): ${green}${list_check[@]}${reset}."
fi

echo ""
echo "SEARCH ENDED."
echo ""

exit 0
