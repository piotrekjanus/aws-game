#!/bin/bash
  
srv_name='gameserver'
cfg_file='gameserver'

yes n | eb init $srv_name > /dev/null
eb create --cfg $cfg_file "${srv_name}-env"
url=`aws elasticbeanstalk describe-environments --no-include-deleted --environment-names "${srv_name}-env" \
    --query "Environments[*].CNAME" --output text`
# Add game server url to django server config
cd ../game && \
python3 config-gen.py --game_host "$url" &&\
cd ../game-server
echo "Server \"${srv_name}\" URL: $url"

