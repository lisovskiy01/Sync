import os
import yaml
import logging as log
import sys
from shutil import copyfile
from lib import supplies

color = supplies.Colors()  # Colors for text

'''Initial config'''
baseconfig = {
    "logdir": "/var/log/",
    "logging": False,
    "encryption": False,
    "hierarchy": True,
    "prompt-when-request": False,
    "key-protection": False,
    "local-host-name": "localhost",
    "port": 9999,
    "max-connections": 2
}

print(color.WARNING + "Starting installer..." + color.ENDC)

'''Remove existent config file'''
if os.path.exists('config.yaml'):
    os.remove('config.yaml')
    log.info('Removed config file in install directory')
if os.path.exists(os.path.expanduser('~')+'/.syncconfig.yaml'):
    os.remove(os.path.expanduser('~')+'/.syncconfig.yaml')
    log.warning('Removed existent config file')

'''Prompt for necessary settings'''
def setSyncFolder():
    syncpath = input('Enter folder to be synced: ')
    while syncpath == '':
        setSyncFolder()
        return
    if syncpath.startswith('~'):
       syncpath = os.path.expanduser('~')+syncpath.split('~')[1]  # Changes '~' to user's /home
       print(syncpath)
    while syncpath.startswith(os.path.expanduser('~')) is False:
        print(supplies.Colors.WARNING+'You are only allowed to sync files in your home'+supplies.Colors.ENDC)
        newdir = input('Enter new directory: ')
        supplies.changeDir(newdir)
        return
    log.info("Set syncdir to: %s" % syncpath)
    baseconfig['syncdir'] = syncpath
setSyncFolder()


def getRemoteIP():
    global remoteip
    remoteip = input("Enter remote client IP: ")
    while remoteip == '':
        getRemoteIP()
    if supplies.ping(remoteip) is True:  # Checks if IP is online. See lib/supplies.py
        baseconfig['remote-host'] = remoteip
        print('Set %s as remote client' % remoteip)
    else:
        log.exception('Client not found. Check IP and connection and try again.')
        getRemoteIP()
getRemoteIP()

'''Write config data to a file'''
with open('config.yaml', 'w') as configfile:
    yaml.dump(baseconfig, configfile, default_flow_style=False)
'''Save config file'''
try:
    copyfile('config.yaml', os.path.expanduser('~')+'/.syncconfig.yaml')
    log.info('Saved config file at \'~/.syncconfig.yaml\'')
except:
    log.critical('could save the config file. Try copying \'config.yaml\' to home directory manually')

print('Installation finished')
