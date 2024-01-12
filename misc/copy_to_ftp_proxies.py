'''
exec:
python

params:
"/mnt/path/to/library_scripts/copy_to_ftp_proxies.py" "<source.directory>/_proxies/<source.basename>"
'''

import sys
import shutil

print(sys.argv)

path_remote = "/mnt/path/to/remote/folder"
library_root = "/mnt/path/to/internal/library"

path_element = ' '.join(sys.argv[1:])
path_output = path_element.replace(library_root, path_remote)

print(path_element)
print(path_output)

try:
    shutil.copytree(path_element, path_output)
except:
    pass
