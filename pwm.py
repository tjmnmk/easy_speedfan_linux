import os

class PWM:
    def __init__(self, sys_directory, pwm_id, pwm_enable_path = None, pwm_control_path = None):
        # check if the sys directory exists
        if not os.path.exists(sys_directory):
            raise ValueError(f"Sys directory {sys_directory} not found")
        
        pwm_control_path_comp = pwm_control_path
        if pwm_control_path_comp is None:
            pwm_control_path_comp = os.path.join(sys_directory, pwm_id)

        pwm_enable_path_comp = pwm_enable_path
        if pwm_enable_path_comp is None:
            pwm_enable_path_comp = os.path.join(sys_directory, pwm_id + "_enable")

        # check if the pwm control path exists
        if not os.path.exists(pwm_control_path_comp):
            raise ValueError(f"PWM control path {pwm_control_path_comp} not found")
        
        # check if the pwm enable path exists
        if not os.path.exists(pwm_enable_path_comp):
            raise ValueError(f"PWM enable path {pwm_enable_path_comp} not found")
        
        self._pwm_control_path = pwm_control_path_comp
        self._pwm_enable_path = pwm_enable_path_comp

    def enable_fan_control(self, enable_value = 1):
        """
        Enable the fan control

        :param enable_value: The value to set the pwm enable path to (default is 1)
        """
        self._set_pwm_control_id(enable_value)

    def disable_fan_control(self, disable_id = 5):
        """
        Disable the fan control
        
        :param disable_id: The value to set the pwm enable path to (default is 5)
        """
        self._set_pwm_control_id(disable_id)

    def set_pwm_value(self, pwm_value):
        """
        Set the pwm value

        :param pwm_value: The value to set the pwm control path to
        """
        # check if the pwm value is valid
        if not isinstance(pwm_value, int):
            raise ValueError(f"PWM value {pwm_value} is not a valid integer")
        
        # set the pwm value
        with open(self._pwm_control_path, "w") as f:
            f.write(str(pwm_value))
        f.close()


    def _set_pwm_control_id(self, pwm_control_id):
        """
        Set the pwm control id
        """
        # check if the pwm control id is valid
        if not isinstance(pwm_control_id, int):
            raise ValueError(f"PWM control id {pwm_control_id} is not a valid integer")
        
        # set the pwm control id
        print(self._pwm_enable_path, pwm_control_id)
        with open(self._pwm_enable_path, "w") as f:
            f.write(str(pwm_control_id))
        f.close()