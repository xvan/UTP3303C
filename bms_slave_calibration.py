import time

from UTP330C import UTP330C, HMC8012
from owon import OwonOsciloscope
from bms import Bms
import numpy as np


with UTP330C() as src, HMC8012() as mult, Bms() as bms:
    mult.reset()

    MIN = 2.2
    ADD_MAX = 7.4

    src.ISET(1, 0.1)
    src.ISET(2, 0.1)
    src.VSET(1, MIN)
    src.VSET(2, MIN)

    src.OUT(True)

    with open(f'slave_raw_bms_cal_ch2fix3.7.csv', 'w') as f:
        f.write("v_src_ch1,v_meas_ch2,slA_ch1,slA_ch2,slB_ch1,slB_ch2\n")
        # Muevo C2
        src.VSET(2, 3.7)
        for ch1_v in [ x/100 for x in  range(220, 370)]:
            src.VSET(1, ch1_v)
            time.sleep(2)
            v_meas = float(mult.read().decode("ascii"))
            [[slA_ch1,slA_ch2],[slB_ch1,slB_ch2]] = bms.read_slave_without_compensation()
            data = f'{ch1_v:.3f}, {v_meas:.3f}, {slA_ch1:.3f}, {slA_ch2:.3f}, {slB_ch1:.3f}, {slB_ch2:.3f}'
            f.write(data + '\n')
            print(data)

        src.OUT(False)
        mult.display('Calibracion Finalizada, Puede Apagar Todo')
