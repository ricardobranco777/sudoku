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

    def get_diag(self, diag):
        "Get diagonal"
        if diag not in {0, 1}:
            raise ValueError
        if diag == 0:
            return tuple(self.grid[num][num] for num in range(9))
        return tuple(self.grid[num][8 - num] for num in range(9))

    def get_box(self, row, col):
        "Return a set with the numbers in the row"
        x, y = 3 * (row // 3), 3 * (col // 3)
        return tuple(self.grid[x + i][y + j] for i in range(3) for j in range(3))

    def set_row(self, row, digits):
        "Set row"
        if len(digits) != 9:
            raise ValueError
        self.grid[row] = list(map(int, digits))

    def set_col(self, col, digits):
        "Set column"
        if len(digits) != 9:
            raise ValueError
        for row in range(9):
            self.grid[row][col] = int(digits[row])

    def set_diag(self, diag, digits):
        "Set diagonal"
        if len(digits) != 9 or diag not in {0, 1}:
            raise ValueError
        if diag == 0:
            for num in range(9):
                self.grid[num][num] = int(digits[num])
        else:
            for num in range(9):
                self.grid[num][8 - num] = int(digits[num])

    def set_box(self, row, col, digits):
        "Set box"
        if len(digits) != 9:
            raise ValueError
        x, y = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                self.grid[x + i][y + j] = int(digits[i * 3 + j])

    def scan_row(self, row):
        "Scan row for zeroes"
        for col in range(9):
            if self.grid[row][col] == 0:
                yield col

    def scan_col(self, col):
        "Scan column for zeroes"
        for row in range(9):
            if self.grid[row][col] == 0:
                yield row

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

    def check_box(self, row, col):
        "Check box"
        box = self.get_box(row, col)
        missing = FULL - set(box)
        if len(missing) == 1:
            x, y = 3 * (row // 3), 3 * (col // 3)
            index = box.index(0)
            i, j = index // 3, index % 3
            self.setitem(x + i, y + j, missing.pop())
            return True
        return False

    def check_row(self, row):
        "Check row"
        solved = 0
        try_digits = FULL - set(self.get_row(row))
        maybe = {n: [] for n in try_digits}
        for try_col in self.scan_row(row):
            for num in try_digits - set(self.get_box(row, try_col)) - set(self.get_col(try_col)):
                maybe[num].append(try_col)
        for num in maybe:
            if len(maybe[num]) == 1:
                self.setitem(row, maybe[num][0], num)
                solved += 1
        return solved

    def check_col(self, col):
        "Check column"
        solved = 0
        try_digits = FULL - set(self.get_col(col))
        maybe = {n: [] for n in try_digits}
        for try_row in self.scan_col(col):
            for num in try_digits - set(self.get_box(try_row, col)) - set(self.get_row(try_row)):
                maybe[num].append(try_row)
        for num in maybe:
            if len(maybe[num]) == 1:
                self.setitem(maybe[num][0], col, num)
                solved += 1
        return solved

    def check_diags(self):
        "Check diagonals"
        solved = 0
        diag = self.get_diag(0)
        missing = FULL - set(diag)
        if len(missing) == 1:
            index = diag.index(0)
            self.setitem(index, index, missing.pop())
            solved += 1
        diag = self.get_diag(1)
        missing = FULL - set(diag)
        if len(missing) == 1:
            index = diag.index(0)
            self.setitem(index, 8 - index, missing.pop())
            solved += 1
        return solved

    def solve1(self):
        "Solve low-hanging fruit in rows, columns & boxes"
        solved = 0
        for row, col in self.scan():
            if self.check_box(row, col):
                solved += 1
            if self.grid[row][col]:
                continue
            solved += self.check_row(row)
            if self.grid[row][col]:
                continue
            solved += self.check_col(col)
        solved += self.check_diags()
        return solved

    def solve2(self):
        "Backtracking solver"
        for row, col in self.scan():
            try_digits = FULL - set(self.get_row(row)) - set(self.get_col(col)) - set(self.get_box(row, col))
            for num in try_digits:
                self.setitem(row, col, num)
                if self.solve2():
                    return True
            self.setitem(row, col, 0)
            return False
        return self.validate()

    def solver(self):
        "Solver"
        while self.solve1():
            pass
        self.solve2()

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
        columns, lines = get_terminal_size()
        spaces = " " * ((columns - 37) // 2)
        lines = "\n" * ((lines - 19) // 2)
        string = f"{spaces}{string}"
        string = string.replace("\n", f"\n{spaces}")
        print("\033c", lines, string, lines, sep="")


if __name__ == "__main__":
    EASY = "000401000004020500069050810602905108107806309000000000700104002000060000300000007"
    MEDIUM = "096000008000800240208010009000637000013000000000125000701060004000500690064000001"
    HARDER = "005300000800000020070010500400005300010070006003200080060500009004000030000009700"
    sudoku = Sudoku(HARDER, seconds=0.01)
    sudoku.solver()
    sudoku.show()
    if not sudoku.validate():
        sys.exit(1)
