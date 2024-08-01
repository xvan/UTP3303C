import serial
import os
import glob
import time
from enum import Enum
from compensator import Compensator

class Bms:
    def __init__(self, port=None, timeout=0.5):
        self.timeout = timeout
        self.suffix = "\n"
        self.compensator = {
            "VBAT": Compensator("VBAT_calibration.csv"),
            "VPOW": Compensator("VPOW_calibration.csv"),
            "IBAT": Compensator("IBAT_calibration.csv"),
            "SLVA_CH1": Compensator("SLVA_CH1_calibration.csv"),
            "SLVB_CH1": Compensator("SLVB_CH1_calibration.csv"),
            "SLVA_CH2": Compensator("SLVA_CH2_calibration.csv"),
            "SLVB_CH2": Compensator("SLVB_CH2_calibration.csv")
        }

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

    def _read_command2(self, cmd):
        time.sleep(self.timeout)
        self._write_command(cmd)
        time.sleep(self.timeout)
        self.ser.readline().strip()
        return [ self.ser.readline().strip(), self.ser.readline().strip() ]

    def _write_command(self, cmd):
        time.sleep(self.timeout)
        return self.ser.write((cmd+self.suffix).encode("ascii"))

    def read_adc_without_compensation(self):
        line = self._read_command("read_adc").decode("ascii")
        return [float(field.split("=")[-1]) for field in line.split(" ")]

    #fixme: unificar con write_command
    def _execute_command(self, cmd: str):
        retval = self._write_command(cmd)
        time.sleep(self.timeout)
        print( self.ser.readline().strip())
        return retval

    class SwitchTypeEnum(Enum):
        Charge = 0
        Discharge = 1
        Off = 1
    def switch(self, state : SwitchTypeEnum):
        if state == Bms.SwitchTypeEnum.Charge:
            self._read_command("switch charge")
        elif state == Bms.SwitchTypeEnum.Discharge:
            self._read_command("switch discharge")
        elif state == Bms.SwitchTypeEnum.Off:
            self._read_command("switch off")
        else:
            raise ValueError("Invalid state")



    def read_adc(self):
        uncomp = self.read_adc_without_compensation()
        return [self.compensator["VBAT"].compensate(uncomp[0]),
                self.compensator["VPOW"].compensate(uncomp[1]),
                self.compensator["IBAT"].compensate(uncomp[2])]

    def read_slave_without_compensation(self):
        result = []
        for line in self._read_command2("read_slave 1"):
            dec_line = line.decode("ascii")
            voltages =  dec_line.split(",")[2:4]
            result.append([ float(voltage.split(":")[-1].strip()) for voltage in voltages])
        return result

    def read_slave(self):
        [[slvA_ch1, slvA_ch2], [slvB_ch1, slvB_ch2]] = self.read_slave_without_compensation()
        return [[self.compensator["SLVA_CH1"].compensate(slvA_ch1),
                self.compensator["SLVA_CH2"].compensate(slvA_ch2)],
                [self.compensator["SLVB_CH1"].compensate(slvB_ch1),
                self.compensator["SLVB_CH2"].compensate(slvB_ch2)]]