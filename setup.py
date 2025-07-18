from setuptools import setup, find_packages

setup(
    name="easy_speedfan_linux",
    version="1.0.2",
    description="Automatic fan speed control for Linux based on CPU/GPU temperature sensors.",
    author="Adam Bambuch",
    author_email="adam.bambuch2@gmail.com",
    url="https://github.com/tjmnmk/easy_speedfan_linux",
    license="Beerware 42.666",
    py_modules=[
        "easy_speedfan_linux",
        "config",
        "pwm_calc",
        "pwm",
        "sensors",
        "sensors_loader",
        "vars"
    ],
    install_requires=[
        "cachetools",
        "loguru",
        "mininterface"
    ],
    data_files=[
        ("share/easy_speedfan_linux", ["pwm_calc.py", "pwm.py", "sensors.py", "sensors_loader.py", "vars.py", "requirements.txt", "config.py"]),
        ("share/doc/easy_speedfan_linux", ["README.md", "config.py", "easy_speedfan_linux.service"]),
        ("share/licenses/easy_speedfan_linux", ["LICENSE"]),
    ],
    entry_points={
        "console_scripts": [
            "easy_speedfan_linux = easy_speedfan_linux:main"
        ]
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
