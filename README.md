# ARGBB Project

[![wakatime](https://wakatime.com/badge/user/018ed2aa-e4fd-4336-bab8-464a091e41b7/project/8889d00d-fe2c-4e77-a79c-585d6f138f1a.svg)](https://wakatime.com/badge/user/018ed2aa-e4fd-4336-bab8-464a091e41b7/project/8889d00d-fe2c-4e77-a79c-585d6f138f1a)

## Overview

The ARGBB project is a MicroPython-based application designed for the Raspberry Pi Pico W. It provides a web interface for configuring WiFi settings and controlling various LED effects on an RGB LED strip.

## Features

- WiFi setup and management
- Multiple LED effects including pulse, fill, meteor, and rainbow train
- Web interface for controlling LED modes, speeds, and colors
- Button input handling for mode and speed changes

## Project Structure

- `wireless/`: Contains files related to WiFi management and HTTP server.
- `modes/`: Contains different LED modes and strategies for changing modes and speeds.
- `led_effects/`: Contains implementations of various LED effects.
- `utils.py`: Utility functions used across the project.
- `config.py`: Configuration settings for the LED strip.
- `app.py`: Main application logic.
- `input_controller.py`: Handles input from buttons and web interface.

## Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/argbb.git
   cd argbb
   ```

2. **Install MicroPython with mDNS support on Raspberry Pi Pico W:**
   Follow the instructions to install the custom MicroPython build from [micropython-mdns](https://github.com/cbrand/micropython-mdns.git).

3. **Upload the project files to the Pico W:**
   Use a tool like [Thonny](https://thonny.org/) or [rshell](https://github.com/dhylands/rshell) to upload the files to the Pico W.

4. **Connect the LED strip:**

   - Connect the data pin of the LED strip to the GPIO pin defined in `config.py` (default is pin 15).
   - Connect the power and ground pins accordingly.

5. **Run the application:**
   - Open a terminal or Thonny and run the `main.py` script.

## Acknowledgments

This project uses a modified version of the [micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater) for over-the-air updates.

## Usage

### Web Interface

- Access the web interface by connecting to the Pico W's WiFi access point and navigating to `http://192.168.4.1` in your browser.
- Once WiFi is set up, you can access the web interface using `http://argbb.local` or ip.
- Use the interface to select WiFi networks, change LED modes, speeds, and colors.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Future Features

- Enhanced web interface with more customization options
- More LED effects
- Custom settings not hardcoded
- Power-On Self-Test (POST) to verify hardware functionality
- Master/slave interface for multiple controllers sync
- Custom modes
- Custom speed and color in web UI
- Add ota updates

## Known Issues

- ~~Application crashes when SSID is in Cyrillic~~
- Issues with colors in long strips
- Slow response on mode change

## License

This project is licensed under the MIT License.
