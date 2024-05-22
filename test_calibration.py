import time

from UTP330C import UTP330C, HMC8012
from owon import OwonOsciloscope
from bms import Bms
import numpy as np


with UTP330C() as src, HMC8012() as mult, OwonOsciloscope() as owon, Bms() as bms:
    mult.reset()

    src.ISET(1, 0.1)
    src.VSET(1, 2.2)
    src.ISET(2, 0)
    src.VSET(2, 0)

    src.OUT(True)

    with open(f'all_calibration8a16_vpow.csv', 'w') as f:
        for v_src in [ x/100 for x in  range(800, 1600)]:
            src.VSET(1, v_src)
            time.sleep(2)
            v_meas = float(mult.read().decode("ascii"))
            v_ch1, v_ch2 = owon.calc_mean()
            v_up, v_down, i = bms.read_adc()

            data = f'{v_src:.3f}, {v_meas:.3f}, {v_ch1:.3f}, {v_ch2:.3f}, {v_up:.3f}, {v_down:.3f}'
            f.write(data + '\n')
            print(data)

        src.OUT(False)
        mult.display('Calibracion Finalizada, Puede Apagar Todo')
