import time

from UTP330C import UTP330C, HMC8012
from owon import OwonOsciloscope
from bms import Bms
import numpy as np


with UTP330C() as src, HMC8012() as mult, Bms() as bms:
    mult.reset()
    mult.conf_current_dc_mode()

    src.VSET(1, 3)
    src.ISET(1, 0)

    src.VSET(2, 13.6)
    src.ISET(2, 0.8)

    #bms.switch(Bms.SwitchTypeEnum.Discharge)
    bms.switch(Bms.SwitchTypeEnum.Charge)

    src.OUT(True)

    with open(f'raw_bms_charge_cal.csv', 'w') as f:
        f.write("i_src,i_meas,v_up,v_down,v_current,old_up,old_down,old_current\n")
        for i_src in [ x/100 for x in  range(0, 300)]:
            src.ISET(1, i_src)
            time.sleep(2)
            i_meas = float(mult.read().decode("ascii"))
            bms.read_adc_without_compensation()
            bms.read_adc_without_compensation()
            v_up, v_down, v_current, old_up, old_down, old_curr = bms.read_adc_without_compensation()
            #i_meas *= -1 # Negativo en la carga
            data = f'{i_src:.3f}, {i_meas:.3f}, {v_up:.3f}, {v_down:.3f}, {v_current:.3f}, {old_up:.3f}, {old_down:.3f}, {old_curr:.3f}'
            f.write(data + '\n')
            print(data)

        src.OUT(False)
        mult.display('Calibracion Finalizada, Puede Apagar Todo')
