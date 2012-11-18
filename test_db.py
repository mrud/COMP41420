#!/usr/bin/env python

from IPStorage import DB
import unittest

class TestStorage(unittest.TestCase):

    def setUp(self):
        self.db = DB()
        self.db.insert("192.168.1.1/24", "Example Message")
        self.db.insert("192.168.1.92/28", "something else")

    def test_invalid(self):
        self.assertRaises(KeyError, self.db.get, "192.168.2.1")

    def test_value(self):
        self.assertEqual(self.db.get("192.168.1.1")[1], "Example Message")
        self.assertEqual(self.db.get("192.168.1.92")[1], "something else")

    def test_network(self):
        self.assertEqual(self.db.get("192.168.1.0")[1], "Example Message")
        self.assertEqual(self.db.get("192.168.1.80")[1], "something else")

    def test_delete(self):
        self.assertEqual(self.db.get("192.168.1.0")[1], "Example Message")
        del self.db["192.168.1.5/24"]
        self.assertRaises(KeyError, self.db.get, "192.168.1.0")
        self.assertEqual(self.db.get("192.168.1.80")[1], "something else")
