import logging
from datetime import datetime
import platform
import sys

if platform.system() == "Linux":
    import pyudev
elif platform.system() == "Windows":
    import win32file
    import win32event
    import win32con
elif platform.system() == "Darwin":
    import os
    import subprocess

def setup_logging():
    """
    Sets up logging to a file and console.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("usb_monitor.log"),
            logging.StreamHandler()
        ]
    )

def monitor_usb_linux():
    """
    Monitors USB device plug-in and removal events on Linux.
    """
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    def usb_device_event(action, device):
        if device.device_type == 'usb_device':
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if action == "add":
                logging.info(f"[{timestamp}] Action: {action}, Device Node: {device.device_node}, Model: {device.get('ID_MODEL')}, Vendor: {device.get('ID_VENDOR')}, Serial: {device.get('ID_SERIAL')}.")
            elif action == "remove":
                logging.info(f"[{timestamp}] Action: {action}, Device Node: {device.device_node}.")

    logging.info("Starting USB device monitor on Linux. Press Ctrl+C to exit.")
    observer = pyudev.MonitorObserver(monitor, callback=usb_device_event)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Exiting USB device monitor.")
        observer.stop()

def monitor_usb_windows():
    """
    Monitors USB device plug-in and removal events on Windows.
    """
    logging.info("Starting USB device monitor on Windows. Press Ctrl+C to exit.")

    volume_handle = win32file.FindFirstChangeNotification(
        "C:\\",
        True,
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
    )

    try:
        while True:
            result = win32event.WaitForSingleObject(volume_handle, 500)
            if result == win32event.WAIT_OBJECT_0:
                logging.info("USB device change detected.")
                win32file.FindNextChangeNotification(volume_handle)
    except KeyboardInterrupt:
        logging.info("Exiting USB device monitor.")
    finally:
        win32file.FindCloseChangeNotification(volume_handle)

def monitor_usb_darwin():
    """
    Monitors USB device plug-in and removal events on macOS.
    """
    logging.info("Starting USB device monitor on macOS. Press Ctrl+C to exit.")

    try:
        while True:
            output = subprocess.run(['system_profiler', 'SPUSBDataType'], stdout=subprocess.PIPE, text=True).stdout
            logging.info("USB devices:")
            logging.info(output)
    except KeyboardInterrupt:
        logging.info("Exiting USB device monitor.")

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
