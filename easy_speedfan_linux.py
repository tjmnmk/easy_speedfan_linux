from dataclasses import dataclass
from mininterface import run
import time

import sensors
import pwm
import vars
import pwm_calc


class EasySpeedFan:
    def __init__(self):
        self._pwm = pwm
        self._sensors = sensors
        self._pwm_calc = pwm_calc

    @property
    def pwm(self):
        return self._pwm

    @property
    def sensors(self):
        return self._sensors
    
    @property
    def pwm_calc(self):
        return self._pwm_calc
    

@dataclass
class Env:
    """ A simple utility for setting fan speed. """

    config_file: str = "config.py"
    """ The config file to use """

    sensors_cache_ttl: int = 2
    """ The time (in sec) to cache the sensors data """

    sensors_path: str = "sensors"
    """ The path to the sensors command """

    loop_sleep: int = 1
    """ The time (in sec) to sleep between loops """

def main(config_file, sensors_cache_ttl, sensors_path, loop_sleep):
    # check if the config file exists
    if config_file is None:
        raise ValueError("Config file is required")
    # check if config file is valid
    if not config_file.endswith(".py"):
        raise ValueError("Config file must be a python script")
    # check if config file readable
    try:
        with open(config_file, "r") as f:
            pass
    except FileNotFoundError:
        raise ValueError(f"Config file {config_file} not found")
    
    # try to import the config file
    try:
        config = __import__(config_file[:-3])
    except ImportError:
        raise ValueError(f"Config file {config_file} is not a valid python script")
    
    # check if the config file has a config function
    if not hasattr(config, "config_loop"):
        raise ValueError(f"Config file {config_file} does not have a config_loop function")
    
    # set all to vars
    vars.config_file = config_file
    vars.sensors_cache_ttl = sensors_cache_ttl
    vars.sensors_path = sensors_path
    
    # run the config function
    config.config_loop(EasySpeedFan())


if __name__ == "__main__":
    m = run(Env, title="My application")

    main(m.env.config_file, m.env.sensors_cache_ttl, m.env.sensors_path, m.env.loop_sleep)