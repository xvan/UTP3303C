import serial
import os
import glob
import time
from enum import Enum


class Bms:
    def __init__(self, port=None, timeout=0.5):
        self.timeout = timeout
        self.suffix = "\n"
        if port is None:
            port = self._auto_detect("0483:5740")

        self.ser = serial.Serial(port, timeout=timeout)

    def __enter__(self):
        return self

    def close(self):
        self.ser.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _auto_detect(self, vid_pid):
        devices = Bms.vidpid_to_devs(vid_pid)
        if len(devices) == 0: return None
        for device in devices:
            try:
                return device
            except:
                pass
        return None

    @staticmethod
    def vidpid_to_devs(vid_pid):
        vid, pid = map(lambda x: int(x, 16), vid_pid.split(':'))
        uevent_files = glob.glob('/sys/bus/usb/devices/[0-9]*:*/uevent')

        device_paths = []
        for uevent_file in uevent_files:
            with open(uevent_file, 'r') as f:
                for line in f:
                    if f'PRODUCT={vid:x}/{pid:x}' in line:
                        device_path = os.path.dirname(uevent_file)
                        device_paths.append(device_path)
                        break

        dev_names = []
        for path in device_paths:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file in ['dev', 'dev_id']:
                        with open(os.path.join(root, "uevent"), 'r') as f:
                            dev_names += [
                                line.strip().replace('DEVNAME=', '/dev/').replace('INTERFACE=', '')
                                for line in f if line.startswith('DEVNAME=') or line.startswith('INTERFACE=')
                            ]
        return dev_names

    def _read_command(self, cmd):
        time.sleep(self.timeout)
        self._write_command(cmd)
        time.sleep(self.timeout)
        self.ser.readline().strip()
        return self.ser.readline().strip()

    def _write_command(self, cmd):
        time.sleep(self.timeout)
        return self.ser.write((cmd+self.suffix).encode("ascii"))

    def read_adc(self):
        line = self._read_command("read_adc").decode("ascii")
        return [float(field.split("=")[-1]) for field in line.split(" ")]
