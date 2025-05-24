from dataclasses import dataclass
import sys
from loguru import logger

import sensors
import pwm
import vars
import pwm_calc
import common


class EasySpeedFan:
    def __init__(self):
        self._pwm = pwm
        self._sensors = sensors
        self._pwm_calc = pwm_calc
        self._logger = logger

    @property
    def pwm(self):
        return self._pwm

    @property
    def sensors(self):
        return self._sensors
    
    @property
    def pwm_calc(self):
        return self._pwm_calc
    
    @property
    def logger(self):
        return self._logger
    
@dataclass
class Env:
    """ A simple utility for setting fan speed. """

    config_file: str = "config.py"
    """ The config file to use """

    sensors_cache_ttl: int = 2
    """ The time (in sec) to cache the sensors data """

    sensors_path: str = "sensors"
    """ The path to the sensors command """

def runner(config_file, sensors_cache_ttl, sensors_path):
    assert isinstance(config_file, str)
    assert isinstance(sensors_cache_ttl, int)
    assert isinstance(sensors_path, str)

    # check if config file is valid
    if not config_file.endswith(".py"):
        logger.error("Config file must be a python script", file=sys.stderr)
        sys.exit(1)
    # check if config file readable
    try:
        with open(config_file, "r") as f:
            pass
    except FileNotFoundError:
        logger.error(f"Config file {config_file} not found", file=sys.stderr)
        sys.exit(1)
    
    # try to import the config file
    try:
        config = __import__(config_file[:-3])
    except ImportError:
        logger.error(f"Config file {config_file} is not a valid python script")
        # raise error, logger will catch it and print it
        raise
    
    # check if the config file has a config function
    if not hasattr(config, "config_loop"):
        logger.error(f"Config file {config_file} does not have a config_loop function")
        sys.exit(1)
    
    # set all to vars
    vars.config_file = config_file
    vars.sensors_cache_ttl = sensors_cache_ttl
    vars.sensors_path = sensors_path
    
    # run the config function
    logger.info("Starting config loop", file=sys.stderr)
    config.config_loop(EasySpeedFan())

@logger.catch
def main():
    #logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
    logger.info("Starting Easy SpeedFan")

    config_file = Env.config_file
    sensors_cache_ttl = Env.sensors_cache_ttl
    sensors_path = Env.sensors_path
    try:
        from mininterface import run
        m = run(Env, title="Easy SpeedFan")
        config_file = m.env.config_file
        sensors_cache_ttl = m.env.sensors_cache_ttl
        sensors_path = m.env.sensors_path

        logger.info("mininterface found, use --help to see all options")
    except ImportError:
        m = Env()

        logger.warning("mininterface not found, running with default arguments")
        logger.warning("You can install it with: pip install mininterface")
        logger.warning("You can specify the config file by simple passing it as an first argument")
        # load the config file from args
        if len(sys.argv) > 2:
            logger.error("Too many arguments, only one config file is allowed")
            sys.exit(1)
        elif len(sys.argv) == 2:
            config_file = sys.argv[1]
            logger.info("Config file: %s" % config_file)
        else:
            logger.info("No config file specified, using default: %s" % config_file)

    logger.info("Config file: %s" % config_file)
    logger.info("Sensors cache ttl: %s" % sensors_cache_ttl)
    logger.info("Sensors (binary) path: %s" % sensors_path)

    runner(config_file, sensors_cache_ttl, sensors_path)

if __name__ == "__main__":
    main()
