import unittest

from trie import PrefixTrie

class TrieTest(unittest.TestCase):

    def test_insert(self):
        db = PrefixTrie()
        value = "string"
        db["test"] = value
        self.assertEqual(db["test"], value)

    def test_prefix(self):
        db = PrefixTrie()
        db["an"] = 0
        db["ant"] = 1
        db["all"] = 2
        db["allot"] = 3
        db["alloy"] = 4
        db["aloe"] = 5
        db["are"] = 6
        db["be"] = 7

        self.assertSequenceEqual(db.longest_prefix("antonym"), ("ant", 1))
        self.assertSequenceEqual(db.longest_prefix("any"), ("an", 0))
        self.assertSequenceEqual(db.longest_prefix("are"), ("are", 6))
        self.assertRaises(KeyError, db.longest_prefix, "alsa")
        self.assertRaises(KeyError, db.longest_prefix, "b")

    def test_del(self):
        db = PrefixTrie()
        db["00"] = 1
        db["001"] = 2
        db["002"] = 3
        db["0011"] = 4
        self.assertRaises(KeyError, db.__delitem__, "b")

        self.assertEqual(db["001"], 2)
        self.assertSequenceEqual(db.longest_prefix("0015"), ("001", 2))

        del db["001"]
        self.assertRaises(KeyError, db.__getitem__, "001")
        self.assertEqual(db["0011"], 4)
        self.assertSequenceEqual(db.longest_prefix("0015"), ("00", 1))
