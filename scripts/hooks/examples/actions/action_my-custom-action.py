"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Script that gets run before deleting an element.
Data is the element entity that is about to be deleted. No result will be returned.

Example output from das element:

{
    'uuuid': '01859093927b96d3a5131f9cd42d8ed7',
    'uuuid_short': '96d3a513',
    'name': 'awesome_element_00044',
    'category': {
        'child_counter': 7,
        'id': 'Q3196',
        'name': 'fire',
        'type': 'default'
    },
    'category_id': 'Q3196',
    'channel': 3,
    'height': 1080,
    'width': 192,
    'pixel_aspect': '1',
    'frame_first': 1001,
    'frame_last': 1049,
    'frame_count': 50,
    'frame_rate': '25',
    'created_at': '2021-10-01 09:26',
    'media_type': 'movie',
    'number': '00044',
    'colorspace': 'sRGB',
    'colorspace_source': 'sRGB',
    'permission': '111',
    'popularity': 23,
    'tags': 'fire, flame, some other tag',
    'path': '/path/to/server/awesome_element_0044/main_1920x1080_srgb/awesome_element_0044.mov',
    'path_thumbnail': '/path/to/server/awesome_element_0044/thumb_960x540/awesome_element_0044.jpg',
    'path_proxy': '/path/to/server/awesome_element_0044/proxy_1920x1080/awesome_element_0044.mov',
    'path_filmstrip': '/path/to/server/awesome_element_0044/filmstrip_11520x270/awesome_element_0044.jpg'
    'path_source': '/server/path/to/source_file.mov',
    'library': {
        'path': '/path/to/library/.config/das-element.lib',
        'values': []
    }

}

"""

METADATA = {
    'name': 'Custom Action', # display name
    'description': 'A custom action to process selected items', # tooltip when hover over button
    'icon': '/path/to/icon.png', # path  or URL to custom icon
    'color': '#008000', # hex colore code, e.g. '#008000' or 'green'
    'order': 1 # numeric value to order the action buttons
}

import sys
import os


def main(*args, logger=None):
    data = args[0]

    for item in data:
        element_path = item.get('path')
        logger.info('Element path:')
        logger.info(element_path)

    return {
        'status': 'success', # 'error'
        'message': 'Custom action executed successfully'
    }


if __name__ == '__main__':
    main(sys.argv[1:])
