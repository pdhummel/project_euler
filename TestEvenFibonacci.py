#!/usr/bin/python

import unittest
from even_fibonacci_2 import sum_even_sequence_values

class TestEvenFibonacci(unittest.TestCase):

    def test_sum_even_sequence_values(self):
        self.assertEquals(4613732, sum_even_sequence_values())

if __name__ == '__main__':
    unittest.main()