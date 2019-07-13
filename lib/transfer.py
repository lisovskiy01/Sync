import os
import logging as log
import socket
from yaml import load
from time import gmtime, localtime, strftime
import ssl  # Will be used in future
import sys
from .supplies import Colors as color

'''Read the config file and find the client IP'''
config = load(open(os.path.expanduser('~')+'/.syncconfig.yaml', 'r'))
remotehost = config["remote-host"]  # Take IP from config file
localhost = config["local-host-name"]  # Local machine's hostname
port = config["port"]  # Take port from config file
maxconnections = config["max-connections"]  # Maximum allowed connections


class Socket:

    def __init__(self, packagename):
        self.packagename = '/tmp/Sync/'+packagename+strftime("_%d-%m")+'.tar.xz'  # Package name with date and extension

        self.sock = socket.socket()
        print("Created socket")
        self.sock.bind((localhost, port))
        self.sock.listen(maxconnections)
        print("Listening on socket")

    def send(self):
        tarfile = self.packagename
        tarfilesize = os.path.getsize('/tmp/Sync/'+tarfile)
        print("File size: %s" % tarfilesize)

        while True:
            conn, adrr = self.sock.accept()  # Prepared socket for listening by default
            print(color.OKBLUE+"Socket connected and ready at %s:%s"+color.ENDC % (adrr, port))
            data = conn.recv(1024)
            print(color.OKGREEN+"Received: %s"+color.ENDC % repr(data))

            file = open(tarfile, 'rb')
            encodedfile = file.read(1024)
            while(encodedfile):
                conn.send(encodedfile)
                print('Send %s' % repr(encodedfile))
                encodedfile = file.read(1024)
            file.close()

            print("Done sending \'%s\'" % tarfile)
            conn.send("Transfer finished, server passing to receiver mode.")
            conn.close()
            self.__init__(packagename='')

    def receive(self):
        self.host = remotehost
        self.sock.connect((self.host, port))
        self.sock.send("Hello, server!")

        with open(self.packagename, 'wb') as file:
            print(color.WARNING+"Created tarfile"+color.ENDC)
            while True:
                print(color.WARNING+"Receive open"+color.ENDC)
                data = self.sock.recv(1024)
                print('data=%s' % (data))
                if not data:
                    break
                file.write(data)
            print(color.OKGREEN+"Tarfile transfer finished"+color.ENDC)
            print(color.WARNING+"Receiving checksum"+color.ENDC)

        file.close()
        print(color.OKGREEN+"Done receiving \'%s\'"+color.ENDC % self.packagename)
        self.sock.close()
        print(color.OKBLUE+"Transfer finished, server falling back to receiver mode."+color.ENDC)