"""Sudoku"""

import sys
import time
from shutil import get_terminal_size


FULL = {1, 2, 3, 4, 5, 6, 7, 8, 9}


class Sudoku:
    """Sudoku"""
    def __init__(self, digits="0" * 81, seconds=0):
        digits = "".join(map(str, digits))
        if len(digits) == 81 and digits.isdigit():
            self.grid = [[int(digits[row * 9 + col]) for col in range(9)] for row in range(9)]
        else:
            raise ValueError("Invalid table")
        self.seconds = seconds

    def __str__(self):
        return "".join(str(self.grid[row][col]) for row in range(9) for col in range(9))

    def get_row(self, row):
        "Get row"
        return tuple(self.grid[row])

    def get_col(self, col):
        "Get column"
        return tuple(self.grid[i][col] for i in range(9))

    def get_box(self, row, col):
        "Get box"
        x, y = 3 * (row // 3), 3 * (col // 3)
        return tuple(self.grid[x + i][y + j] for i in range(3) for j in range(3))

    def scan(self):
        "Scan grid for zeroes"
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    yield row, col

    def setitem(self, row, col, value):
        "Set item in grid, optionally show change"
        if self.seconds:
            self.show()
            time.sleep(self.seconds)
        self.grid[row][col] = value
        if self.seconds:
            self.show()

    def solver(self):
        "Backtracking solver"
        for row, col in self.scan():
            try_digits = FULL - set(self.get_row(row)) - set(self.get_col(col)) - set(self.get_box(row, col))
            for num in try_digits:
                self.setitem(row, col, num)
                if self.solver():
                    return True
            self.setitem(row, col, 0)
            return False
        return self.validate()

    def validate_row(self, row):
        "Validate row"
        return set(self.get_row(row)) == FULL

    def validate_col(self, col):
        "Validate column"
        return set(self.get_col(col)) == FULL

    def validate(self):
        "Validate grid"
        return all(self.validate_row(row) for row in range(9)) and \
            all(self.validate_col(col) for col in range(9))

    def display(self):
        "Display grid"
        string = "╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗\n"
        for row in range(9):
            string += "║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║\n".format(*self.grid[row])
            if row == 8:
                string += "╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝\n"
            elif (row + 1) % 3 == 0:
                string += "╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\n"
            else:
                string += "╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\n"
        return string.replace("0", " ")

    def show(self):
        "Show grid"
        string = self.display()
        if sys.stdout.isatty():
            cls = "\033c"
            columns, lines = get_terminal_size()
            spaces = " " * ((columns - 37) // 2)
            lines = "\n" * ((lines - 19) // 2)
            string = f"{spaces}{string}"
            string = string.replace("\n", f"\n{spaces}")
        else:
            cls = lines = ""
        print(cls, lines, string, lines, sep="")


if __name__ == "__main__":
    EASY = "000401000004020500069050810602905108107806309000000000700104002000060000300000007"
    MEDIUM = "096000008000800240208010009000637000013000000000125000701060004000500690064000001"
    HARDER = "609008750300900001000000200830010006002003000560070009000000100100300007703001560"
    HARDER = "005300000800000020070010500400005300010070006003200080060500009004000030000009700"
    sudoku = Sudoku(HARDER, seconds=0)
    sudoku.solver()
    sudoku.show()
    if not sudoku.validate():
        sys.exit(1)
