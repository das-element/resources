"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/

Script to convert a folder structure into the hierarchy tree format for das element
1. change the 'path' at the bottom of the script
2. copy&paste or merge the result into the 'hierarchy.json' file
"""

import json
from pathlib import Path


def get_hierarchy_from_folder(root_path):
    def get_folders_as_dict(root_path):
        result = {}
        root_path += '/'  # need to add a trailing slash here - otherwise we get an empty data dict
        for path in Path(root_path).rglob('*'):
            data = result
            # remove root folder since we are only interessted in the folder structure
            path_strip_root = str(path).replace(root_path, '')
            items = path_strip_root.split("/")
            for item in items:
                data = data.setdefault(item, {})
        return result

    def convert_to_hierarchy(data, foo='', result=[]):
        # recursive function
        result = []
        for key, entity in data.items():
            item_id = '{}-{}'.format(foo, key)
            item_id = item_id.lstrip('-')  # remove any dashes at the front
            item_id = item_id.lower()  # make the ID lowercase
            item_id = item_id.replace(' ', '-')  # remove spaces in the ID
            new_item = {'id': item_id, 'name': key, 'synonyms': []}
            if entity:
                # only create children entry if there are any
                new_item['children'] = convert_to_hierarchy(entity,
                                                            item_id,
                                                            result=[])
            result.append(new_item)
        return result

    # path should only have forward slashes - that's important for Windows
    root_path = root_path.replace('\\', '/')

    # get the folder strucutre as a dictionary
    paths_as_dict = get_folders_as_dict(root_path)
    # and now use a recursive function to convert it to the correct format
    hierarchy_data = convert_to_hierarchy(paths_as_dict)

    # this is the default hierarchy structure
    # the root / (Q2574811) is required
    return {
        "hierarchy": [{
            "children": hierarchy_data,
            "id": "Q2574811",
            "name": "/"
        }],
        "version": "my custom hierarchy"
    }


path = '/path/to/your/folder'
result = get_hierarchy_from_folder(path)

print(json.dumps(result, indent=4))
