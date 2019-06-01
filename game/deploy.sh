#!/bin/bash
  
srv_name='djangoserver-test-remove'
cfg_file='djangosrv'

yes n | eb init $srv_name > /dev/null
#TODO: timeout 1 is debug only
eb create --cfg $cfg_file --timeout 1 "${srv_name}-env"
url=`aws elasticbeanstalk describe-environments --no-include-deleted --environment-names "${srv_name}-env" \
    --query "Environments[*].CNAME" --output text`

status=`aws elasticbeanstalk describe-environments --no-include-deleted --environment-names "${srv_name}-env" \
    --query "Environments[*].status" --output text`
counter=0
max_loops=60
while [ "$status" != "Ready" ] && [ "$counter" -lt "$max_loops" ]; do
    echo $counter #TODO: debug only
    sleep 30
    counter=$((counter+1))
    status=`aws elasticbeanstalk describe-environments --no-include-deleted --environment-names "${srv_name}-env" \
    --query "Environments[*].status" --output text`
done

if [ "$counter" -eq "$max_loops" ]; then
    echo "Timeout! Enviroment creation failed"
else
    #TODO: update urls and call ed deploy
    echo "Server \"${srv_name}\" URL: $url"
fi


