from pathlib import Path
from itertools import groupby
from math import prod

def get_toy_data():
    return (
        "123 328  51 64 \n"
        " 45 64  387 23 \n"
        "  6 98  215 314\n"
        "*   +   *   +  "
    )


def get_input_data(fpath: Path=None) -> Path:
    if fpath is None:
        fpath = Path(__file__).parent / "assets" / "day_6_trash_compactor.txt"
    return Path(fpath).read_text()


def test_part_1():
    puzzle = prep_data(get_toy_data())
    expressions = build_expressions(puzzle)
    answer = sum(evaluate(expressions))
    assert answer == 4277556
    return answer


def solve_part_1():
    puzzle = prep_data(get_input_data())
    expressions = build_expressions(puzzle)
    return sum(evaluate(expressions))

def prep_data(puzzle):
    return [row.strip().split() for row in puzzle.splitlines()]

def build_expressions(puzzle: list[list[str]]):
    numbers,  operations = puzzle[:-1], puzzle[-1]

    expressions = []
    for ii, col in enumerate(zip(*numbers)):
        op = operations[ii]
        expression = build_expression(col, op)
        expressions.append(expression)
    return expressions


def build_expression(numbers, operator):
    expression = ""
    for ni, number in enumerate(numbers):
        expression += number
        if ni+1 < len(numbers):
            expression += operator
    return expression


def evaluate(expressions):
    return (eval(expression) for expression in expressions)


def parse_input_part_2(s: str):
    """Rodrigos Solution."""
    def is_not_none(obj):
        return obj is not None

    *operand_chars, operator_line = s.splitlines()
    operand_chars = list(zip(*operand_chars))

    operands = [
        int(string) if (string := "".join(tup).strip()) else None
        for tup in operand_chars
    ]

    grouped_operands = []
    for key, group in groupby(operands, key=is_not_none):
        if key:
            grouped_operands.append(list(group))

    operators = [
        sum if op_char == "+" else prod
        for op_char in operator_line.split()
    ]
    results = []
    for col, op in zip(grouped_operands, operators):
        results.append(op(col))
    return results


def test_part_2():
    """My solution"""
    s = get_toy_data()
    results = sum(part_2(s))
    assert results == 3263827


def part_2(puzzle: str):
    """My Solution"""
    operator_map = {"+": sum, "*": prod}

    *columns, operators = puzzle.splitlines()
    columns = transpose(columns)
    
    operands = []
    group = []
    for tup in columns:
        s = "".join(tup).strip()
        if not s.isdigit():
            # Close out group and reset
            operands.append(group)
            group = []
            continue
        group.append(int(s))
    # If final tuple wasn't a blank line make sure that the sub-group still gets added
    if group:
        operands.append(group)

    ops = [operator_map[op] for op in operators.split()]
    results = []
    for col, op in zip(operands, ops):
        results.append(op(col))
    return results


def transpose(l: list) -> list:
    return list(zip(*l))


if __name__ == "__main__":
    test_part_1()
    part1 = solve_part_1()
    assert part1 == 3785892992137
    # Rodrigos Solution
    part2 = parse_input_part_2(get_input_data())
    assert sum(part2) == 7669802156452
    # My Solution
    test_part_2()
    my_solution = sum(part_2(get_input_data())) 
    assert my_solution == 7669802156452