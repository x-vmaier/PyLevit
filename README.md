# PyLevit

PyLevit is a Python application designed to interface with an Arduino-based electromagnet levitator system. It provides a graphical user interface (GUI) for controlling and monitoring the levitation process via serial communication with the Arduino.

![PyLevit GUI](https://i.imgur.com/XJ5VNJJ.png)

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Overview

PyLevit serves as the front-end interface for interacting with an Arduino-based electromagnet levitator system. It facilitates real-time control of system parameters such as setpoint, proportional gain, integral gain, and derivative gain, while also providing visual feedback through plots and status indicators.

## Requirements

To run PyLevit, you need:

- Python 3.x
- Required Python packages listed in `requirements.txt`
- An Arduino Nano (ATmega328) with the appropriate firmware installed

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages by running:
   ```
   pip install -r requirements.txt
   ```
3. Ensure your Arduino Nano is connected to your computer.
4. Upload the firmware provided in the Arduino repository to your Arduino Nano.

## Usage

1. Run the `main.py` script:
   ```
   python main.py
   ```
2. PyLevit GUI will open up.
3. Connect your Arduino Nano to the PyLevit GUI via serial communication.
4. Use the GUI to adjust system parameters and monitor the levitation process in real-time.

## Credits

- **Author:** [Valentin Maier](https://github.com/x-vmaier)
- **Institution:** HTL Bulme

## License

This code is licensed under the [MIT License](LICENSE). Feel free to use, modify, or distribute it according to the terms of the license.

For more details, refer to the [PyLevit repository](https://github.com/x-vmaier/PyLevit) for integrating the levitator system with the graphical user interface.