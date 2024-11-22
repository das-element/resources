"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Create a transcoding template with a 'custom arguments' task.
This example is for Linux. For Windows (examples below) adjust the ffmpeg executable paths.

For Windows there is a command line limit of 8190 characters.
This can be a problem if the filmstrip has a large number of frames. Something around 50 frames and more.
That's why we need to create chunks/batches of the filmstrip first and in the end stitch them back together

If you are using Linux/MacOS and not Windows or if you haven't experienced that issues yet,
simply take the other Pyhton scripts (create_filmstrip.py) since that one is eassier to understand.


Requirements:
The environment variable 'DASELEMENT_RESOURCES' needs to point to some network
share where this script is located.

Run code with Python 3!
For Python 2 you have to adjust the subprocess command


######## Linux ########
exec:
/opt/Thinkbox/Deadline10/bin/deadlinecommand

params:
-SubmitCommandLineJob -startupdirectory "$DASELEMENT_RESOURCES" -executable "/usr/bin/python3" -arguments "scripts/custom/create_filmstrip_batch.py \"<path>\" \"<path_filmstrip>\" <media_type> <frame_first> <frame_last>" -name "[das element] <name> - filmstrip" -prop BatchName="[das element] <name>" -frames 1 -chunksize 1 -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.filmstrip.directory>\" -prop OutputFilename0=\"<paths.filmstrip.filename>\"


######## Windows ########
exec:
"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"

params:
-SubmitCommandLineJob -startupdirectory "%DASELEMENT_RESOURCES%" -executable "C:/Python/Python37/python.exe" -arguments "scripts/custom/create_filmstrip_batch.py \"<path>\" \"<path_filmstrip>\" <media_type> <frame_first> <frame_last>" -name "[das element] <name> - filmstrip" -prop BatchName="[das element] <name>" -frames 1 -chunksize 1 -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.filmstrip.directory>\" -prop OutputFilename0=\"<paths.filmstrip.filename>\"

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
    result = eval(os.popen(command_string).read().lstrip('(').rstrip(',)'))
    frame_rate = round(result, 3)
    print('Movie frame rate: {}'.format(frame_rate))
    return frame_rate


def get_frame_numbers(frame_first, frame_last, number_of_frames):
    frame_numbers = []  # the frame numbers used for the filmstrip
    frame_numbers_total = int(frame_last) - int(frame_first) + 1

    # calculate which frames to use for the filmstrip
    # the frames will be evenly distributed across the total length of the element
    frame_mod = float(frame_numbers_total) / float(number_of_frames)
    if frame_mod < 1.0:
        frame_mod = 1.0

    for num in range(frame_numbers_total):
        if float(num) % frame_mod >= 1.0:
            continue
        frame_numbers.append(int(num))

    print('Frame numbers:')
    print(frame_numbers[:number_of_frames])
    # limit number of frames to the given frames value.
    # This fixes potential some rounding calculation errors
    return frame_numbers[:number_of_frames]


def write_temp_frame_thumbnail(media_type, path_input, path_output,
                               frame_number, width, height, frame_rate,
                               frame_first):

    # scale and add letterbox if needed
    scale = 'scale={}:{}:'.format(width, height)
    scale += 'force_original_aspect_ratio=decrease,'
    scale += 'pad={}:{}:(ow-iw)/2:(oh-ih)/2'.format(width, height)

    command = [EXECUTABLE_FFMPEG, '-y', '-nostats', '-loglevel', 'warning']

    if media_type == 'sequence':
        command += _get_arguments_for_sequence(path_input, frame_number,
                                               frame_first)
    else:
        command += _get_arguments_for_movie(path_input, frame_number,
                                            frame_rate)

    command += [
        '-vf', '"premultiply=inplace=1,{}"'.format(scale), '-q:v', '5',
        '-frames:v', '1', '"{}"'.format(path_output)
    ]

    returncode, output, error = execute_command(command)

    if returncode != 0:
        print('Returncode: {}'.format(returncode))
        print('Output: {}'.format(output))
        print('Error: {}'.format(error))

    return True


def _get_arguments_for_sequence(path, frame_number, frame_first):
    # rudimentary frame padding validation - we assume here that the frame counter is just before the file extension
    # %04d defines the frame padding of 4 -> 0001
    regex = r'(\d+|[%][0]\d[d]|[#]+)\.\w{2,}$'
    match = re.search(regex, path)

    if not match:
        raise Exception('Failed to validate frame padding of source path')

    value = match.groups()[0]
    frame_padding = value if '%' in value else '%0{}d'.format(len(value))
    frame = frame_padding % (int(frame_first) + int(frame_number))

    path = Path(path)
    stem_name = re.sub(regex, frame, path.name)
    path_frame = path.parent / (stem_name + path.suffix)

    # make sure to convert from linear to videospace
    return ['-i', '"{}"'.format(path_frame)]


def _get_arguments_for_movie(path, frame, frame_rate):
    arguments = []
    timestamp = frames_to_timestamp(int(frame), frame_rate)

    # the flag "ignore_editlist" is only available to certain movie files
    if not Path(path).suffix.lower() in ('.avi', '.flv', '.mkv', '.mpg',
                                            '.mpeg', '.mp4', '.mxf'):
        arguments += ['-ignore_editlist', '1']

    arguments += [
        '-ss', timestamp, '-noaccurate_seek', '-i', '"{}"'.format(path)
    ]
    return arguments


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
    path, path_output, media_type, frame_first, frame_last = args[0]

    if media_type == 'image':
        print('No sequence or movie file - will not render filmstrip')
        return False

    if media_type == 'generic':
        print('Is generic media type - will not render filmstrip')
        return False

    paths_frames = []  # temporary file paths

    command = [EXECUTABLE_FFMPEG, '-y', '-vsync', '0']
    streams = ''

    height = 270  # set height of filmstrip
    number_of_frames = 24  # the number of frames that the filmstrip has
    frame_width = int((16. / 9.) * float(height))  # image has 16:9 image ratio
    frame_numbers = get_frame_numbers(frame_first, frame_last,
                                      number_of_frames)

    if media_type == 'movie':
        frame_rate = get_movie_frame_rate(path)
    else:
        frame_rate = 24  # set some random frame rate for the image sequence

    # make sure folders exists
    if not Path(path_output).parent.exists():
        Path(path_output).parent.mkdir()

    # for Windows there is a command line limit of 8190 characters
    # that's why we need to create chunks/batches of the filmstrip first
    # and in the end stitch them back together

    batch_mod = 24  # number of frames to batch together
    stream_counter = 0
    batch_number = 0
    batches = {}

    # render single thumbnails
    for stream_number, frame_number in enumerate(frame_numbers):
        path_frame = Path('{}-{}.{}'.format(path_output, frame_number, 'jpg'))
        paths_frames.append(path_frame)

        if stream_number % batch_mod == 0:
            stream_counter = 0
            batch_number += 1
            batches[batch_number] = {
                'command': [EXECUTABLE_FFMPEG, '-y', '-vsync', '0'],
                'streams': '',
                'frames': 0,
            }

        batches[batch_number]['streams'] += '[{}:v]'.format(stream_counter)
        batches[batch_number]['command'] += ['-i', '"{}"'.format(path_frame)]
        batches[batch_number]['frames'] += 1
        stream_counter += 1

        write_temp_frame_thumbnail(media_type, path, path_frame, frame_number,
                                   frame_width, height, frame_rate,
                                   frame_first)

    # render batches of thumbnails
    command = [EXECUTABLE_FFMPEG, '-y', '-vsync', '0']
    streams = ''
    batch_output_paths = []

    for batch_id, data in batches.items():
        command_batch = data['command']
        streams_batch = data['streams']
        number_of_batch_frames = data['frames']
        path_output_batch = '{}-b{}.jpg'.format(path_output, batch_id)

        # if a clip is shorter than the frames, make sure to add blank frames
        padding = 'pad={}:{}:0:0:#161a21'.format(
            number_of_batch_frames * frame_width, height)

        if len(frame_numbers) > 1:
            # if a movie file has only one frame it will not work
            # for hstack a minimum of 2 frames is required
            streams_batch += 'hstack=inputs=' + str(
                number_of_batch_frames) + ','

        streams_batch += padding + '[v]'
        command_batch += [
            '-filter_complex', '"{}"'.format(streams_batch), '-map', '[v]',
            '"{}"'.format(path_output_batch)
        ]

        returncode, output, error = execute_command(command_batch)

        if returncode != 0:
            print(returncode)
            print(output)
            print(error)
            raise Exception("Oh no .... something went wrong!")

        stream_id = batch_id - 1  # the stream_id needs to start at 0
        streams += '[{}:v]'.format(stream_id)
        command += ['-i', '"{}"'.format(path_output_batch)]

        batch_output_paths.append(path_output_batch)

    # finally stitch together the batches to the final filmstrip

    # if a clip is shorter than the frames, make sure to add blank frames
    padding = 'pad={}:{}:0:0:#161a21'.format(number_of_frames * frame_width,
                                             height)

    if len(batch_output_paths) > 1:
        # if a movie file has only one frame it will not work
        # for hstack a minimum of 2 frames is required
        streams += 'hstack=inputs=' + str(batch_number) + ','

    streams += padding + '[v]'
    command += [
        '-filter_complex', '"{}"'.format(streams), '-map', '[v]',
        '"{}"'.format(path_output)
    ]

    returncode, output, error = execute_command(command)

    # finally delete the temporary frames
    for path in paths_frames + batch_output_paths:
        try:
            os.remove(str(path))
        except OSError as error_msg:
            print(error_msg)

    if returncode != 0:
        print(returncode)
        print(output)
        print(error)
        raise Exception("Oh no .... something went wrong!")

    return returncode


if __name__ == '__main__':
    main(sys.argv[1:])
