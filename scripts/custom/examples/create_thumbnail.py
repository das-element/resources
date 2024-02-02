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


def frames_to_timestamp(frames, frame_rate):
    # Python 2
    # h = operator.floordiv(frames, 3600 * frame_rate)
    # Python 3
    h = frames // (3600 * frame_rate)

    #  check to see if hours >= 24. SMPTE Timecode only goes to 23:59
    if h >= 24:
        h = h % 24
        frames = frames - (86400 * frame_rate)

    # Python 2
    # m = operator.floordiv(frames % (3600 * frame_rate), 60 * frame_rate)
    # Python 3
    m = (frames % (3600 * frame_rate)) // (60 * frame_rate)

    value = (1.0 / float(frame_rate)) * float(frames) % 60
    value = '%.3f' % (value)
    s = int(value.split('.')[0])  # get secods
    f = value.split('.')[1]  # get millisecond

    return '%02d:%02d:%02d.%03s' % (h, m, s, f)


def get_movie_frame_rate(path):
    command = [
        EXECUTABLE_FFPROBE, '-v', '0', '-of', 'csv=p=0', '-select_streams',
        'v:0', '-show_entries', 'stream=r_frame_rate', '"{}"'.format(path)
    ]
    command_string = ' '.join(command)
    result = eval(os.popen(command_string).read())
    frame_rate = round(result, 3)
    print('Movie frame rate: {}'.format(frame_rate))
    return frame_rate


def execute_command(command):
    command_as_string = ' '.join(command)
    print(command_as_string)

    process = subprocess.run(command_as_string,
                             capture_output=True,
                             shell=True)

    returncode = process.returncode
    output = process.stdout.decode('utf8', 'ignore').strip('\n')
    error = process.stderr.decode('utf8', 'ignore').strip('\n')
    return returncode, output, error


def main(*args):
    path, path_output, media_type, first, last = args[0]

    width = 960
    height = 540
    frame_center = int(int(first) + round((int(last) - int(first)) / 2))

    command = [EXECUTABLE_FFMPEG]

    if media_type == 'image':
        command += ['-i', '"{}"'.format(path)]

    if media_type == 'movie':
        frame_rate = get_movie_frame_rate(path)
        timestamp = frames_to_timestamp(frame_center, frame_rate)
        command += ['-i', '"{}"'.format(path), '-ss', timestamp]

    if media_type == 'sequence':
        # rudimentary frame padding validation - we assume here that the frame counter is just before the file extension
        # %04d defines the frame padding of 4 -> 0001
        regex = r'(\d+|[%][0]\d[d]|[#]+)\.\w{2,}$'
        match = re.search(regex, path)

        if not match:
            raise Exception('Failed to validate frame padding of source path')

        value = match.groups()[0]
        frame_padding = value if '%' in value else '%0{}d'.format(len(value))
        frame = frame_padding % frame_center

        path = Path(path)
        stem_name = re.sub(regex, frame, path.name)
        path_frame = path.parent / (stem_name + path.suffix)

        # make sure to convert from linear to videospace
        command += ['-i', '"{}"'.format(path_frame)]

    filter_scale = 'scale={}:{}:'.format(width, height)
    filter_scale += 'force_original_aspect_ratio=decrease,'
    filter_scale += 'pad={}:{}:(ow-iw)/2:(oh-ih)/2'.format(width, height)

    command += [
        '-y', '-vf', '"premultiply=inplace=1,{}"'.format(filter_scale), '-q:v',
        '5', '-frames:v', '1', '-update', 'true', '"{}"'.format(path_output)
    ]

    # make sure folders exists
    if not Path(path_output).parent.exists():
        Path(path_output).parent.mkdir()

    # execute command
    returncode, output, error = execute_command(command)

    if returncode != 0:
        print(returncode)
        print(output)
        print(error)
        raise Exception("Oh no .... something went wrong!")

    return returncode


if __name__ == '__main__':
    main(sys.argv[1:])
