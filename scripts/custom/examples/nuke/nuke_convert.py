"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Example script to convert the element using Nuke.

Requirements:

Two parts are required, one is this Python file and a Nuke template file (e.g.: nuke_convert_log2lin.nk).
- create a transcoding template with a 'custom arguments' task
- set the values for the executable and parameters from examples below

The environment variable 'DASELEMENT_RESOURCES' needs to point to the location where this script is located.
Make sure to define the resolution changes also in the transcoding template path values.
Define the 'Type of output file' if you convert e.g a movie file into a EXR sequence.

In the parameters you can link to the different nuke_convert_*-templates.
This allows you to define different operations, like color space conversion or reformating, depending on the input.

######## Linux / MacOS ########
exec:
/usr/local/Nuke12.2v3/Nuke12.2v3
/Applications/Nuke12.2v3/Nuke12.2v3.app/Contents/MacOS/Nuke12.2

params:
-t "$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_convert.py" "$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_convert_lin2lin.nk" "<source.directory>/<source.filename>" "<path>" <source.frame_first> <source.frame_last> <frame_first> <frame_last>


######## Windows ########
exec:
"C:/Program Files/Nuke12.2v3/Nuke12.2.exe"

params:
-t "%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_convert.py" "%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_convert_lin2lin.nk" "<source.directory>/<source.filename>" "<path>" <source.frame_first> <source.frame_last> <frame_first> <frame_last>


######## Example: AWS Deadline ########
exec:
/opt/Thinkbox/Deadline10/bin/deadlinecommand
"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"

params:
-SubmitCommandLineJob -executable "/usr/local/Nuke12.2v3/Nuke12.2v3" -arguments "-t \"$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_convert.py\" \"$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_convert_lin2lin.nk\" \"<source.directory>/<source.filename>\" \"<path>\" <source.frame_first> <source.frame_last> <frame_first> <frame_last>" -name "[das element] <name> - main" -prop BatchName="[das element] <name>" -priority 50 -prop OutputDirectory0=\"<paths.main.directory>\" -prop OutputFilename0=\"<paths.main.filename>\"
-SubmitCommandLineJob -executable "C:/Program Files/Nuke12.2v3/Nuke12.2.exe" -arguments "-t \"%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_convert.py\" \"%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_convert_lin2lin.nk\" \"<source.directory>/<source.filename>\" \"<path>\" <source.frame_first> <source.frame_last> <frame_first> <frame_last>" -name "[das element] <name> - main" -prop BatchName="[das element] <name>" -priority 50 -prop OutputDirectory0=\"<paths.main.directory>\" -prop OutputFilename0=\"<paths.main.filename>\"

"""

import os
from datetime import datetime

import nuke

print('nuke.rawArgs: %s' % nuke.rawArgs)
path_script = nuke.rawArgs[-7].replace('\\', '/')
path_input = nuke.rawArgs[-6].replace('\\', '/')
path_output = nuke.rawArgs[-5].replace('\\', '/')
source_frame_first = int(nuke.rawArgs[-4])
source_frame_last = int(nuke.rawArgs[-3])
frame_first = int(nuke.rawArgs[-2])
frame_last = int(nuke.rawArgs[-1])

# define default first frame of sequence
default_first_frame = 1001

# Nuke starts movie files with Frame 1, not Frame 0
source_is_movie = path_input.split('.')[-1] in ['mov', 'mp4']
if source_is_movie:
    source_frame_first += 1
    source_frame_last += 1

# open template nuke script
nuke.scriptOpen(path_script)

# set the file paths for the input
print('Read Node Path: %s' % path_input)
node_read = nuke.toNode('input')
node_read['file'].setValue(path_input)
node_read['first'].setValue(source_frame_first)
node_read['last'].setValue(source_frame_last)
node_read['origfirst'].setValue(source_frame_first)
node_read['origlast'].setValue(source_frame_last)

# set the file paths for the output
print('Write Node Path: %s' % path_output)
node_write = nuke.toNode('output')
node_write['file'].setValue(path_output)

# Example to modify the color space conversion
# node_colorspace = nuke.toNode('colorspace')
# node_colorspace['colorspace_in'].setValue('RGB')  # RGB is Linear
# node_colorspace['colorspace_out'].setValue('RGB')  # RGB is Linear

# set the time offset
node_timeoffset = nuke.toNode('timeoffset')
node_timeoffset['time_offset'].setExpression('%s-[value [topnode].first]' %
                                             default_first_frame)

# save nuke file in a folder called 'jobs' with the timestamp in the file name
# /some/path/jobs/2021-11-06_11-58-17_nuke_convert_lin2lin.nk
date_string = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
path_script_directory = os.path.dirname(path_script) + '/jobs'
path_script_filename = date_string + '_' + os.path.basename(path_script)
path_script_job = path_script_directory + '/' + path_script_filename

# make sure that the jobs folder exists
if not os.path.exists(path_script_directory):
    os.makedirs(path_script_directory)

# save the job nuke script
nuke.scriptSaveAs(path_script_job)

# render the job
nuke.execute(node_write, frame_first, frame_last, continueOnError=False)
