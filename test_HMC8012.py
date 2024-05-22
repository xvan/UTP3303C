import unittest
import UTP330C
import time

class InstanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.utp = UTP330C.HMC8012()
        if(cls.utp is None):
            raise Exception("No UTP330C found")

    @classmethod
    def tearDownClass(cls):
        cls.utp.close()

    def test_autostart(self):
        self.assertIsNotNone(self.utp)


    def test_many(self):
        self.utp.reset()
        self.utp.clear_status()
        self.utp.conf_current_dc_mode()
        print("ESR:", self.utp.get_esr())
        print(self.utp.get_status_byte())
        print("FETCH:", self.utp.fetch())
        print("READ:", self.utp.read())
        self.utp.beep()
        print(self.utp.get_error())
        self.utp.display("Hello, Rey!")

    def test_set_current(self):
        print(self.utp.conf_current_dc_mode())
        print(self.utp.conf_current_dc_mode())



if __name__ == '__main__':
    unittest.main()
