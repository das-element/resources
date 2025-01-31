"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/

Python script for Autodesk Flame.
When the script gets executed it will try import a file path or sequence from the clipboard.

How to use:
In Das Element, selected an element and press Ctrl+c (macOS: cmd+c) to copy the file path to the clipboard
In Flame, exectue this python script to import the file into the current project.
It will be imported to a library named "DasElement Import". Can be changed in the IMPORT_REEL_NAME variable.

Note:
For Linux make sure xclip is installed (sudo yum install xclip).
"""

import flame
import subprocess
import sys

IMPORT_REEL_NAME = "DasElement Import"
VALID_FILE_EXTENSIONS = (
    ".mov",
    ".exr",
    ".jpg",
    ".jpeg",
    ".png",
    ".tif",
    ".tiff",
)


def get_reel(reel_name=IMPORT_REEL_NAME):
    # Get the current project's workspace
    workspace = flame.projects.current_project.current_workspace

    # Loop through libraries to find the reel
    for library in workspace.libraries:
        for reel in library.reels:
            if reel.name == reel_name:
                print(f"Found reel: '{reel_name}'")
                return reel

    # If not found, create a new reel in the first available library
    if workspace.libraries:
        new_reel = workspace.libraries[0].create_reel(reel_name)
        print(f"Reel not found. Creating reel: '{reel_name}'")
        return new_reel
    else:
        print("No libraries available to create a new reel.")
        return None


def get_paths_from_clipboard():
    if sys.platform == "darwin":
        # macOS clipboard command
        result = subprocess.run(["pbpaste"], capture_output=True, text=True)
    else:
        # Linux clipboard command
        result = subprocess.run(["xclip", "-selection", "clipboard", "-o"],
                                capture_output=True,
                                text=True)
    # can return one or more file paths
    return result.stdout.strip().split('\n')


def validate_file_path(path):
    return path.startswith("/") and path.endswith(VALID_FILE_EXTENSIONS)


def import_from_clipboard():
    try:
        file_paths = get_paths_from_clipboard()
        for file_path in file_paths:
            # Validate file path
            if validate_file_path(file_path):
                print(f"Importing: {file_path}")
                # Load into Flame like drag & drop
                flame.import_clips(file_path, get_reel())
            else:
                print("Clipboard does not contain a valid file path.")

    except Exception as e:
        print(f"Error: {e}")


import_from_clipboard()
