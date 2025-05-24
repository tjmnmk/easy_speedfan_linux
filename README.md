# easy_speedfan_linux

A simple Python tool for automatic fan speed control on Linux based on CPU and GPU temperature sensors.

## Features
- Customizable fan control logic via `config.py`
- Supports multiple temperature sensors (CPU, GPU, etc.)
- Flexible PWM calculation functions (linear, quadratic, cubic, exponential, smoothing) — you can also implement your own calculation directly in `config.py`
- Logging with [loguru](https://github.com/Delgan/loguru)
- Can be run as a systemd service

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/easy_speedfan_linux.git
   cd easy_speedfan_linux
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure you have permission to write to sysfs (run as root or with sudo).

## Usage

Run the main script:
```
sudo python easy_speedfan_linux.py
```

### Configuration (`config.py`)
- The `config.py` file contains the main control loop for fan speed regulation.
- Select which temperature sensors and PWM outputs to use (edit the sensor and PWM paths).
- Adjust the temperature-to-PWM mapping (e.g., change the temperature thresholds or the PWM calculation function).
- Add your own logic for how the fan speed should react to CPU/GPU temperature.
- Example:
  ```python
  pwm_value = easy_speedfan.pwm_calc.linear_pwm(temp_cpu_value, 50, 80, 75, 255)
  if temp_gpu_value > 100 and pwm_value < 170:
      pwm_value = 170
  pwm_value = easy_speedfan.pwm_calc.smooth_pwm(previous_pwm_value, pwm_value)
  ```
- You can modify this logic to suit your hardware and cooling needs.

### Running as a systemd Service
You have two options:

1. Copy `easy_speedfan_linux.service` to `/etc/systemd/system/` and adjust paths if needed:
   ```
   sudo cp easy_speedfan_linux.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now easy_speedfan_linux.service
   ```
   
   Or, alternatively, you can enable the service directly from your project directory without copying:
   ```
   sudo systemctl enable --now $(pwd)/easy_speedfan_linux.service
   ```
2. Check status:
   ```
   sudo systemctl status easy_speedfan_linux.service
   ```

## License

This project is licensed under the Beerware License. See [LICENSE](LICENSE) for details.

## Warning

This program is not production quality and may contain bugs. Incorrect configuration or a bug in the program can damage your computer. Use at your own risk!
