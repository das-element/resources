"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/



Example Python script for pre gallery load hook (pre_gallery_load.py)
This hook lets you filter out specific elements so they remain hidden from the user.

Example element data:

[{
    'uuuid': '01859093927b96d3a5131f9cd42d8ed7',
    'name': 'awesome_element_00044',
    'path': '/path/to/server/awesome_element_0044.mov',
    'path_source': '/server/path/to/source_file.mov',
    'tags': [{'id': 'awesome', 'name': 'awesome', 'type': 'custom'}],
    'metadata': [{'id': '01957544525f7c4a8186e280f991cf2c',
                'key': 'foo',
                'value': 'bar'}],
    ...
}]

"""

import os
import sys

RESTIRCTED_SHOW = ['project-abc', 'project-xyz']
RESTRICTED_FACILITY = ['munich', 'london']


def is_restricted_show(path):
    return any(show in path for show in RESTIRCTED_SHOW)


def is_restricted_facility():
    return os.getenv('CURRENT_FACILITY') in RESTRICTED_FACILITY


def main(*args, logger=None):
    # args will be a List of Dicts
    items = args[0]
    result = []

    for item in items:
        path = item.get('path', '')
        path_source = item.get('path_source', '')

        if is_restricted_show(path) or is_restricted_show(path_source):
            continue

        if is_restricted_facility():
            continue

        result.append(item)
    return result


if __name__ == '__main__':
    main(sys.argv[1:])
