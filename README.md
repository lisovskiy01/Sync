# sync
A python-written program for Linux that automatically synchronizes directories between devices. Like cloud, but without clouds.

## How is it
Sync creaes a tarfile with files and sends it another device, where client-Sync unpacks it and extracts the files to same directories where they were on the first device.
```
'/home/foo/Desktop/Report.docx' packed into a 'sync_tarfile_xx-xx.tar.xz'
remote IP read from config
tarfile sent to this IP
tarfile recieved
tarfile unpacked
'Report.docx' extracted into '/home/bar/Desktop/Report.docx'
```

## Requirements
python
Linux machine

## Install
run ```python3 install.py``` to set up base config

## Usage
```python3 sync.py --pack``` - to create a tarfile

```python3 sync.py --unpack``` - to unpack and extract files from a tarfile

```python3 sync.py --list``` - to list files in a tarfile

```python3 sync.py --open-socket``` - to create a socket (NOT TESTED AND PROBABLY NOT WORKING)

## Future
Sync is in early stages of development, so any help and contributions would be great

## Built With
My ass and Python
