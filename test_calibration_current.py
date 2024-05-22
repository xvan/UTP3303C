import time

from UTP330C import UTP330C, HMC8012
from owon import OwonOsciloscope
from bms import Bms
import numpy as np


with UTP330C() as src, HMC8012() as mult, OwonOsciloscope() as owon, Bms() as bms:
    mult.reset()
    mult.conf_current_dc_mode()
    # src.ISET(1, 0)
    # src.VSET(1, 10)
    # src.ISET(2, 0.1)
    # src.VSET(2, 8)
    # src._write_command(f'TRACK2')
    #src.OUT(True)

    with open(f'all_calibration8a16_curr_minus.csv', 'w') as f:
        for i_src in [ x/1000 for x in range(0, 2000, 100)]:
            #src.ISET(2, i_src)
            time.sleep(2)
            i_meas = float(mult.read().decode("ascii"))
            v_ch1, v_ch2 = owon.calc_mean()
            v_up, v_down, i_sense = bms.read_adc()
            v_up2, v_down2, i_sense2 = bms.read_adc_without_compensation()

            #data = f'{i_src:.3f}, {i_meas:.3f}, {v_ch1:.3f}, {v_ch2:.3f}, {v_up:.3f}, {v_down:.3f}, {i_sense:.3f}'
            data = f'{i_src*2:.3f}, {i_meas:.3f},{i_sense2:.3f}, {i_sense:.3f}, {abs(i_meas - i_sense):.3f}'
            f.write(data + '\n')
            print(data)

        #src.OUT(False)
        mult.display('Calibracion Finalizada, Puede Apagar Todo')

