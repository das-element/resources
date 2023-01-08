"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/



Example Python script for pre ingest load hook (pre_export.py)
This scripts converts the data so you can import a CSV file into Autodesk Shotgrid


Example output from das element:

[{
    'uuuid': '01859093927b96d3a5131f9cd42d8ed7',
    'uuuid_short': '927b96d3',
    'name': 'awesome_element_00044',
    'category': 'fire',
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
    'popularity': 23,
    'tags': 'fire, flame, some other tag',
    'path': '/path/to/server/awesome_element_0044/main_1920x1080_srgb/awesome_element_0044.mov',
    'path_thumbnail': '/path/to/server/awesome_element_0044/thumb_960x540/awesome_element_0044.jpg',
    'path_proxy': '/path/to/server/awesome_element_0044/proxy_1920x1080/awesome_element_0044.mov',
    'path_filmstrip': '/path/to/server/awesome_element_0044/filmstrip_11520x270/awesome_element_0044.jpg'
    'path_source': '/server/path/to/source_file.mov',
}]


Example output format for Shotgrid:

"Version Name","Frame Range","Frame Count","First Frame","Frame Rate","Last Frame","Path to Frames","Tags"
"awesome_element_0044","1001-1049","50","1001","25","1049","/path/to/server/awesome_element_0044/main_1920x1080_srgb/awesome_element_0044.mov","fire, flame, some other tag"

"""

import sys


def main(*args):
    # args will be a List of Dicts:
    items = args[0]
    result = []

    for item in items:
        frame_range = '{}-{}'.format(item['frame_first'], item['frame_last'])
        sg_item = {
            "Version Name": item['name'],
            "Frame Count": item['frame_count'],
            "First Frame": item['frame_first'],
            "Last Frame": item['frame_last'],
            "Frame Rate": item['frame_rate'],
            "Frame Range": frame_range,
            "Path to Frames": item['path'],
            "Tags": item['tags'].replace(',', ', '),
        }
        result.append(sg_item)
    return result


if __name__ == '__main__':
    main(sys.argv[1:])
