'''
exec:
python

params:
"/mnt/path/to/library_scripts/copy_to_ftp_proxies.py" "<source.directory>/_proxies/<source.basename>"
'''

import sys
import shutil

print(sys.argv)

path_dropbox = "/Volumes/RAID_04 [48TB - T3]/Dropbox (Personal)/VFX Elements"
library_root = "/Volumes/AssetShare/_VFX_ELEMENTS"

path_element = ' '.join(sys.argv[1:])
path_output = path_element.replace(library_root, path_dropbox)

print(path_element)
print(path_output)

#try:
#    shutil.copytree(path_element, path_output)
#except:
#    pass
