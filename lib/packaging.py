import os
from time import gmtime, localtime, strftime
import hashlib
import tarfile
from yaml import load, dump
import logging as log
from getpass import getuser
from .supplies import Colors, affirm_answ, deny_answ, all_answ
from shutil import rmtree
'''Read the config file and find the source folder'''

configfile = load(open(os.path.expanduser('~')+'/.syncconfig.yaml', 'r'))
sync_source = configfile['syncdir']
hierarchy_status = configfile['hierarchy']


'''MD5 Checksum function'''
def createMD5(fname):

    if os.path.exists('checksum.txt'):
        os.remove('checksum.txt')
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    with open("checksum", 'w' ) as MD5FILE:
        MD5FILE.write(hash_md5.hexdigest())
    return hash_md5.hexdigest()


''' 
Sync classes for peer-to-peer package manipulation
'''

class Package:

    def __init__(self, verbose = True):  # 'verbose' option manipulates output TODO: use 'verbose' functionalty
        self.name = 'sync_tarfile'+strftime("_%d-%m")
        self.source = sync_source

    def pack(self):
        '''Make sure Sync doesn't mess up'''
        if os.path.exists('/tmp/Sync'):
            rmtree('/tmp/Sync')
            os.mkdir('/tmp/Sync')
        else:
            os.mkdir('/tmp/Sync')

        '''Remove existent tarfile if exists'''
        if os.path.exists('/tmp/Sync/'+self.name + '.tar.xz'):
            os.remove('/tmp/Sync/'+self.name + '.tar.xz')
            log.info("Removed previous tarfile: " + '/tmp/Sync/'+self.name + '.tar.xz')

        '''Collect files into a tar'''
        package = tarfile.open(name='/tmp/Sync/'+self.name + '.tar.xz', mode='x:xz')  # Creates a tar in mode for entry
        log.info("Created tarfile: " + package.name)

        hrchcontent = {}  # Content to be written in the hierarchy file
        hrchcount = 1
        with os.scandir(sync_source) as DIR_SCAN:
            for file in DIR_SCAN:
                if not file.name.startswith('.'):
                    try:
                        package.add(file.path, arcname=file.name)
                        hrchcontent[hrchcount] = file.path
                        hrchcount = hrchcount + 1
                        log.info("Added " + file.path + " to package")
                    except Exception as e:
                        log.error('permission denied to '+file.path)

        hrchcontent['username'] = getuser()
        hrchcontent['syncdir'] = sync_source
        with open('/tmp/Sync/hierarchy.yaml', 'w') as hrch:
            dump(hrchcontent, hrch, default_flow_style=False)  # Write content into the hierarchy file
        package.add('/tmp/Sync/hierarchy.yaml', arcname='hierarchy.yaml')
        log.info('Formed hierarchy')
        package.close()  # Close the tar file
        log.info("Closed tarfile: " + package.name)
        createMD5('/tmp/Sync/'+self.name+".tar.xz")
        os.remove('/tmp/Sync/hierarchy.yaml')

    def unpack(self):

        package = tarfile.open(name='/tmp/Sync/'+self.name + '.tar.xz', mode='r:xz')
        log.info("Opened tarfile: " + self.name)
        package.extract('hierarchy.yaml', path='/tmp/Sync')
        hrch = load(open('/tmp/Sync/hierarchy.yaml', 'r'))
        hrchcount = 1

        package.extract('hierarchy.yaml', path='/tmp/Sync/')  # Extracts paths for files in a tarfile
        for pathn in hrch:
            extract_path = hrch['syncdir'].split(hrch['username'])[0]+getuser()+hrch['syncdir'].split(hrch['username'])[1]

            try:
                if pathn not in  ['syncdir', 'username']:
                    package.extract(hrch[pathn], extract_path)
                    log.info("Extracted \'%s\' into %s" % (hrch[pathn], extract_path+'/'))
                    hrchcount+=1
            except:
                log.info('Couldn\'t extract file %s' % hrch[pathn])

        log.info(Colors.OKGREEN+('Done. Extracted %s files' % hrchcount)+Colors.ENDC)

    def list(self):
        with tarfile.open(name='/tmp/Sync/'+self.name + '.tar.xz', mode='r:xz') as package:
            log.info("Contents of: " + self.name)
            package.list(verbose=True)
