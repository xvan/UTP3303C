import serial
import os
import glob
import time
from enum import Enum

class UTP330C:
    def __init__(self, port=None, timeout=0.05):
        self.port = port
        self.timeout = timeout

        if self.port is None:
            self.port = self._auto_detect()

        self.ser = serial.Serial(self.port, timeout=timeout)

        if b"P3303C%**" != self.IDN():
            raise Exception("UTP330C not found on port: "+port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.ser.close()

    def _auto_detect(self):
        vid_pid = "5345:1234"
        devices = UTP330C.vidpid_to_devs(vid_pid)
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

    def VSET(self, channel, value):
        return self._write_command(f'VSET{channel}:{value}')

    def ISET(self, channel, value):
        return self._write_command(f'ISET{channel}:{value}')

    def VGET(self, channel):
        return float(self._read_command(f'VSET{channel}?'))

    def IGET(self, channel):
        return float(self._read_command(f'ISET{channel}?'))

    def LOCK(self, status):
        return self._write_command(f'LOCK{int(status)}')

    def VOUT(self, channel):
        return float(self._read_command(f'VOUT{channel}?'))

    def IOUT(self, channel):
        return float(self._read_command(f'IOUT{channel}?'))

    def OUT(self, status):
        rval = self._write_command(f'OUT{int(status)}')
        time.sleep(0.1) # Wait for the output to stabilize
        return rval

    def BEEP(self, status):
        return self._write_command(f'BEEP{int(status)}')

    def STATUS(self):
        return STATUS(self._read_command('STATUS?')[0])

    def IDN(self):
        return self._read_command('*IDN?')

    def RECALL(self, number):
        return self._write_command(f'RCL{number}')

    def SAVE(self, number):
        return self._write_command(f'SAV{number}')

    def TRACK(self, number):
        return self._write_command(f'TRACK{number}')

    def Set_OCP(self, status):
        return self._write_command(f'OCP{int(status)}')

    def Get_OCP(self):
        return self._read_command('OCP?')

    def Set_OVP(self, status):
        return self._write_command(f'OVP{int(status)}')

    def Get_OVP(self):
        return self._read_command('OVP?')

    def OCPSTE(self, channel, value):
        return self._write_command(f'OCPSTE{channel}:{value}')

    def OVPSTE(self, channel, value):
        return self._write_command(f'OVPSTE{channel}:{value}')

    def _write_command(self, cmd):
        time.sleep(self.timeout)
        return self.ser.write(cmd.encode("ascii"))

    def _read_command(self, cmd):
        time.sleep(self.timeout)
        self._write_command(cmd)
        time.sleep(self.timeout)
        return self.ser.readline()

    class TrackEnum(Enum):
        INDEPENDENT = 0
        SERIES = 1
        PARALLEL = 2

class STATUS():
    def __init__(self, status: int):
        self.status = status
        self.ch1_mode = STATUS.ChannelModeEnum(self.status & 0b1)
        self.ch2_mode = STATUS.ChannelModeEnum((self.status >> 1) & 0b1)
        self.output = STATUS.OutputStatus((self.status >> 6) & 0b1)

    def __str__(self):
        return f"STATUS: {self.status}, CH1: {self.ch1_mode}, CH2: {self.ch2_mode}, OUT: {self.output}"

    class ChannelModeEnum(Enum):
        CV = 0
        CC = 1

    class OutputStatus(Enum):
        OFF = 0
        ON = 1







