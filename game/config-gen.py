import argparse
import json

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--game_host',
                    metavar='game_host',
                    type = str,
                    required = True,
                    help='game host name')

args = parser.parse_args()

config = { 'game_host' : args.game_host}
config_content = 'var config = ' + json.dumps(config) + ';'
with open('static/config/config.js', 'w+') as f:
    f.write(config_content)
