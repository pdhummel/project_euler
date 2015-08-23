#!/usr/bin/python

###############################################################################
# https://projecteuler.net/problem=96
# https://projecteuler.net/project/resources/p096_sudoku.txt
#
# Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. 
# Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. 
# The objective of Su Doku puzzles, however, 
# is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. 
# Below is an example of a typical starting puzzle grid and its solution grid.
# 
# A well constructed Su Doku puzzle has a unique solution and can be solved by logic, 
# although it may be necessary to employ "guess and test" methods in order to eliminate options 
# (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; 
# the example above is considered easy because it can be solved by straight forward direct deduction.
# 
# The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, 
# but all with unique solutions (the first puzzle in the file is the example above).
# 
# By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; 
# for example, 483 is the 3-digit number found in the top left corner of the solution grid above.
# 
#
# Much of the algorithm was derived from concepts explained at the following:
# http://www.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Introduction.html
###############################################################################

import sys
import copy
import time


###############################################################################
# Solves sudoku puzzles found in an input file and outputs the sum of 
# the top-left 3-digit numbers for all grids.
###############################################################################
def main():
    start = time.clock()
    process_input_file()
    end = time.clock()
    elapsed_time = end - start
    print "The program took " + str(elapsed_time) + " seconds to execute."


###############################################################################
# Reads sudoku puzzles from the input file, p096_sudoku.txt, and solves them.
# Outputs the sum of the top-left 3-digit numbers for all grids.
###############################################################################
def process_input_file():
    f = open('./p096_sudoku.txt', 'r')
    puzzle_lines = []
    line_count = 0
    puzzle_number = 0
    total_top3_sum = 0
    for line in f:
        if "Grid" in line:
            puzzle_lines = []
            puzzle_number += 1
            line_count = 0
        else:
            puzzle_lines.append(line)
            line_count += 1
        if line_count == 9:            
            puzzle = create_puzzle(puzzle_lines)
            start = time.clock()
            puzzle = solve_puzzle(puzzle)
            end = time.clock()
            elapsed_time = end - start            
            if not validate_solved_puzzle(puzzle):
                print "Warning, puzzle " + str(puzzle_number) + " was not solved!"
            total_top3_sum += get_puzzle_value(puzzle)
    f.close()
    print "The sum of the 3-digit numbers for all grids is " + str(total_top3_sum)


###############################################################################
# Creates the puzzle map representation from a list of input strings.
# Input:  puzzle_lines is a list of 9 digit strings
# returns:  a puzzle map
# The puzzle is a 9x9 grid that is represented by a map.  The key is a tuple of coordinates(row, col).
# The value is a list where the first element of the list is the cell value and the second element in the list
# is also a list of possible cell values in the case that the cell value is 0 or empty.
#     Ex:  puzzle[0,0] = [0, [1,2,3,4,5,6,7,8,9] ] 
#        This cell in the top left corner is still unknown and could have any possible value.
###############################################################################
def create_puzzle(puzzle_lines):
    puzzle = {}
    for row_num in range(0, 9):
        row = puzzle_lines[row_num]
        for col_num in range(0, 9):
            cell_value = row[col_num:col_num+1]
            if int(cell_value) > 0:
                puzzle[row_num, col_num] = [cell_value, set([int(cell_value)])]
            else:
                puzzle[row_num, col_num] = [cell_value, set([1,2,3,4,5,6,7,8,9])]
    return puzzle


###############################################################################
# Prints a puzzle.
# Input:  puzzle map
# Output something like this:
# =========================    
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |
# =========================    
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |
# =========================    
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |
# | 0 0 0 | 0 0 0 | 0 0 0 |
# =========================    
###############################################################################
def print_puzzle(puzzle):
    print "========================="
    for row_num in range(0, 9):
        sys.stdout.write("| ")
        for col_num in range(0, 9):
            cell = puzzle[row_num, col_num]
            sys.stdout.write(cell[0] + " ")
            if col_num % 3 == 2:
                sys.stdout.write("| ")
        if row_num % 3 == 2:
            print "\n========================="
        else:
            print ""


###############################################################################
# Solves a single sudoku puzzle.
# Input:  puzzle map.  
# returns the solved puzzle map
###############################################################################
def solve_puzzle(puzzle):
    puzzle = recursive_solving_algorithm(puzzle)
    return puzzle


###############################################################################
# Each cell is initialized with a set of all possible values (1-9) for the cell.
# This function adjusts that set of possible values by eliminating values found in the same row, same column, or same box.
# Input:  puzzle map.  This data structure is modified.
###############################################################################
def markup_cells(puzzle):
    has_changes = True
    while has_changes:
        has_changes = False
        for row_num in range(0, 9):
            for col_num in range(0, 9):
                cell = puzzle[row_num, col_num]
                if cell[0] == "0":
                    puzzle[row_num, col_num][1] = check_row_values(puzzle, row_num, col_num)
                    puzzle[row_num, col_num][1] = check_column_values(puzzle, row_num, col_num)
                    puzzle[row_num, col_num][1] = check_box_values(puzzle, row_num, col_num)
                    if len(puzzle[row_num, col_num][1]) == 1:
                        puzzle[row_num, col_num][0] = str(list(puzzle[row_num, col_num][1])[0])
                        has_changes = True

###############################################################################
# Each cell is initialized with a set of all possible values (1-9) for the cell.
# This function adjusts that set of possible values by eliminating values found in the same row.
# Input:  puzzle map
#         row of cell being checked
#         column of cell being checked
###############################################################################
def check_row_values(puzzle, row_num, col_num):
    possible_value_set = puzzle[row_num, col_num][1]
    for col in range(0, 9):
        if col_num != col:
            cell_value = puzzle[row_num, col][0]
            possible_value_set = possible_value_set - set([int(cell_value)])
    return possible_value_set

###############################################################################
# Each cell is initialized with a set of all possible values (1-9) for the cell.
# This function adjusts that set of possible values by eliminating values found in the same column.
# Input:  puzzle map
#         row of cell being checked
#         column of cell being checked
###############################################################################
def check_column_values(puzzle, row_num, col_num):
    possible_value_set = puzzle[row_num, col_num][1]
    for row in range(0, 9):
        if row_num != row:
            cell_value = puzzle[row, col_num][0]
            possible_value_set = possible_value_set - set([int(cell_value)])
    return possible_value_set

###############################################################################
# Each cell is initialized with a set of all possible values (1-9) for the cell.
# This function adjusts that set of possible values by eliminating values found in the same box.
# Input:  puzzle map
#         row of cell being checked
#         column of cell being checked
###############################################################################
def check_box_values(puzzle, row_num, col_num):
    possible_value_set = puzzle[row_num, col_num][1]
    start_row = 0
    start_col = 0
    if row_num > 2:
        start_row = 3
    if row_num > 5:
        start_row = 6
    if col_num > 2:
        start_col = 3
    if col_num > 5:
        start_col = 6        
    for row in range(start_row, start_row + 3):
        for col in range(start_col, start_col + 3):
            if row_num != row or col_num != col:
                cell_value = puzzle[row, col][0]
                possible_value_set = possible_value_set - set([int(cell_value)])
    return possible_value_set


###############################################################################
# For a definition of preemptive sets, check here:
#     http://www.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Solving_any_Sudoku_II.html
# Basically, they are useful for pruning down possible values for a cell.
#
# Input puzzle map.  This data structure is modified.
###############################################################################
def find_preemptive_sets(puzzle):
    for row_num in range(0, 9):
        for col_num in range(0, 9):
            find_preemptive_sets_in_row(puzzle, row_num, col_num)
            find_preemptive_sets_in_column(puzzle, row_num, col_num)
            find_preemptive_sets_in_box(puzzle, row_num, col_num)
    markup_cells(puzzle)

###############################################################################
# For a definition of preemptive sets, check here:
#     http://www.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Solving_any_Sudoku_II.html
# Basically, they are useful for pruning down possible values for a cell.
# This method checks on a row.
# Input:  puzzle map.  This data structure is modified.
#         row of cell being checked
#         column of cell being checked
###############################################################################
def find_preemptive_sets_in_row(puzzle, row_num, col_num):
    possible_value_set = puzzle[row_num, col_num][1]
    if len(possible_value_set) > 1:    
        set_count = 1
        for col in range(0, 9):
            if col_num != col:
                set_to_match = puzzle[row_num, col][1]
                if set_to_match == possible_value_set:
                    set_count += 1
        if set_count >= len(possible_value_set):
            for col in range(0, 9):
                set_to_change = puzzle[row_num, col][1]
                if set_to_change != possible_value_set:
                    set_to_change = set_to_change - possible_value_set
                    puzzle[row_num, col][1] = set_to_change


###############################################################################
# For a definition of preemptive sets, check here:
#     http://www.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Solving_any_Sudoku_II.html
# Basically, they are useful for pruning down possible values for a cell.
# This method checks on a column.
# Input:  puzzle map.  This data structure is modified.
#         row of cell being checked
#         column of cell being checked
###############################################################################
def find_preemptive_sets_in_column(puzzle, row_num, col_num):
    possible_value_set = puzzle[row_num, col_num][1]
    if len(possible_value_set) > 1:
        set_count = 1
        for row in range(0, 9):
            if row_num != row:
                set_to_match = puzzle[row, col_num][1]
                if set_to_match == possible_value_set:
                    set_count += 1
        if set_count >= len(possible_value_set):
            for row in range(0, 9):
                set_to_change = puzzle[row, col_num][1]
                if set_to_change != possible_value_set:
                    set_to_change = set_to_change - possible_value_set
                    puzzle[row, col_num][1] = set_to_change


###############################################################################
# For a definition of preemptive sets, check here:
#     http://www.math.cornell.edu/~mec/Summer2009/meerkamp/Site/Solving_any_Sudoku_II.html
# Basically, they are useful for pruning down possible values for a cell.
# This method checks in a box.
# Input:  puzzle map.  This data structure is modified.
#         row of cell being checked
#         column of cell being checked
###############################################################################
def find_preemptive_sets_in_box(puzzle, row_num, col_num):
    possible_value_set = puzzle[row_num, col_num][1]
    if len(possible_value_set) > 1:    
        set_count = 1
        start_row = 0
        start_col = 0
        if row_num > 2:
            start_row = 3
        if row_num > 5:
            start_row = 6
        if col_num > 2:
            start_col = 3
        if col_num > 5:
            start_col = 6        
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                if row != row_num or col != col_num:
                    set_to_match = puzzle[row, col][1]
                    if set_to_match == possible_value_set:
                        set_count += 1
        if set_count >= len(possible_value_set):
            for row in range(start_row, start_row + 3):
                for col in range(start_col, start_col + 3):
                    set_to_change = puzzle[row, col][1]
                    if set_to_change != possible_value_set:
                        new_set = set_to_change - possible_value_set
                        puzzle[row, col][1] = new_set



###############################################################################
# Recursively fills-in each cell until a valid puzzle is formed.
# This is a bit of a brute force method.
#
# Input:  puzzle map
# returns a new solved copy of the puzzle map.
###############################################################################
def recursive_solving_algorithm(puzzle):    
    test_puzzle = copy.deepcopy(puzzle)    
    markup_cells(test_puzzle)
    find_preemptive_sets(test_puzzle)                                                    
    for row in range(0, 9):
        for col in range(0, 9):
            cell = test_puzzle[row, col]
            if cell[0] == "0":
                choices = list(cell[1])
                for choice in choices:
                    test_puzzle[row, col][0] = str(choice)
                    return_puzzle = None                    
                    if not has_duplicate(test_puzzle, row, col):
                        return_puzzle = recursive_solving_algorithm(test_puzzle)
                    if return_puzzle != None:
                        return return_puzzle
                return None
    # if things are already solved, we will fall through
    return test_puzzle


###############################################################################
# Checks whether the specified cell has a duplicate in the same row, column, or box.
# Input:  puzzle map
#         row of cell being checked
#         column of cell being checked
# returns True if there is a duplicate and the puzzle is invalid.
###############################################################################
def has_duplicate(puzzle, row_num, col_num):
    cell_value = puzzle[row_num, col_num][0]
    for i in range(0, 9):
        if i != col_num:
            if cell_value == puzzle[row_num, i][0]:
                return True
        if i != row_num:
            if cell_value == puzzle[i, col_num][0]:
                return True
    start_row = 0
    start_col = 0
    if row_num > 2:
        start_row = 3
    if row_num > 5:
        start_row = 6
    if col_num > 2:
        start_col = 3
    if col_num > 5:
        start_col = 6        
    for row in range(start_row, start_row + 3):
        for col in range(start_col, start_col + 3):
            if row_num != row or col_num != col:
                if cell_value == puzzle[row, col][0]:
                    return True
    return False


###############################################################################
# Gets the top 3 left-most digits of the puzzle.
# Input:  puzzle map
# returns top-left 3 digits of the puzzle as a single number
###############################################################################
def get_puzzle_value(puzzle):
    puzzle_value = 0
    puzzle_value += int(puzzle[0,0][0] + puzzle[0,1][0] + puzzle[0,2][0])
    return puzzle_value


###############################################################################
# Checks if the puzzle is solved.
# Input:  puzzle map
# returns True if the puzzle is solved
###############################################################################
def is_puzzle_solved(puzzle):
    for row_num in range(0, 9):
        for col_num in range(0, 9):
            if puzzle[row_num, col_num][0] == "0":
                return False
            if has_duplicate(puzzle, row_num, col_num):
            	return False
    return True

###############################################################################
# Checks if the puzzle is solved and valid.
# Input:  puzzle map
# returns True if the puzzle is solved otherwise raises an exception
###############################################################################
def validate_solved_puzzle(puzzle):
    for row_num in range(0, 9):
        for col_num in range(0, 9):
            if puzzle[row_num, col_num][0] == "0":
                raise ValueError("0 value found at " + str(row_num) + "," + str(col_num))
            if has_duplicate(puzzle, row_num, col_num):
                raise ValueError("duplicate value found for " + str(row_num) + "," + str(col_num))
    return True

###############################################################################
if __name__ == "__main__":
    main()