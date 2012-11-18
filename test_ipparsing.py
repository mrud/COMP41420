import unittest
from IPStorage import DB
V4 = DB.IPv4

class IPParsingTests(unittest.TestCase):
    def test_onedot(self):
        input_ip = "65"
        ip, netmask = V4.normalize(input_ip)
        self.assertEqual(netmask, 8, "Netmask is wrong")
        self.assertEqual(ip, 0x41000000)

    def test_onedot_netmask(self):
        input_ip =  "65/17"
        ip, netmask =  V4.normalize(input_ip)
        self.assertEqual(netmask, 17)
        self.assertEqual(ip, 0x41000000)

    def test_twodot(self):
        input_ip =  "65.1"
        ip, netmask =  V4.normalize(input_ip)
        self.assertEqual(netmask, 16)
        self.assertEqual(ip, 0x41010000)

    def test_threedot(self):
        input_ip =  "65.0.1"
        ip, netmask =  V4.normalize(input_ip)
        self.assertEqual(netmask, 24)
        self.assertEqual(ip, 0x41000100)

    def test_ip(self):
        input_ip =  "127.0.0.1"
        ip, netmask =  V4.normalize(input_ip)
        self.assertEqual(netmask, 32, "Netmask should be 32 for full ip address")
        self.assertEqual(ip, 0x7F000001)

    def test_ip_netmask(self):
        input_ip =  "127.0.0.1/24"
        ip, netmask =  V4.normalize(input_ip)
        self.assertEqual(netmask, 24, "Netmask should be 32 for full ip address")
        self.assertEqual(ip, 0x7F000001)

    def test_invalid_netmask(self):
        input_ip = "127.0.0.1/33"
        self.assertRaises(ValueError, V4.normalize, input_ip)

        input_ip = "127.0.0.1/-1"
        self.assertRaises(ValueError, V4.normalize, input_ip)

        input_ip = "127.0.0.1/-1/5"
        self.assertRaises(ValueError, V4.normalize, input_ip)

    def test_invalid_ips(self):
        self.assertRaises(ValueError, V4.normalize, "")
        self.assertRaises(ValueError, V4.normalize, "1.2.3.4.5")
        self.assertRaises(ValueError, V4.normalize, "a")
        self.assertRaises(ValueError, V4.normalize, "256")

    def test_netmask(self):
        input_ip = "127.0.0.1/0"
        ip, netmask =  V4.normalize(input_ip)
        self.assertEqual(netmask, 0)






def main():
    unittest.main()

if __name__ == '__main__':
    main()