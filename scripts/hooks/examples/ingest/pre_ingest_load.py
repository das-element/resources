"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/



Example Python script for pre ingest load hook (pre_ingest_load.py)
This scripts will automatically create tags based on keywords in the file paths.
The last found tag will be set as the category.
The script will also try to find assets with a certain naming pattern like:

env_intHouse
veh_awesomeCar

"""

import sys
import re

"""
Example to load custom external Python code

To make sure everything updates each time this hook file gets exectured see the example import:

import some_module # Import your external modules
recursive_reload(some_module) # Recursively reload the modules
from some_module import some_function # Import the necessary functions after reloading
"""

# search for these tags in the file paths and create them as tags
TAGS = ['assets', 'environments', 'hdri', 'photogrammetry', 'texture']


def main(*args):
    '''
        args will be a List of Dicts:

        [{
            'path': '/path/to/some/file.mov',
            'path_thumbnail': '/path/to/some/thumbnail.jpg',
            'path_proxy': '/path/to/some/proxy.mov',
            'category': 'torch',
            'tags': ['fire', 'flame'],
            'colorspace': 'rec709',
            'mapping': 'copy & rename',
            'metadata': {'key1': 'value1', 'key2': 'value2'},
            'additionals': [{'path': '/path/to/some/additional.exr', 'type': 'file', 'name': 'additional name'}]            
        }]
    '''
    items = args[0]
    result = []

    for item in items:
        path = item.get('path', '').replace('\\', '/')
        path_items = path.split('/')
        for path_item in path_items:
            # search for keywords in file path
            if path_item in TAGS:
                item.get('tags', []).append(path_item)

            # example regular expression to search for a pattern in the file path
            regex_asset = r'(prp|env|veh_\w*)'
            match = re.search(regex_asset, path_item)
            if match:
                item.get('tags', []).append(path_item)

        if item.get('tags'):
            # set last tag as the category
            item['category'] = item['tags'][-1]

        # overwrite colorspace reference value for an element
        # please note: this does not acctually change the colorspace and does not effect the actual colorspace of the files on disk
        # item['colorspace'] = 'my colorspacename'

        # set template mapping
        item['mapping'] = 'copy & rename'

        # add custom metadata
        item['metadata'] = {'key1': 'value1', 'key2': 'value2'}

        # custom thumbnail
        # item['path_thumbnail'] = '/path/to/custom/thumbnail.jpg'

        # custom proxy file
        # item['path_proxy'] = '/path/to/custom/proxy.mov'

        result.append(item)
    return result


if __name__ == '__main__':
    main(sys.argv[1:])
