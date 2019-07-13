from time import sleep
from lib import transfer, supplies, packaging
import argparse
import logging as log
import sys

'''
Sync - open-source program to synchronize directories between devices in a secure way
with an option of keeping exact directory paths persistent

v.0.1 - First public release (by lisovskiy01)

TODOs:
Enable encryption
MITM IP protection !
Daemonization !!!
Online synchronization
Frontend(?)
Cleanup all code    
'verbose' option while packing ()
'remove-last' option ()
'''

pkg = packaging.Package()  # Packaging management. See lib/packaging.py

parser = argparse.ArgumentParser(description='Synchronize directories on multiple devices')
parser.add_argument('--change-directory', type=str, default='', help='Change directory to be synced')
parser.add_argument('--open-socket', action='store_true', help='Open socket for connection')
parser.add_argument('--list', action='store_true', help='List files in a found tarfile')
#parser.add_argument('-v', '-verbose', help='Verbosity', action='count')
excl = parser.add_mutually_exclusive_group()
excl.add_argument('--pack', action='store_true', help='Pack the directory in a tarfile (stored in /tmp)')
excl.add_argument('--unpack', action='store_true', help='Unpack a tarfile (stored in /tmp)')
args = parser.parse_args()


if args.change_directory:
    supplies.changeDir(args.change_directory)
elif args.pack:
    pkg.pack()
elif args.unpack:
    pkg.unpack()
elif args.open_socket:
    transfer = transfer.Socket('sync_tarfile')
    transfer.send()
elif args.list:
    pkg.list()


