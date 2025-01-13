import logging
from datetime import datetime
import platform
import sys
import time

if platform.system() == "Linux":
    import pyudev
elif platform.system() == "Windows":
    import win32gui
    import win32con
elif platform.system() == "Darwin":
    import subprocess

def setup_logging():
    """Sets up logging to a file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("usb_monitor.log"),
            logging.StreamHandler()
        ]
    )

def log_usb_event(action, details):
    """Logs USB device events."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{timestamp}] Action: {action}, Details: {details}")

def monitor_usb_linux():
    """Monitors USB device plug-in and removal events on Linux."""
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    def usb_device_event(action, device):
        if device.device_type == 'usb_device':
            details = {
                "Device Node": device.device_node,
                "Model": device.get('ID_MODEL'),
                "Vendor": device.get('ID_VENDOR'),
                "Serial": device.get('ID_SERIAL')
            }
            log_usb_event(action, details)

    logging.info("Starting USB device monitor on Linux. Press Ctrl+C to exit.")
    observer = pyudev.MonitorObserver(monitor, callback=usb_device_event)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exiting USB device monitor.")
        observer.stop()

def monitor_usb_windows():
    """Monitors USB device plug-in and removal events on Windows."""
    def device_change_handler(hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DEVICECHANGE:
            # https://learn.microsoft.com/en-us/windows/win32/devio/dbt-devicearrival
            if wparam == 0x8000:  # DBT_DEVICEARRIVAL
                log_usb_event("add", "USB device connected.")
            # https://learn.microsoft.com/en-us/windows/win32/devio/dbt-deviceremovecomplete
            elif wparam == 0x8004:  # DBT_DEVICEREMOVECOMPLETE
                log_usb_event("remove", "USB device disconnected.")
        return True

    logging.info("Starting USB device monitor on Windows. Press Ctrl+C to exit.")
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = 'USBMonitor'
    wc.lpfnWndProc = device_change_handler
    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(class_atom, 'USBMonitor', 0, 0, 0, 0, 0, 0, 0, 0, None)

    try:
        win32gui.PumpMessages()
    except KeyboardInterrupt:
        logging.info("Exiting USB device monitor.")
    finally:
        win32gui.DestroyWindow(hwnd)

def monitor_usb_darwin():
    """Monitors USB device plug-in and removal events on macOS."""
    logging.info("Starting USB device monitor on macOS. Press Ctrl+C to exit.")

    prev_devices = set()
    try:
        while True:
            output = subprocess.run(['system_profiler', 'SPUSBDataType'], stdout=subprocess.PIPE, text=True).stdout
            current_devices = set(output.split("\n"))

            added = current_devices - prev_devices
            removed = prev_devices - current_devices

            for device in added:
                log_usb_event("add", device)
            for device in removed:
                log_usb_event("remove", device)

            prev_devices = current_devices
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Exiting USB device monitor.")
    except Exception as e:
        logging.error(f"Error monitoring USB devices: {e}")

def main():
    setup_logging()

    os_type = platform.system()
    if os_type == "Linux":
        monitor_usb_linux()
    elif os_type == "Windows":
        monitor_usb_windows()
    elif os_type == "Darwin":
        monitor_usb_darwin()
    else:
        logging.error(f"Unsupported operating system: {os_type}")
        sys.exit(1)

if __name__ == "__main__":
    main()
