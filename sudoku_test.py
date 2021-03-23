"Sudoku test"


import random
import unittest

from sudoku import Sudoku


DIGITS = {1, 2, 3, 4, 5, 6, 7, 8, 9}

VALID = "123456789456789123789123456231564897564897231897231564312645978645978312978312645"
INVALID = VALID[:-1] + "1"

INCOMPLETE = "123456789456789123789123456231564897564897231897231564312645978645978312978312640"
INCOMPLETE_DISPLAY = """
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║ 1 │ 2 │ 3 ║ 4 │ 5 │ 6 ║ 7 │ 8 │ 9 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 4 │ 5 │ 6 ║ 7 │ 8 │ 9 ║ 1 │ 2 │ 3 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 7 │ 8 │ 9 ║ 1 │ 2 │ 3 ║ 4 │ 5 │ 6 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 2 │ 3 │ 1 ║ 5 │ 6 │ 4 ║ 8 │ 9 │ 7 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 5 │ 6 │ 4 ║ 8 │ 9 │ 7 ║ 2 │ 3 │ 1 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 8 │ 9 │ 7 ║ 2 │ 3 │ 1 ║ 5 │ 6 │ 4 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 3 │ 1 │ 2 ║ 6 │ 4 │ 5 ║ 9 │ 7 │ 8 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 6 │ 4 │ 5 ║ 9 │ 7 │ 8 ║ 3 │ 1 │ 2 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 9 │ 7 │ 8 ║ 3 │ 1 │ 2 ║ 6 │ 4 │   ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝
"""

EASY = "000401000004020500069050810602905108107806309000000000700104002000060000300000007"
EASY_SOLVED = "573481296814629573269357814632975148157846329498213765786134952925768431341592687"

HARDER = "005300000800000020070010500400005300010070006003200080060500009004000030000009700"
HARDER_SOLVED = "145327698839654127672918543496185372218473956753296481367542819984761235521839764"


def random_digits():
    "Return 9 random digits from 1..9 except one random replaced by 0"
    digits = list(DIGITS)
    random.shuffle(digits)
    return "".join(map(str, digits)).replace(str(random.choice(digits)), "0")


class Test_Sudoku(unittest.TestCase):
    "Test Sudoku"

    def test_validate1(self):
        "Test valid Sudoku"
        sudoku = Sudoku(VALID)
        self.assertTrue(sudoku.validate())

    def test_validate2(self):
        "Test invalid Sudoku"
        sudoku = Sudoku(INVALID)
        self.assertFalse(sudoku.validate())

    def test_grid(self):
        "Test grid"
        sudoku = Sudoku(VALID)
        grid = [[int(VALID[row * 9 + col]) for col in range(9)] for row in range(9)]
        self.assertEqual(sudoku.grid, grid)

    def test_exception(self):
        "Test exception"
        with self.assertRaises(ValueError):
            _ = Sudoku("1")
            _ = Sudoku(1)
            _ = Sudoku("blabla")

    def test_display(self):
        "Test display"
        sudoku = Sudoku(INCOMPLETE)
        self.assertEqual(sudoku.display(), INCOMPLETE_DISPLAY.lstrip())

    def test_str(self):
        "Test normalize"
        sudoku = Sudoku(VALID)
        self.assertEqual(str(sudoku), VALID)

    def test_check_row(self):
        "Test check_row()"
        for row in range(9):
            sudoku = Sudoku()
            sudoku.set_row(row, random_digits())
            sudoku.check_row(row)
            self.assertEqual(set(sudoku.get_row(row)), DIGITS)

    def test_check_col(self):
        "Test check_col()"
        for col in range(9):
            sudoku = Sudoku()
            sudoku.set_col(col, random_digits())
            sudoku.check_col(col)
            self.assertEqual(set(sudoku.get_col(col)), DIGITS)

    def test_check_diag(self):
        "Test check_diag()"
        for diag in range(2):
            sudoku = Sudoku()
            sudoku.set_diag(diag, random_digits())
            sudoku.check_diags()
            self.assertEqual(set(sudoku.get_diag(diag)), DIGITS)

    def test_check_box(self):
        "Test check box"
        for row in range(9):
            for col in range(9):
                sudoku = Sudoku()
                sudoku.set_box(row, col, random_digits())
                self.assertTrue(sudoku.check_box(row, col))
                self.assertEqual(set(sudoku.get_box(row, col)), DIGITS)

    def test_solver1(self):
        "Test solver"
        sudoku = Sudoku(EASY)
        sudoku.solver()
        self.assertEqual(str(sudoku), EASY_SOLVED)
        self.assertTrue(sudoku.validate())

    def test_solver2(self):
        "Test solver"
        sudoku = Sudoku(HARDER)
        sudoku.solver()
        self.assertEqual(str(sudoku), HARDER_SOLVED)
        self.assertTrue(sudoku.validate())
