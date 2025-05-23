from dataclasses import dataclass
import sys

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

def main(config_file, sensors_cache_ttl, sensors_path):
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
    print("Starting config loop", file=sys.stderr)
    config.config_loop(EasySpeedFan())

if __name__ == "__main__":
    config_file = Env.config_file
    sensors_cache_ttl = Env.sensors_cache_ttl
    sensors_path = Env.sensors_path
    try:
        from mininterface import run
        m = run(Env, title="Easy SpeedFan")
        config_file = m.env.config_file
        sensors_cache_ttl = m.env.sensors_cache_ttl
        sensors_path = m.env.sensors_path

        print("mininterface found, use --help to see all options", file=sys.stderr)
    except ImportError:
        m = Env()

        print("mininterface not found, running with default arguments", file=sys.stderr)
        print("You can install it with: pip install mininterface", file=sys.stderr)
        print("You can specify the config file by simple passing it as an first argument", file=sys.stderr)
        # load the config file from args
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
            print("Config file: %s" % config_file, file=sys.stderr)
        else:
            print("No config file specified, using default: %s" % config_file, file=sys.stderr)

    print("Config file: %s" % config_file, file=sys.stderr)
    print("Sensors cache ttl: %s" % sensors_cache_ttl, file=sys.stderr)
    print("Sensors (binary) path: %s" % sensors_path, file=sys.stderr)

    main(config_file, sensors_cache_ttl, sensors_path)