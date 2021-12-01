"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Example script to render the proxy movie for the element using Nuke.

Requirements:

Two parts are required, one is this Python file and the Nuke template file (nuke_proxy.nk).
- create a transcoding template with a 'custom arguments' task
- set the values for the executable and parameters from examples below

The environment variable 'DASELEMENT_RESOURCES' needs to point to the location where this script is located.
Make sure to define the resolution changes also in the transcoding template path values.
Define the 'Type of output file' and set it to 'single file' because the output is a movie file.

######## Linux / MacOS ########
exec:
/usr/local/Nuke12.2v3/Nuke12.2v3
/Applications/Nuke12.2v3/Nuke12.2v3.app/Contents/MacOS/Nuke12.2

params:
-t "$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_proxy.py" "$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_proxy.nk" "<path>" "<path_proxy>" <frame_first> <frame_last>

######## Windows ########
exec:
"C:/Program Files/Nuke12.2v3/Nuke12.2.exe"

params:
-t "%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_proxy.py" "%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_proxy.nk" "<path>" "<path_proxy>" <frame_first> <frame_last>

######## Example: AWS Deadline ########
exec:
/opt/Thinkbox/Deadline10/bin/deadlinecommand
"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"


params:
-SubmitCommandLineJob -executable "/usr/local/Nuke12.2v3/Nuke12.2v3" -arguments "-t \"$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_proxy.py\" \"$DASELEMENT_RESOURCES/scripts/custom/nuke/nuke_proxy.nk\" \"<path>\" \"<path_proxy>\" <frame_first> <frame_last>" -name "[das element] <name> - proxy" -prop BatchName="[das element] <name>" -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.proxy.directory>\" -prop OutputFilename0=\"<paths.proxy.filename>\"
-SubmitCommandLineJob -executable "C:/Program Files/Nuke12.2v3/Nuke12.2.exe" -arguments "-t \"%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_proxy.py\" \"%DASELEMENT_RESOURCES%/scripts/custom/nuke/nuke_proxy.nk\" \"<path>\" \"<path_proxy>\" <frame_first> <frame_last>" -name "[das element] <name> - proxy" -prop BatchName="[das element] <name>" -priority 50 -prop JobDependencies="<custom.dependency>" -prop OutputDirectory0=\"<paths.proxy.directory>\" -prop OutputFilename0=\"<paths.proxy.filename>\"


"""

import os
from datetime import datetime

import nuke

print('nuke.rawArgs: %s' % nuke.rawArgs)
path_script = nuke.rawArgs[-5].replace('\\', '/')
path_input = nuke.rawArgs[-4].replace('\\', '/')
path_output = nuke.rawArgs[-3].replace('\\', '/')
frame_first = int(nuke.rawArgs[-2])
frame_last = int(nuke.rawArgs[-1])

# open template nuke script
nuke.scriptOpen(path_script)

# set the file paths for the input
print('Read Node Path: %s' % path_input)
node_read = nuke.toNode('input')
node_read['file'].setValue(path_input)
node_read['first'].setValue(frame_first)
node_read['last'].setValue(frame_last)

# set the file paths for the output
print('Write Node Path: %s' % path_output)
node_write = nuke.toNode('output')
node_write['file'].setValue(path_output)

# save nuke file in a folder called 'jobs'
date_string = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
path_script_directory = os.path.dirname(path_script) + '/jobs'
path_script_filename = date_string + '_' + os.path.basename(path_script)
path_script_job = path_script_directory + '/' + path_script_filename

# make sure that the jobs folder exists
if not os.path.exists(path_script_directory):
    os.makedirs(path_script_directory)

# save the job nuke script
nuke.scriptSaveAs(str(path_script_job))

# render the job
nuke.execute(node_write, frame_first, frame_last, continueOnError=False)
