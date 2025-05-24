# easy_speedfan_linux

A simple Python tool for automatic fan speed control on Linux based on CPU and GPU temperature sensors.

## Features
- Customizable fan control logic via `config.py`
- Supports multiple temperature sensors (CPU, GPU, etc.)
- Flexible PWM calculation functions (linear, quadratic, cubic, exponential, smoothing) — you can also implement your own calculation directly in `config.py`
- Logging with [loguru](https://github.com/Delgan/loguru)
- Can be run as a systemd service

## Installation

### From source

1. Clone this repository:
   ```
   git clone https://github.com/tjmnmk/easy_speedfan_linux.git
   cd easy_speedfan_linux
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure you have permission to write to sysfs (run as root or with sudo).

### Arch Linux package

1. Build and install the package using PKGBUILD (see `archlinux/` or `archlinux_devel/`):
   ```
   cd archlinux
   makepkg -si
   ```
   or
   ```
   cd archlinux_devel
   makepkg -si
   ```
2. The configuration file is installed to `/etc/easy_speedfan_linux/config.py`.
3. The systemd service file is installed to `/usr/lib/systemd/system/easy_speedfan_linux.service`.

## Usage

> **Recommended:** For automatic fan control, use the systemd service. See the [Running as a systemd Service](#running-as-a-systemd-service) section below for details. Manual script execution is not recommended for regular use.

Run the main script manually (not recommended):
```
sudo python easy_speedfan_linux.py
```

or if installed as a package:
```
sudo easy_speedfan_linux
```



### Configuration (`config.py`)
- The `config.py` file contains the main control loop for fan speed regulation.
- You can use any temperature sensor or PWM output that is visible to the `sensors` command from the `lm_sensors` package (not just CPU or GPU sensors).
- Select which temperature sensors and PWM outputs to use (edit the sensor and PWM paths).
- Adjust the temperature-to-PWM mapping (e.g., change the temperature thresholds or the PWM calculation function).
- Add your own logic for how the fan speed should react to temperature readings.
- Example:
  ```python
  pwm_value = easy_speedfan.pwm_calc.linear_pwm(temp_cpu_value, 50, 80, 75, 255)
  if temp_gpu_value > 100 and pwm_value < 170:
      pwm_value = 170
  pwm_value = easy_speedfan.pwm_calc.smooth_pwm(previous_pwm_value, pwm_value)
  ```
- You can modify this logic to suit your hardware and cooling needs.

### Running as a systemd Service
After installing the package, the service file is already in the correct location. Just enable and start the service:
```
sudo systemctl daemon-reload
sudo systemctl enable --now easy_speedfan_linux.service
```

If you install manually, you can use:
```
sudo systemctl enable --now $(pwd)easy_speedfan_linux.service
```

Check the service status:
```
sudo systemctl status easy_speedfan_linux.service
```

## License

This project is licensed under the Beerware License 42.666. See [LICENSE](LICENSE) for details.

## Warning

This program may contain bugs. Incorrect configuration or a bug in the program can damage your computer. Use at your own risk!
