#!/usr/bin/python

###############################################################################
# https://projecteuler.net/problem=506
#
# Consider the infinite repeating sequence of digits:
# 1234321234321234321...
#
# Amazingly, you can break this sequence of digits into a sequence of integers such that the sum of the digits in the n'th value is n.
#
# The sequence goes as follows:
# 1, 2, 3, 4, 32, 123, 43, 2123, 432, 1234, 32123, ...
#
# Let vn be the n'th value in this sequence. For example, v2 = 2, v5 = 32 and v11 = 32123.
#
# Let S(n) be v1 + v2 + ... + vn. For example, S(11) = 36120, and S(1000) mod 123454321 = 18232686.
#
# Find S(1014) mod 123454321.
#
###############################################################################

import time

# About 2 hours for the initial solution.
# TODOs:
# accept input
# optimize memory usage -- http://stackoverflow.com/questions/19926089/python-equivalent-of-java-stringbuffer

###############################################################################
# Outputs the sum of the terms from the clock sequence.
###############################################################################
def main():
    start = time.clock()
    total_sum = sum_sequence_values(pow(10, 14))
    end = time.clock()
    elapsed_time = end - start
    print "The program took " + str(elapsed_time) + " seconds to execute."

###############################################################################
# Returns and outputs the following sum, S(n) from the specified nth value.
# Let vn be the n'th value from the clock sequence. 
# Where S(n) is v1 + v2 + ... + vn.
#
# Input: nth term from sequence
# returns:  S(n)
###############################################################################
def sum_sequence_values(n):
    base_number_seq = [1,2,3,4,3,2]
    total_sum = 0
    total_seq = base_number_seq
    current_seq_value = 0
    current_seq_sum = 0
    position = 0
    num = 1
    while num < n + 1:
        while num != current_seq_sum:
            if position >= len(total_seq):
                position = 0
            digit = total_seq[position]
            position += 1
            current_seq_sum += digit
            current_seq_value = current_seq_value * 10 + digit
        total_sum += current_seq_value
        current_seq_value = 0
        current_seq_sum = 0
        num += 1
    print "S(" + str(num) + ") mod 123454321 = " + str(total_sum % 123454321)
    return total_sum % 123454321


###############################################################################
if __name__ == "__main__":
    main()