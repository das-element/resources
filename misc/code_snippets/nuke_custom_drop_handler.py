"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/

Define here some custom behaviors when an element from the asset library is dropped into Nuke

Place this file somewhee in your .nuke folder and import it in 'menu.py'

Example (add this line to the menu.py):
import nuke_custom_drop_handler
"""

import nuke
import nukescripts

# check if the file(s) dropped belongs to the elements library
# update this here to your library root path
library_root = "/mnt/library/vfx_elements"
default_first_frame = 1000


def import_element_default(path):
    read_node = nuke.createNode("Read", inpanel=False)
    read_node["file"].fromUserText(path)
    read_node["label"].setValue("asset library")
    # give all asset library Read nodes a specific color
    read_node["tile_color"].setValue(0xff3fff)
    return True


def import_element_movie(path):
    read_node = nuke.createNode("Read", inpanel=False)
    read_node["file"].fromUserText(path)
    read_node["before"].setValue("black")
    read_node["after"].setValue("black")
    read_node["label"].setValue("asset library")
    # give all asset library Read nodes a specific color
    read_node["tile_color"].setValue(0xff3fff)

    # add a Timeoffset to make sure the clip starts at the default first frame
    timeoffset_node = nuke.createNode("TimeOffset", inpanel=False)
    timeoffset_node["time_offset"].setValue(default_first_frame)
    timeoffset_node["label"].setValue("[value this.time_offset]")
    # connect it to the Read node
    timeoffset_node.setInput(0, read_node)
    # just move the Timeoffset node below the Read node
    timeoffset_node.setYpos(read_node.ypos() + 100)
    timeoffset_node.setXpos(read_node.xpos())

    return True


def file_handler(path):
    # get file extension
    # based on the file extension different drop
    extension = path.split('.')[-1]

    if extension in ['mov', 'mp4']:
        return import_element_movie(path)

    return import_element_default(path)


def custom_drop_handler(mimeType, value):
    # if the dropped file path(s) is located in the asset library
    # apply the custom drop behavior
    if value.startswith(library_root):
        return file_handler(value)
    return False


# add this custom drop handler so Nuke will use it
nukescripts.addDropDataCallback(custom_drop_handler)
