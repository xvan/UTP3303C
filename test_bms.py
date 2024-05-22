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

if __name__ == '__main__':
    unittest.main()