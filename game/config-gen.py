import argparse
import json

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--game_host',
                    metavar='game_host',
                    type = str,
                    required = True,
                    help='game host name')

parser.add_argument('--game_port',
                    metavar='game_port',
                    type = int,
                    required = True,
                    help='game port name')

args = parser.parse_args()

# write config
config = { 'game_host' : '{}:{}'.format(args.game_host, args.game_port)}

config_content = 'var config = ' + json.dumps(config) + ';'
with open('static/config/config.js', 'w+') as f:
    f.write(config_content)


config = "ALLOWED_HOSTS = ['{}','localhost']".format(args.game_host)

with open('autoconfig.py', 'w+') as f:
    f.write(config)
