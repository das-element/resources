"""
           __                   __                          __
      ____/ /___ ______   ___  / /__  ____ ___  ___  ____  / /_
     / __  / __ `/ ___/  / _ \/ / _ \/ __ `__ \/ _ \/ __ \/ __/
    / /_/ / /_/ (__  )  /  __/ /  __/ / / / / /  __/ / / / /_
    \__,_/\__,_/____/   \___/_/\___/_/ /_/ /_/\___/_/ /_/\__/


Example Python script for post render hook (post_render.py)
This script will crawl the output for the Job Submission ID and pass it on to the proxy tasks.

"""

import sys
import re


def main(*args):
    # args[0] is a list of all outputs from all the transcoding step items
    job_outputs = args[0]
    job_ids = []

    for job_output in job_outputs:
        if not job_output:
            continue

        match = re.search(r'JobID=([a-zA-Z0-9]*)', job_output)
        if match:
            job_id = match.group(1)
            job_ids.append(job_id)
            print('Job ID:')
            print(job_id)

    # returns data that can later be access as "custom"
    # in this example: <custom.dependency>
    return {'dependency': ','.join(job_ids)}


if __name__ == '__main__':
    main(sys.argv[1:])
