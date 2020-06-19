from unittest import TestCase


class Sudoku:

    size = 9
    square_size = 3

    def __init__(self, file_name):
        self.file_name = file_name
        self.raw_field = self._get_from_file()
        self._validate_field()
        self.field = self._to_int()

    def play(self):
        answer = self.solve()
        print(answer)

    def solve(self):
        """
        Алгоритм: проходит по всем значениям матрицы судоку,
            если находит 0 пытается вычислить значение.
        Вычисление: множество возможных значений минус значения строки, стобца и квадрата.
        Завершение: вычисление всех значений, в обратном случае - ошибка.
        """
        stats = []
        while True:
            count = self.size * self.size
            for i in range(self.size):
                for j in range(self.size):
                    if self.field[i][j] == 0:
                        variants = {v for v in range(1, self.size + 1)
                                    } - self._row(i) - self._col(j) - self._square(i, j)
                        if len(variants) == 1:
                            self.field[i][j] = list(variants)[0]
                        else:
                            continue
                    count -= 1
            stats.append(count)
            if count == 0:
                return [''.join(map(str, line)) for line in self.field]
            # повторяется кол-во не вычисленных значений
            if len(stats) > 1 and stats[-1] == stats[-2]:
                raise Exception("Can't solve, too complicated")

    def _row(self, index):
        """Множество значений строки по индексу."""
        return set(self.field[index])

    def _col(self, index):
        """Множество значений столбца по индексу."""
        return {self.field[i][index] for i in range(9)}

    def _square(self, row_index, col_index):
        """Множество значений квадрата по индексам."""
        value = set()
        row_start = row_index // self.square_size * self.square_size
        col_start = col_index // self.square_size * self.square_size
        for i in range(row_start, row_start + self.square_size):
            for j in range(col_start, col_start + self.square_size):
                value.add(self.field[i][j])
        return value

    def _get_from_file(self):
        """Список строк из файла без переносов."""
        with open(self.file_name) as file:
            return [line.rstrip() for line in file.readlines()]

    def _validate_field(self):
        """
        Проверяет соответствие поля критериям:
        длинна столбца, длинна строки, значения - натуральные числа.
        """
        if len(self.raw_field) != self.size:
            raise ValueError(f'Column length should be {self.size}')
        for row in self.raw_field:
            if len(row) != self.size:
                print(f"Wrong row: {row}")
                raise ValueError(f'Row length should be {self.size}')
            try:
                int(row)
            except ValueError:
                print(f"Wrong row: {row}")
                raise ValueError('Values should be int')

    def _to_int(self):
        """Конвертирует поле в числовые значения."""
        int_sudoku_field = []
        for i in range(self.size):
            int_sudoku_field.append([])
            for j in range(self.size):
                int_sudoku_field[i].append(int(self.raw_field[i][j]))
        return int_sudoku_field


class TestSudoku(TestCase):

    sudoku = Sudoku('sudoku#1')

    def test_solve(self):
        """Проверяет алгоритм решения судоку"""
        assert self.sudoku.solve() == [
            '483921657',
            '967345821',
            '251876493',
            '548132976',
            '729564138',
            '136798245',
            '372689514',
            '814253769',
            '695417382',
        ]

    def test__row(self):
        """Проверяет множество значений строки."""
        assert self.sudoku._row(3) == {0, 8, 1, 2, 9}

    def test__col(self):
        """Проверяет множество значений столбца."""
        assert self.sudoku._col(3) == {0, 3, 8, 1, 7, 6, 2}

    def test__square(self):
        """Проверяет множество значений квадрата."""
        assert self.sudoku._square(3, 3) == {0, 1, 2, 7, 8}

    def test__get_from_file(self):
        """Проверяет список строк из файла."""
        data = self.sudoku._get_from_file()

        assert isinstance(data, list)
        assert all([isinstance(row, str)] for row in data)

    def test__to_int(self):
        """Проверяет конвертацию поля в числовой формат."""
        assert self.sudoku._to_int() == [
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0],
        ]

    def test__validate_field_col_length_error(self):
        """Проверяет вызов ошибки если столбцы не правильной длинны."""
        self.sudoku.raw_field.append('8-10203009')

        with self.assertRaises(ValueError) as context:
            self.sudoku._validate_field()

        assert context.exception.args[0] == f'Column length should be {self.sudoku.size}'
        self.sudoku.raw_field.pop()

    def test__validate_field_row_length_error(self):
        """Проверяет вызов ошибки если строка не правильной длинны."""
        tmp, self.sudoku.raw_field[7] = self.sudoku.raw_field[7], '8-10203009'

        with self.assertRaises(ValueError) as context:
            self.sudoku._validate_field()

        assert context.exception.args[0] == f'Row length should be {self.sudoku.size}'
        self.sudoku.raw_field[7] = tmp

    def test__validate_field_symbol_error(self):
        """Проверяет вызов ошибки если в строке не правильный символ."""
        tmp, self.sudoku.raw_field[7] = self.sudoku.raw_field[7], '8a0203009'

        with self.assertRaises(ValueError) as context:
            self.sudoku._validate_field()

        assert context.exception.args[0] == 'Values should be int'
        self.sudoku.raw_field[7] = tmp


print('Start functional tests:')
for n in range(1, 4):
    s = Sudoku(f'sudoku#{n}')
    print(f"Try to solve sudoku#{n}")
    s.play()
cs = Sudoku('sudoku#4')
print("Try to solve sudoku#4")
try:
    cs.play()
except Exception as e:
    print(e)
    print('Test success!')

print('Start model tests:')
test = TestSudoku()
test.test__row()
test.test__col()
test.test__square()
test.test__get_from_file()
test.test__to_int()
test.test__validate_field_col_length_error()
test.test__validate_field_row_length_error()
test.test__validate_field_symbol_error()
print('Test success!')
