import pyudev
import logging
from datetime import datetime

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

def usb_device_event(action, device):
    """
    Callback function to handle USB device events.

    Args:
        action (str): The action performed (add, remove, etc.).
        device (Device): The udev device object representing the USB device.
    """
    if device.device_type == 'usb_device':
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if action == "add":
            logging.info(f"[{timestamp}] Action: {action}, Device Node: {device.device_node}, Model: {device.get('ID_MODEL')}, Vendor: {device.get('ID_VENDOR')}, Serial: {device.get('ID_SERIAL')}.")
        elif action == "remove":
            logging.info(f"[{timestamp}] Action: {action}, Device Node: {device.device_node}.")

def monitor_usb_devices():
    """
    Monitors USB device plug-in and removal events.
    """
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    logging.info("Starting USB device monitor. Press Ctrl+C to exit.")
    observer = pyudev.MonitorObserver(monitor, callback=usb_device_event)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Exiting USB device monitor.")
        observer.stop()

if __name__ == "__main__":
    setup_logging()
    monitor_usb_devices()