#!/usr/bin/python

import unittest
from clock_sequence_506 import sum_sequence_values
from clock_sequence_506 import sum_sequence_values2
from clock_sequence_506 import sum_sequence_values3

class TestClockSequence(unittest.TestCase):

    def test_sum_sequence_values(self):
        self.assertEquals(36120, sum_sequence_values(11))
        self.assertEquals(260517, sum_sequence_values(15))
        self.assertEquals(1494838, sum_sequence_values(16))
        self.assertEquals(3838050, sum_sequence_values(17))
        self.assertEquals(55072872, sum_sequence_values(29))
        self.assertEquals(32875304, sum_sequence_values(30))
        self.assertEquals(57808267, sum_sequence_values(31))
        self.assertEquals(107138899, sum_sequence_values(32))
        self.assertEquals(18232686, sum_sequence_values(1000))

        self.assertEquals(36120, sum_sequence_values2(11))
        self.assertEquals(260517, sum_sequence_values2(15))    
        self.assertEquals(1494838, sum_sequence_values2(16))    
        self.assertEquals(3838050, sum_sequence_values2(17)) 
        self.assertEquals(55072872, sum_sequence_values2(29))
        self.assertEquals(32875304, sum_sequence_values2(30))
        self.assertEquals(57808267, sum_sequence_values2(31))
        self.assertEquals(107138899, sum_sequence_values2(32))
        self.assertEquals(18232686, sum_sequence_values2(1000))            

        self.assertEquals(36120, sum_sequence_values3(11))
        self.assertEquals(260517, sum_sequence_values3(15))    
        self.assertEquals(1494838, sum_sequence_values3(16))    
        self.assertEquals(3838050, sum_sequence_values3(17)) 
        self.assertEquals(55072872, sum_sequence_values3(29))
        self.assertEquals(32875304, sum_sequence_values3(30))
        self.assertEquals(57808267, sum_sequence_values3(31))
        self.assertEquals(107138899, sum_sequence_values3(32))
        self.assertEquals(18232686, sum_sequence_values3(1000))

if __name__ == '__main__':
    unittest.main()