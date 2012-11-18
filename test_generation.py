import unittest
from IPStorage import DB
V4 = DB.IPv4

class TestGenerate(unittest.TestCase):

    def test_generate(self):
        a = V4("255.255.255.254/28")
        self.assertEqual(len(list(a.generate())), 16)

        a = V4("255.255.255.9/24")
        self.assertEqual(len(list(a.generate())), 2**8)

        a = V4("255.255.255.9/16")
        self.assertEqual(len(list(a.generate())), 2**16)

    def test_32bit(self):
        a = V4("255.255.255.254/32")
        self.assertEqual(len(list(a.generate())), 1)


def main():
    unittest.main()

if __name__ == '__main__':
    main()