import time

from UTP330C import UTP330C, HMC8012
import numpy as np
from datetime import datetime


with UTP330C() as src, HMC8012() as mult:

    mult.reset()

    src.ISET(1, 1.5)
    src.VSET(1, 0)
    src.ISET(2, 0)
    src.VSET(2, 0)

    src.OUT(True)

    with open(f'data_4.csv', 'w') as f:
        f.write('V1, V2\n')
        for v_src in np.arange(0, 5, 0.01):
            src.VSET(1, v_src)
            time.sleep(3)
            v_meas = mult.read().decode("ascii")
            data = f'{v_src}, {v_meas}\n'
            print(v_src, abs(v_src - float(v_meas)), v_meas)
            f.write(data)

    src.OUT(False)
