# USB Device Monitor
#Some Screenshots of it in action 
![usb_monitor](https://github.com/user-attachments/assets/09ce3a7f-0682-47e4-b6bd-1311e4b541e4)


A cross-platform Python script for monitoring USB device plug-in and removal events on Linux, Windows, and macOS.

## Features

- Logs USB device connections and disconnections.
- Supports Linux, Windows, and macOS.
- Outputs logs to both the console and a file (`usb_monitor.log`).
- Graceful termination with Ctrl+C.

## Requirements

### Linux
- Python 3.x
- `pyudev` library

### Windows
- Python 3.x
- `pywin32` library

### macOS
- Python 3.x

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/BaseMax/USB-device-monitor.git
   cd USB-device-monitor
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script directly:

```bash
python usb_device_monitor.py
```

The script will start monitoring USB devices and log events to the console and `usb_monitor.log`.

## How It Works

- **Linux**: Uses the `pyudev` library to monitor USB device events.
- **Windows**: Utilizes the Windows API to handle USB device changes.
- **macOS**: Leverages `system_profiler` to detect USB device state changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

© 2025 Max Base

GitHub: [BaseMax](https://github.com/BaseMax)
