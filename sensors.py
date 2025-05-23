import time

import sensors_loader

class TemperatureSensor:
    def __init__(self, sensor_module, sensor_adapter, sensor_id):
        self._sensor_module = sensor_module
        self._sensor_adapter = sensor_adapter
        self._sensor_id = sensor_id

    def get_temperature(self):
        """
        Get the temperature of the sensor
        """
        # get the sensors data
        data = sensors_loader.load_sensors_data()
        # get the sensor data
        try:
            sensor_data = data[self._sensor_module][self._sensor_adapter][self._sensor_id]
        except KeyError:
            raise ValueError(f"Sensor {self._sensor_module} {self._sensor_adapter} {self._sensor_id} not found, check the sensors -j output")
        try:
            temperature = int(sensor_data)
        except ValueError:
            raise ValueError(f"Sensor {self._sensor_module} {self._sensor_adapter} {self._sensor_id} is not a valid temperature sensor, check the sensors -j output")
        
        return temperature