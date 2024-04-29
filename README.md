# BCD to Seven-Segment Display Clock

Welcome to the BCD to Seven-Segment Display Clock project repository! This project combines the power of Verilog with Python to create a digital clock that simulates a seven-segment display using Binary-Coded Decimal (BCD). Ideal for students and hobbyists interested in digital electronics and embedded system design.

![Clock Display](images/clock-display.png)

## Overview

This project uses a Verilog-based BCD to seven-segment decoder to drive a simulated display, coupled with a Python/Tkinter graphical user interface that shows time updating in real time. It serves as a functional demonstration of how digital hardware can be integrated with software to create educational and practical applications.

### Features

- **Verilog Simulation**: Simulates a BCD to seven-segment decoder.
- **Python GUI**: A real-time updating GUI created with Tkinter.
- **Educational Value**: Perfect for educational purposes to teach digital logic and the workings of embedded systems.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- [Icarus Verilog](http://iverilog.icarus.com/) for Verilog simulation.
- [Python](https://www.python.org/downloads/) (3.6 or newer).
- Tkinter (usually included with Python).

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/bcd-to-seven-segment-clock.git
   cd bcd-to-seven-segment-clock

2. **Run the Verilog simulation**
- Navigate to the project directory and execute:
  ```sh
  iverilog -o simulation.vvp src/bcd_to_7seg.v src/tb_segment7.v
  vvp simulation.vvp
3. **Launch the Python GUI**
  - Execute the following command in the project directory:
    ```sh
    python index.py

## Usage
To use the digital clock, simply run the `index.py` script after following the installation steps. The GUI will display the current time, updating every second, reflecting the real-time operation of the simulated hardware.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
