"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Add custom tags to an element during the ingest.
This allows you to for example run custom machine learning models to create tags.

Requirements:
You will need the das element API to update the element in the database.
https://github.com/das-element/python-api


######## Linux ########
exec:
/usr/bin/python3

params:
"$DASELEMENT_RESOURCES/scripts/custom/create_custom_tags.py" <element.uuid>


######## Windows ########
exec:
"C:/Python/Python37/python.exe"

params:
"%DASELEMENT_RESOURCES%/scripts/custom/create_custom_tags.py" <element.uuid>

"""

import sys
from daselement_api import api as de

def get_tags(file_path):
    tags = []
    # here you can add your custom code to set more tags
    return tags

def main(*args):
    #  make sure to update this file path to your library .lib file
    library_path = '/some/path/das-element.lib'

    element_uuid = args[0][0]
    # get element by element unique ID (uuid)
    entity = de.get_element_by_uuid(library_path, element_uuid)
    path_thumbnail = entity.get('path_thumbnail')
    path_proxy = entity.get('path_proxy')

    tags = get_tags(path_thumbnail)

    # update the elemente in the database with the new data
    entity_type = 'Element'
    entity_id = entity.get('id')
    # add your new tags to the existing entity tags
    new_data = {'tags': entity.get('tags', []) + tags}

    entity = de.update(library_path, entity_type, entity_id, new_data)
    return True


if __name__ == '__main__':
    main(sys.argv[1:])
