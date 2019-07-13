import os
import sys
import yaml
from getpass import getuser
import logging as log

'''
Miscellaneous stuff for Sync to use
'''

affirm_answ = ['y', 'Y', 'yes', 'Yes']
deny_answ = ['all', 'a']
all_answ = ['n', 'N', 'no', 'No']

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

userhome = os.path.expanduser('~')

'''Connectivity check'''
def ping(ip):
    if not sys.platform.startswith('win'):
        pingarg = ' -c 1'
    else:
        pingarg = ' -n 1'
    command = ('ping '+ip+pingarg+' >> /dev/null')
    if os.system(command) == 0:
        return True
    else:
        return False

'''Change directory for syncing in ~/.syncconfig.yaml'''
def changeDir(dir):
    if dir.startswith('~'):
        syncpath = os.path.expanduser('~') + dir.split('~')[1]  # Changes '~' to user's /home
    else:
        syncpath = dir
    while syncpath.startswith(os.path.expanduser('~')) is False:
        print(Colors.WARNING+'You are only allowed to sync files in your home'+Colors.ENDC)
        newdir = input('Enter new directory: ')
        changeDir(newdir)
        return
    while os.path.exists(syncpath) is False:
        print(Colors.WARNING+'Error: directory doesn\'t exist'+Colors.ENDC)
        newdir = input('Enter new directory: ')
        changeDir(newdir)
        return
    with open(os.path.expanduser('~')+'/.syncconfig.yaml', 'r') as configfile:
        config = yaml.load(configfile)
    with open(os.path.expanduser('~')+'/.syncconfig.yaml', 'w') as configfile:
        config['syncdir'] = syncpath
        yaml.dump(config, configfile, default_flow_style=False)
    print('Changed directory to %s' % config['syncdir'])


