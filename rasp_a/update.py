#!/usr/bin/python3

import os
def get_abs_path(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, file_name)

# so we get access to shared libs
import sys
sys.path.insert(1, get_abs_path('..'))

# import ds18, bme, sds
import ds18, bme
import rasp_client

# rasp_client.post_update(ds18, bme, sds)
rasp_client.post_update(ds18, bme)
