"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Simple script to lauch das element lite with a specific config file

1. get project config file path
2. set the environment variable to the config file
3. launch the application

"""

import os


def launch_das_element_lite():
    def get_project():
      return 'foobar'

    def get_project_config_path(project):
        return '/mnt/server/{}/.das-element/das-element.conf'.format(project)

    app_name = 'das-element-lite-1.1.4'
    app_path = '/Applications/{}.app'.format(app_name)  # this path is for MacOS

    project = get_project()
    project_config_path = get_project_config_path(project)

    # set environment variable to point to project specific config file
    os.environ['DASELEMENT_CONFIG_PATH'] = project_config_path

    # command to launche the software
    cmd = 'open {}'.format(PATH_APP) # this command is for MacOS

    print(os.environ['DASELEMENT_CONFIG_PATH'])
    print(cmd)

    os.system(cmd)


launch_das_element_lite()
