"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Example file if you use some custom dependency in your submission scripts.
To resolve a path pattern like <custom.dependecy> you need to add some value for the custom data.
If that is not provided the resolve would otherwise fail if you re-render the proxies and there is no main task to provide the depdency.

"""

import sys


def main(*args, logger=None):
    data = args[0]

    # make sure to set some value for the dependency.
    # otherwise it will fail when resolving the path pattern '<custom.dependency>'
    if not data.get('template_values', {}).get('custom'):
        data['template_values']['custom'] = {'dependency': ''}

    return data


if __name__ == '__main__':
    main(sys.argv[1:])
