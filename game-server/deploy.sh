#!/bin/bash
  
yes n | eb init
eb create --cfg gameserver gameserver-dev
url=`aws elasticbeanstalk describe-environments --environment-names front-env \
    --query "Environments[*].CNAME" --output text`
echo "\nGameserver URL: $url"

