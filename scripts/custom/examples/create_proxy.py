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
-SubmitCommandLineJob -startupdirectory "$DASELEMENT_RESOURCES" -executable "/usr/bin/python" -arguments "scripts/custom/create_proxy.py \"<path>\" \"<path_proxy>\" <media_type> <frame_first>" -name "[das element] <name> - proxy" -prop BatchName="[das element] <name>" -frames 1 -chunksize 1 -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.proxy.directory>\" -prop OutputFilename0=\"<paths.proxy.filename>\"


######## Windows ########
exec:
"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"

params:
-SubmitCommandLineJob -startupdirectory "%DASELEMENT_RESOURCES%" -executable "C:/Python/Python37/python.exe" -arguments "scripts/custom/create_proxy.py \"<path>\" \"<path_proxy>\" <media_type> <frame_first>" -name "[das element] <name> - proxy" -prop BatchName="[das element] <name>" -frames 1 -chunksize 1 -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.proxy.directory>\" -prop OutputFilename0=\"<paths.proxy.filename>\"

"""

import os
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


def main(*args):
    path, path_output, media_type, frame_first = args[0]

    frame_rate = 24  # Set random frame rate. Works for image sequences but is not accurate for movie files!
    width = 1920
    height = 1080

    executable = [EXECUTABLE_FFMPEG]
    arguments = []

    if media_type == 'image':
        print('No sequence or movie file - will not render filmstrip')
        return False

        # as an alternative you could loop an still image for 1 second
        # arguments += ['-loop', '1', '-i', path, '-t', '1']

    if media_type == 'movie':
        frame_rate = get_movie_frame_rate(path)
        arguments += ['-i', path]

    if media_type == 'sequence':
        extension = Path(path).suffix
        # %04d defines the frame padding of 4 -> 0001
        path_string_format = '{}.{}{}'.format('.'.join(path.split('.')[:-2]),
                                              '%04d', extension)
        arguments += [
            '-start_number',
            str(frame_first), '-r',
            str(frame_rate), '-f', 'image2', '-i', path_string_format
        ]

    timestamp_start = frames_to_timestamp(int(frame_first), frame_rate)

    arguments += [
        '-y', '-r',
        str(frame_rate), '-vf',
        'scale={0}:{1}:force_original_aspect_ratio=decrease,pad={0}:{1}:(ow-iw)/2:(oh-ih)/2'
        .format(width, height), '-vcodec', 'libx264', '-crf', '23', '-preset',
        'faster', '-tune', 'film', '-pix_fmt', 'yuv420p', '-framerate',
        str(frame_rate), '-timecode', timestamp_start, '-acodec', 'copy',
        path_output
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
        print('Something went wrong!')
        print(process.returncode)
        print(output)
        print(error)
        raise Exception("Oh no ... something went wrong!")

    return process.returncode


if __name__ == '__main__':
    main(sys.argv[1:])
