#!/usr/bin/python

import unittest
from clock_sequence_506 import sum_sequence_values

class TestClockSequence(unittest.TestCase):

    def test_sum_sequence_values(self):
        self.assertEquals(36120, sum_sequence_values(11))
        self.assertEquals(18232686, sum_sequence_values(1000))

if __name__ == '__main__':
    unittest.main()