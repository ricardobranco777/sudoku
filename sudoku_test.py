"Sudoku test"


import unittest

from sudoku import Sudoku


VALID = "123456789456789123789123456231564897564897231897231564312645978645978312978312645"
INVALID = VALID[:-1] + "1"

HARDER = "005300000800000020070010500400005300010070006003200080060500009004000030000009700"
HARDER_SOLVED = "145327698839654127672918543496185372218473956753296481367542819984761235521839764"

IMPOSSIBLE = "609008750300900001000000200830010006002003000560070009000000100100300007703001560"


class TestSudoku(unittest.TestCase):
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

    def test_generate(self):
        "Test generator"
        sudoku = Sudoku()
        sudoku.generate()
        self.assertTrue(sudoku.validate())
