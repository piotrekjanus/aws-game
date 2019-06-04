#!/bin/bash
  
srv_name='zatackaserverpostgress'
cfg_file='djangosrv'

yes n | eb init $srv_name > /dev/null
eb create --cfg $cfg_file "${srv_name}-env"
url=`aws elasticbeanstalk describe-environments --no-include-deleted --environment-names "${srv_name}-env" \
    --query "Environments[*].CNAME" --output text`

status=`aws elasticbeanstalk describe-environments --no-include-deleted --environment-names "${srv_name}-env" \
    --query "Environments[*].status" --output text`
counter=0
max_loops=60
while [ "$status" != "Ready" ] && [ "$counter" -lt "$max_loops" ]; do
    sleep 30
    counter=$((counter+1))
    status=`aws elasticbeanstalk describe-environments --no-include-deleted --environment-names "${srv_name}-env" \
    --query "Environments[*].status" --output text`
done

if [ "$counter" -eq "$max_loops" ]; then
    echo "Timeout! Enviroment creation failed"
else
    python3 django-config-gen.py --allowed_hosts "$url"
    eb deploy #deploy once more to update ALLOWED HOSTS
    echo "Server \"${srv_name}\" URL: $url"
fi


