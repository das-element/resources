"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Create a transcoding template with a 'custom command' task.
This example is for Linux. For Windows (examples below) adjust the ffmpeg executable paths.

Requirements:
The environment variable 'DASELEMENT_RESOURCES' needs to point to some network
share where this script is located.


######## Linux ########
exec:
/opt/Thinkbox/Deadline10/bin/deadlinecommand

params:
-SubmitCommandLineJob -startupdirectory "$DASELEMENT_RESOURCES" -executable "/usr/bin/python" -arguments "scripts/custom/create_thumbnail.py \"<path>\" \"<path_thumbnail>\" <media_type> <frame_first> <frame_last>" -name "[das element] <name> - thumbnail" -prop BatchName="[das element] <name>" -frames 1 -chunksize 1 -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.thumbnail.directory>\" -prop OutputFilename0=\"<paths.thumbnail.filename>\"


######## Windows ########
exec:
"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"

params:
-SubmitCommandLineJob -startupdirectory "%DASELEMENT_RESOURCES%" -executable "C:/Python/Python37/python.exe" -arguments "scripts/custom/create_thumbnail.py \"<path>\" \"<path_thumbnail>\" <media_type> <frame_first> <frame_last>" -name "[das element] <name> - thumbnail" -prop BatchName="[das element] <name>" -frames 1 -chunksize 1 -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.thumbnail.directory>\" -prop OutputFilename0=\"<paths.thumbnail.filename>\"

"""

import os
import re
import subprocess
import sys
from pathlib import Path

CURRENT_OS = sys.platform

if CURRENT_OS in ("linux", "linux2"):
    EXECUTABLE_FFMPEG = '/usr/bin/ffmpeg'
    EXECUTABLE_FFPROBE = '/usr/bin/ffprobe'
elif CURRENT_OS == "darwin":
    EXECUTABLE_FFMPEG = '/usr/bin/ffmpeg'
    EXECUTABLE_FFPROBE = '/usr/bin/ffprobe'
elif CURRENT_OS in ("win32", "win64"):
    EXECUTABLE_FFMPEG = 'C:/ffmpeg/bin/ffmpeg.exe'
    EXECUTABLE_FFPROBE = 'C:/ffmpeg/bin/ffprobe.exe'
else:
    raise Exception("Unknown operating system: {}".format(CURRENT_OS))


def frames_to_timecode(frames, frame_rate):
    h = int(frames / 86400)
    m = int(frames / 1440) % 60
    s = int((frames % 1440) / frame_rate)
    f = frames % 1440 % frame_rate
    return '%02d:%02d:%02d.%02d' % (h, m, s, f)


def get_movie_frame_rate(path):
    command = [
        EXECUTABLE_FFPROBE, '-v', '0', '-of', 'csv=p=0', '-select_streams',
        'v:0', '-show_entries', 'stream=r_frame_rate', '"{}"'.format(path)
    ]
    command_string = ' '.join(command)
    return eval(os.popen(command_string).read())


def main(*args):
    path, path_output, media_type, first, last = args[0]

    width = 960
    height = 540
    frame_center = int(int(first) + round((int(last) - int(first)) / 2))

    executable = [EXECUTABLE_FFMPEG]
    arguments = []

    if media_type == 'image':
        arguments += ['-i', path]

    if media_type == 'movie':
        frame_rate = get_movie_frame_rate(path)
        timestamp = frames_to_timecode(frame_center, frame_rate)
        arguments += ['-i', path, '-ss', timestamp]

    if media_type == 'sequence':
        extension = Path(path).suffix
        # {:04d} defines the frame padding of 4 -> 0001
        path_center_frame = '{}.{:04d}{}'.format(
            '.'.join(path.split('.')[:-2]), frame_center, extension)
        # make sure to convert from linear to videospace
        arguments += ['-gamma', '2.2', '-i', path_center_frame]

    filter_scale = 'scale={}:{}:'.format(width, height)
    filter_scale += 'force_original_aspect_ratio=decrease,'
    filter_scale += 'pad={}:{}:(ow-iw)/2:(oh-ih)/2'.format(width, height)

    arguments += [
        '-y', '-vf', filter_scale, '-vcodec', 'png', '-q:v', '5', '-frames:v',
        '1', path_output
    ]

    command = executable + arguments
    print('Command to execute:')
    print(' '.join(command))

    if not Path(path_output).parent.exists():
        Path(path_output).parent.mkdir()

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode != 0:
        print(process.returncode)
        print(output)
        print(error)
        raise Exception("Oh no ... something went wrong!")

    return process.returncode


if __name__ == '__main__':
    main(sys.argv[1:])
