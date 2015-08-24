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
# References:
# http://eulersolutions.fr.yuku.com/topic/358/problem-506#.VdoocrcVfsY
# https://github.com/Meng-Gen/ProjectEuler/blob/master/506.py
#       (100000000000000, '=>', 18934502L)
# https://projecteuler.net/thread=506
# 
###############################################################################

import time


###############################################################################
# Outputs the sum of the terms from the clock sequence.
###############################################################################
def main():
    start = time.clock()
    total_sum = sum_sequence_values3(pow(10, 14))
    end = time.clock()
    elapsed_time = end - start
    print "The program took " + str(elapsed_time) + " seconds to execute."

###############################################################################
#
# Returns and outputs the following sum, S(n) from the specified nth value.
# Let vn be the n'th value from the clock sequence. 
# Where S(n) is v1 + v2 + ... + vn.
#
# Input: nth term from sequence
# returns:  S(n)
#
# This was basically my original brute force method.  Not very performant.
#
###############################################################################
def sum_sequence_values(n):
    base_number_seq = (1,2,3,4,3,2)
    total_sum = 0
    current_seq_value = 0
    current_seq_sum = 0
    position = 0
    num = 1
    while num < n + 1:
        while num != current_seq_sum:
            if position >= 6:  # len(base_number_seq)
                position = 0
            digit = base_number_seq[position]
            position += 1
            current_seq_sum += digit
            current_seq_value = current_seq_value * 10 + digit
        total_sum += current_seq_value
        current_seq_value = 0
        current_seq_sum = 0
        num += 1
    print "S(" + str(n) + ") mod 123454321 = " + str(total_sum % 123454321)
    return total_sum % 123454321


###############################################################################
# 
# Returns and outputs the following sum, S(n) from the specified nth value.
# Let vn be the n'th value from the clock sequence. 
# Where S(n) is v1 + v2 + ... + vn.
#
# Input: nth term from sequence
# returns:  S(n)
#
# This was my second attempt to get something faster.
# The key was in recognizing that the sequence repeats after every 15.
#
###############################################################################
def sum_sequence_values2(n, supress=False):
    # 1, 2, 3, 4, 32, 123, 43, 2123, 432, 1234, 32123, 43212, 34321, 23432, 123432, 1234321, 2343212, . . .
    # Sequence repeats every 15.
    suffix = (0, 1, 2, 3, 4, 32, 123, 43, 2123, 432, 1234, 32123, 43212, 34321, 23432, 123432 )
    # The prefixes all sum to 15
    prefix = (123432, 123432, 234321, 343212, 432123, 321234, 123432, 432123, 212343, 432123, 123432, 321234, 432123, 343212, 234321, 123432)

    total_sum = 0
    position = 0
    num = 1
    while num < n + 1:
        seq_for_n = num % 15
        if seq_for_n == 0:
            seq_for_n = 15
        number_of_15s = num / 15
        current_seq_value = 0

        if num > 15:
                # replicate the prefix for the number of sets of 15 we have
                current_seq_value = int(str(prefix[seq_for_n]) * number_of_15s)

        # Add the suffix to the current_seq_value
        if num % 15 > 0 or current_seq_value == 0: 
            shift = 10**len(str(suffix[seq_for_n]))
            current_seq_value = current_seq_value * shift + suffix[seq_for_n]

        total_sum += current_seq_value
        num += 1
    if not supress:
        print "S(" + str(n) + ") mod 123454321 = " + str(total_sum % 123454321)
    return total_sum % 123454321


###############################################################################
# 
# Returns and outputs the following sum, S(n) from the specified nth value.
# Let vn be the n'th value from the clock sequence. 
# Where S(n) is v1 + v2 + ... + vn.
#
# Input: nth term from sequence
# returns:  S(n)
#
# This was my third attempt and didn't require much thinking as the author
# described the algorithm.
#
# From https://projecteuler.net/thread=506;page=2:        
# There is a repetition of vn%123454321 and found that it repeats every 15*55555 
# S(15*55555)%123454321 = 48521737 
# Find the integer value of n/(15*55555) which shall be x 
# Find n%(15*55555) which shall be i 
# Then compute ( 48521737*x + S(i) ) mod 123454321
#
###############################################################################
def sum_sequence_values3(n):
        x = n / (15*55555)
        i = n % (15*55555)
        sum_i = sum_sequence_values2(i, True)
        total_sum = 48521737 * x + sum_i
        print "S(" + str(n) + ") mod 123454321 = " + str(total_sum % 123454321)
        return total_sum % 123454321


###############################################################################
if __name__ == "__main__":
    main()