import unittest
import UTP330C
import time

class StaticTests(unittest.TestCase):
    def test_load(self):
        UTP330C.UTP330C('/dev/ttyACM0')

    def test_vpid_to_dev(self):
        vid_pid = "5345:1234"  # Example VID:PID
        devices = UTP330C.UTP330C.vidpid_to_devs(vid_pid)
        self.assertTrue(len(devices) > 0)


class InstanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.utp = UTP330C.UTP330C()
        if(cls.utp is None):
            raise Exception("No UTP330C found")

    @classmethod
    def tearDownClass(cls):
        cls.utp.close()

    def test_autostart(self):
        self.assertIsNotNone(self.utp)

    def test_vset(self):
        self.utp.VSET(1, 4)
        self.assertEqual(4, self.utp.VGET(1))
        self.utp.VSET(1, 5)
        self.assertEqual(5, self.utp.VGET(1))
        self.utp.VSET(2, 4)
        self.assertEqual(4, self.utp.VGET(2))
        self.utp.VSET(2, 5)
        self.assertEqual(5, self.utp.VGET(2))

    def test_iget(self):
        self.utp.ISET(1, 0.1)
        self.assertEqual(self.utp.IGET(1), 0.1)
        self.utp.ISET(1, 0.4)
        self.assertEqual(self.utp.IGET(1), 0.4)
        self.utp.ISET(2, 0.1)
        self.assertEqual(self.utp.IGET(2), 0.1)
        self.utp.ISET(2, 0.4)
        self.assertEqual(self.utp.IGET(2), 0.4)

    def test_round(self):
        self.utp.OUT(False)

        self.utp.VSET(1, 1.1)
        self.utp.VSET(2, 2.2)

        self.assertEqual(self.utp.VOUT(1), 0.0)
        self.assertEqual(self.utp.VOUT(2), 0.0)
        self.assertEqual(self.utp.IOUT(1), 0.0)
        self.assertEqual(self.utp.IOUT(2), 0.0)
        self.assertEqual(self.utp.STATUS().output, UTP330C.STATUS.OutputStatus.OFF)

        self.utp.OUT(True)
        self.utp.BEEP(True)

        self.assertEqual(self.utp.VOUT(1), 1.1)
        self.assertEqual(self.utp.VOUT(2), 2.2)
        self.assertEqual(self.utp.IOUT(1), 0.0)
        self.assertEqual(self.utp.IOUT(2), 0.0)
        self.assertEqual(self.utp.STATUS().output, UTP330C.STATUS.OutputStatus.ON)

        self.utp.OUT(False)

        self.assertEqual(self.utp.VOUT(1), 0.0)
        self.assertEqual(self.utp.VOUT(2), 0.0)
        self.assertEqual(self.utp.IOUT(1), 0.0)
        self.assertEqual(self.utp.IOUT(2), 0.0)
        self.assertEqual(self.utp.STATUS().output, UTP330C.STATUS.OutputStatus.OFF)

    def test_tracks(self):
        self.utp.TRACK(UTP330C.UTP330C.TrackEnum.INDEPENDENT)
        self.utp.TRACK(UTP330C.UTP330C.TrackEnum.SERIES)
        self.utp.TRACK(UTP330C.UTP330C.TrackEnum.PARALLEL)

    def test_overprotections(self):
        self.utp.Set_OVP(True)
        print(self.utp.Get_OVP())
        self.utp.Set_OVP(False)
        print(self.utp.Get_OVP())
        self.utp.Set_OCP(True)
        self.utp.Set_OCP(False)

if __name__ == '__main__':
    unittest.main()
