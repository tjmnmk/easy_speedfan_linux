import time
import sys

def config_loop_example(easy_speedfan):
    #### EDIT THIS FILE AND REMOVE THE NEXT LINE
    easy_speedfan.logger.error("Not configured, exiting"); sys.exit(1)
    ############################################

    temp_cpu = easy_speedfan.sensors.TemperatureSensor("coretemp-isa-0000", "Package id 0", "temp1_input")
    temp_gpu = easy_speedfan.sensors.TemperatureSensor("amdgpu-pci-0500", "junction", "temp2_input")

    pwm_cpu2 = easy_speedfan.pwm.PWM("/sys/devices/platform/nct6775.2608/hwmon/hwmon3/", "pwm2")

    pwm_cpu2.enable_fan_control()

    previous_pwm_value = 0
    try:
        while True:
            easy_speedfan.logger.info("Config loop")

            # get the temperature
            temp_cpu_value = temp_cpu.get_temperature()
            temp_gpu_value = temp_gpu.get_temperature()

            # print the temperature
            easy_speedfan.logger.info(f"CPU temp: {temp_cpu_value}")
            easy_speedfan.logger.info(f"GPU temp: {temp_gpu_value}")

            pwm_value = easy_speedfan.pwm_calc.linear_pwm(temp_cpu_value, 50, 80, 75, 255)
            if temp_gpu_value > 100 and pwm_value < 170:
                pwm_value = 170

            # smooth the pwm value
            pwm_value = easy_speedfan.pwm_calc.smooth_pwm(previous_pwm_value, pwm_value)

            # set the pwm value
            pwm_cpu2.set_pwm_value(pwm_value)

            # print the pwm value
            easy_speedfan.logger.info(f"PWM value: {pwm_value}", file=sys.stderr)
            # set the previous pwm value
            previous_pwm_value = pwm_value

            # sleep for the loop sleep time
            time.sleep(1)
    finally:
        easy_speedfan.logger.error("Error occurred, disabling fan control", file=sys.stderr)
        pwm_cpu2.disable_fan_control()
        easy_speedfan.logger.error("Fan control disabled", file=sys.stderr)
        # easy_speedfan_linux will catch the error and print it
        
        



