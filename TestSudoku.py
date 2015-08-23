#!/usr/bin/python

import unittest
from sudoku_96 import create_puzzle
from sudoku_96 import solve_puzzle
from sudoku_96 import check_row_values
from sudoku_96 import check_column_values
from sudoku_96 import check_box_values
from sudoku_96 import has_duplicate
from sudoku_96 import get_puzzle_value
from sudoku_96 import is_puzzle_solved
from sudoku_96 import validate_solved_puzzle

class TestSudoku(unittest.TestCase):
    
    def setUp(self):
        self.puzzle_lines = []
        self.puzzle_lines.append("003020600")
        self.puzzle_lines.append("900305001")
        self.puzzle_lines.append("001806400")
        self.puzzle_lines.append("008102900")
        self.puzzle_lines.append("700000008")
        self.puzzle_lines.append("006708200")
        self.puzzle_lines.append("002609500")
        self.puzzle_lines.append("800203009")
        self.puzzle_lines.append("005010300")

    def test_create_puzzle(self):
        puzzle = create_puzzle(self.puzzle_lines)
        self.assertEquals(puzzle[0,0][0], "0")
        self.assertEquals(puzzle[0,0][1], set([1,2,3,4,5,6,7,8,9]))

    def test_solve_puzzle(self):
        puzzle = create_puzzle(self.puzzle_lines)
        puzzle = solve_puzzle(puzzle)
        self.assertEquals(puzzle[0,0][0], "4")
        self.assertEquals(puzzle[0,1][0], "8")
        self.assertEquals(puzzle[0,2][0], "3")
        self.assertEquals(puzzle[8,8][0], "2")

    def test_check_row_values(self):
        puzzle = create_puzzle(self.puzzle_lines)
        possible_value_set = check_row_values(puzzle, 0, 0)
        self.assertEquals(possible_value_set, set([1,4,5,7,8,9]))

    def test_check_column_values(self):
        puzzle = create_puzzle(self.puzzle_lines)
        possible_value_set = check_column_values(puzzle, 0, 0)
        self.assertEquals(possible_value_set, set([1,2,3,4,5,6]))

    def test_check_box_values(self):
        puzzle = create_puzzle(self.puzzle_lines)
        possible_value_set = check_box_values(puzzle, 0, 0)
        self.assertEquals(possible_value_set, set([2,4,5,6,7,8]))
        possible_value_set = check_box_values(puzzle, 7, 7)
        self.assertEquals(possible_value_set, set([1,2,4,6,7,8]))        

    def test_has_duplicate(self):
        puzzle = create_puzzle(self.puzzle_lines)
        puzzle[0, 0][0] = "4"
        self.assertFalse(has_duplicate(puzzle, 0, 0))
        # row
        puzzle[0, 0][0] = "3"
        self.assertTrue(has_duplicate(puzzle, 0, 0))
        # column
        puzzle[0, 0][0] = "7"
        self.assertTrue(has_duplicate(puzzle, 0, 0))
        # box
        puzzle[0, 0][0] = "1"
        self.assertTrue(has_duplicate(puzzle, 0, 0))

    def test_get_puzzle_value(self):
        puzzle = create_puzzle(self.puzzle_lines)
        puzzle = solve_puzzle(puzzle)
        self.assertEquals(483, get_puzzle_value(puzzle))

    def test_is_puzzle_solved(self):
        puzzle = create_puzzle(self.puzzle_lines)
        puzzle = solve_puzzle(puzzle)
        self.assertTrue(is_puzzle_solved(puzzle)) 
        puzzle[0, 0][0] = "0"
        self.assertFalse(is_puzzle_solved(puzzle)) 

    def test_validate_solved_puzzle(self):
        puzzle = create_puzzle(self.puzzle_lines)
        puzzle = solve_puzzle(puzzle)
        self.assertTrue(validate_solved_puzzle(puzzle))
        puzzle[0, 0][0] = "0"
        try:
            validate_solved_puzzle(puzzle)
            self.fail("ValueError for 0 not raised")
        except:
            pass
        puzzle[0, 0][0] = "3"
        try:
            validate_solved_puzzle(puzzle)
            self.fail("ValueError for duplicate not raised")
        except:
            pass


if __name__ == '__main__':
    unittest.main()