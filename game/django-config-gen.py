import argparse
import json

parser = argparse.ArgumentParser(description='Configurate django.')
parser.add_argument('--allowed_hosts',
                    metavar='allowed_hosts',
                    type = str,
                    nargs = '+',
                    required = True,
                    help='game host name')

args = parser.parse_args()

hosts_string = "','".join(args.allowed_hosts)

config = "ALLOWED_HOSTS = ['{}']".format(hosts_string)

with open('autoconfig.py', 'w+') as f:
    f.write(config)
