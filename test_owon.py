import unittest
from array import array

import matplotlib.pyplot as plt
import numpy as np

from owon import ResponseStartLength, OwonOsciloscope, ResponseBin, ResponseBinWithHeader, Compensator


class OwonTestCase(unittest.TestCase):

    def test_packet(self):
        data = array('B', [54, 249, 21, 0, 189, 223, 29, 140, 1, 0, 0, 0])
        packet = ResponseStartLength(data)
    def test_bmp(self):
        with OwonOsciloscope() as owon:
            data = owon.ReadBmp()
            self.assertEqual(data[0:2], array('B', b'BM'))
    def test_bin(self):
        with OwonOsciloscope() as owon:
            responses = owon.ReadBin()
            np.savetxt('/tmp/out.csv', np.array(responses[0].sampling_data) * responses[0].voltage_value_per_point * 10 ** responses[0].attenuation_multiplying_power_index)
            #self.assertEqual(2, responses[0].volts_per_div)
            # self.assertEqual(0.5, responses[0].milliseconds_per_div)
            print("time_base", responses[0].time_base_level)
            print("ms per div", responses[0].milliseconds_per_div)
            print("spacing_interval", responses[0].spacing_interval)
            print("calculated_interval", responses[0].calculated_spacing_interval)
            self.assertEqual(responses[0].spacing_interval, responses[0].calculated_spacing_interval)


    def test_osciloscope_file(self):
        with open("dataWithHeader.bin", "rb") as fi:
            data = array('B', fi.read())
            rb = ResponseBinWithHeader(data)
            plt.plot(np.array(rb.sampling_data) * rb.voltage_value_per_point)
        with open("dataWithoutHeader.bin", "rb") as fi:
             data = array('B', fi.read())
             rb = ResponseBin(data, rb.machine_model)
             plt.plot(np.array(rb.sampling_data) * rb.voltage_value_per_point)
        plt.show()

    def test_read_signal(self):
        with OwonOsciloscope() as owon:
            signals = owon.ReadSignal()
            for signal in signals:
                plt.plot( signal[0],signal[1])
            plt.show()

    def test_mean(self):
        with OwonOsciloscope() as owon:
            signals = owon.ReadSignal()
            for signal in signals:
                print(np.mean(signal[1]))


class CompensatorTestCase(unittest.TestCase):
    def test_compensator(self):
        compensator = Compensator("CH1_calibration.csv")
        print(compensator.compensate(3.4))

    def test_data(self):
        compensator = Compensator("CH1_calibration.csv")
        data = np.loadtxt("sample_signal.csv")
        print(data)
        #compensated = compensator.compensate(data)
        #print(compensated)

if __name__ == '__main__':
    unittest.main()
