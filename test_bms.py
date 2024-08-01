import unittest
import bms
import time


class InstanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.utp = bms.Bms()
        if(cls.utp is None):
            raise Exception("BMS not found")
    @classmethod
    def tearDownClass(cls):
        cls.utp.close()


    def test_autostart(self):
        self.assertIsNotNone(self.utp)

    def test_hello(self):
        for _ in range(4):
            print(self.utp.read_adc_without_compensation())

    def test_slaves(self):
        for _ in range(4):
            print(self.utp.read_slave_without_compensation())

    def test_slaves_calibrated(self):
        for _ in range(4):
            print(self.utp.read_slave_without_compensation())
            [[slva_ch1,slva_ch2],[slvb_ch1,slvb_ch2]] = self.utp.read_slave()
            print ([[slva_ch1, slva_ch2, slva_ch2 - slva_ch1 ], [slvb_ch1, slvb_ch2,slvb_ch2 -slvb_ch1 ]])

    def test_switch(self):
        self.utp.switch(bms.Bms.SwitchTypeEnum.Charge)
        time.sleep(2)
        self.utp.switch(bms.Bms.SwitchTypeEnum.Discharge)
        time.sleep(2)
        self.utp.switch(bms.Bms.SwitchTypeEnum.Off)
        time.sleep(2)
        print(self.utp.read_adc())

if __name__ == '__main__':
    unittest.main()