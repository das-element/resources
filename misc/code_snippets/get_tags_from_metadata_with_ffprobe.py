
"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/

Script get the metadata of a file with ffprobe.
1. adjust to your ffprobe executable file
2. we assume here that the metadata is a string that separates tags by comma

"""

EXECUTABLE_FFPROBE = 'ffprobe'


def get_tags_from_metadata(file_path):
    def get_ffprobe_data(file_path):
        cmd = [EXECUTABLE_FFPROBE, '-export_xmp', '1', file_path]
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return output[1].decode('utf8', 'ignore')

    tags = []
    data = get_ffprobe_data(file_path)

    # custom metadat tag - 1
    regex = 'xmp:Label=["](.*)["]'
    match = re.search(regex, data)
    if match:
        match_string = match.groups()[0]
        tags += match_string.split(',')

    # custom metadat tag - 2
    regex = 'myCustomTags\W+[:]\W(.*)'
    match = re.search(regex, data)
    if match:
        match_string = match.groups()[0]
        tags += match_string.split(',')

    return tags
