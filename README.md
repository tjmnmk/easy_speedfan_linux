# easy_speedfan_linux

A simple Python tool for automatic fan speed control on Linux based on CPU and GPU temperature.

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run as root or with sufficient permissions to write to sysfs.

## Usage

Run the main script:
```
sudo python easy_speedfan_linux.py
```

### Configuration (`config.py`)

The `config.py` file contains the main control loop for fan speed regulation. Here you can:
- Select which temperature sensors and PWM outputs to use (edit the sensor and PWM paths).
- Adjust the temperature-to-PWM mapping (e.g., change the temperature thresholds or the PWM calculation function).
- Add your own logic for how the fan speed should react to CPU/GPU temperature.

Example (from `config.py`):
```python
pwm_value = easy_speedfan.pwm_calc.linear_pwm(temp_cpu_value, 45, 75, 0, 255)
if temp_gpu_value > 100 and pwm_value < 170:
    pwm_value = 170
```
You can modify this logic to suit your hardware and cooling needs.

## Warning

This program is not production quality and may contain bugs. Incorrect configuration or a bug in the program can damage your computer. Use at your own risk!
