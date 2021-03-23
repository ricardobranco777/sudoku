"Sudoku test"


import unittest

from sudoku import Sudoku


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

IMPOSSIBLE = "609008750300900001000000200830010006002003000560070009000000100100300007703001560"


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

    def test_solver(self):
        "Test solver"
        sudoku = Sudoku(HARDER)
        sudoku.solver()
        self.assertEqual(str(sudoku), HARDER_SOLVED)
        self.assertTrue(sudoku.validate())

    def test_solver2(self):
        "Test solver on impossible"
        sudoku = Sudoku(IMPOSSIBLE)
        sudoku.solver()
        self.assertEqual(str(sudoku), IMPOSSIBLE)
        self.assertFalse(sudoku.validate())
