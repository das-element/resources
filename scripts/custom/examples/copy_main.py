"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Create a transcoding template with a 'custom command' task.
This example is for Linux and Deadline.

Requirements:
The environment variable 'DASELEMENT_RESOURCES' needs to point to some network
share where this script is located. In this example to copy a image sequence you
need the package fileseq (https://pypi.org/project/Fileseq/)
$ pip install fileseq


######## Linux ########
exec:
/opt/Thinkbox/Deadline10/bin/deadlinecommand

params:
-SubmitCommandLineJob -startupdirectory "$DASELEMENT_RESOURCES" -executable "/usr/bin/python" -arguments "scripts/custom/copy_main.py \"<source.path>\" \"<path>\" <media_type> <frame_first> <frame_last>" -frames 1 -chunksize 1 -priority 50 -name "[das element] <name> - main" -prop BatchName="[das element] <name>" -prop OutputDirectory0=\"<paths.main.directory>\" -prop OutputFilename0=\"<paths.main.filename>\"

######## Windows ########
exec:
"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"

params:
-SubmitCommandLineJob -startupdirectory "%DASELEMENT_RESOURCES%" -executable "C:/Python/Python37/python.exe" -arguments "scripts/custom/copy_main.py \"<source.path>\" \"<path>\" <media_type> <frame_first> <frame_last>" -frames 1 -chunksize 1 -priority 50 -name "[das element] <name> - main" -prop BatchName="[das element] <name>" -prop OutputDirectory0=\"<paths.main.directory>\" -prop OutputFilename0=\"<paths.main.filename>\"

"""

import sys
import shutil
from fileseq import FileSequence, findSequenceOnDisk
from pathlib import Path


def copy_file_sequence(source, output, frame_first, frame_last):
    # get all source file paths
    source_files = [Path(path) for path in list(findSequenceOnDisk(source))]
    # get all element file paths
    sequence = FileSequence(output.replace('#', '@'))
    sequence.setFrameRange('{}-{}'.format(frame_first, frame_last))
    output_files = [Path(path) for path in list(sequence)]

    # create destination folder if it does not yet exist
    if not Path(output).parent.exists():
        Path(output).parent.mkdir()

    # copy files
    has_error = False
    for item in zip(source_files, output_files):
        if not item[0].exists():
            has_error = True
            print('Source file does not exist: {}'.format(item[0]))
            print('Failed to copy file: {}'.format(item[1]))
            continue
        shutil.copy2(str(item[0]), str(item[1]))

    return has_error


def main(*args):
    print(args[0])
    path_source, path_output, media_type, frame_first, frame_last = args[0]

    if media_type == 'sequence':
        has_error = copy_file_sequence(path_source, path_output, frame_first,
                                       frame_last)
        if has_error:
            raise Exception("Oh no ... something went wrong!")
        return True

    # check if the source file path exists
    if not Path(path_source).exists():
        print('Source file does not exist: {}'.format(path_source))
        print('Failed to copy file: {}'.format(path_output))
        raise Exception("Oh no ... something went wrong!")

    shutil.copy2(path_source, path_output)
    return True


if __name__ == '__main__':
    main(sys.argv[1:])
