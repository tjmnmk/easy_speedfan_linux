"""

Loads the sensors data from sensors -j

"""

import json
import os
import subprocess
import cachetools

import vars

# TODO: use ttl time from vars
@cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=1))
def load_sensors_data():
    """
    Loads the sensors data from sensors -j
    """
    sensors_path = vars.sensors_path

    # run the sensors command
    try:
        output = subprocess.check_output([sensors_path, "-j"])
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Sensors command {sensors_path} failed: {e}")
    
    # parse the output
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Sensors command {sensors_path} output is not valid JSON: {e}")
    
    return data
