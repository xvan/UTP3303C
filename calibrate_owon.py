import time

from UTP330C import UTP330C, HMC8012
from owon import OwonOsciloscope
import numpy as np

with UTP330C() as src, HMC8012() as mult, OwonOsciloscope() as owon:
    mult.reset()

    src.ISET(1, 0.01)
    src.VSET(1, 2.2)
    src.ISET(2, 0)
    src.VSET(2, 0)

    src.OUT(True)

    mult.display('Calibrando Osciloscopio, No Apagar')
    with open(f'owon_calibration.csv', 'w') as f:
        f.write('MULT, CH1, CH2\n')
        for v_src in np.arange(0, 5, 0.01):
            src.VSET(1, v_src)
            time.sleep(20)
            v_meas = mult.read().decode("ascii")
            v_ch1, v_ch2 = [np.mean(signal[1]) / 1000 for signal in owon.ReadSignal()]
            data = f'{v_meas},{v_ch1},{v_ch2}'
            print(data)
            f.write(data + '\n')

    src.OUT(False)
    mult.display('Calibracion Finalizada, Puede Apagar Todo')