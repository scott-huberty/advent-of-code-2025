from pathlib import Path
from warnings import warn

def get_toy_data():
    return (
        "..@@.@@@@.\n"
        "@@@.@.@.@@\n"
        "@@@@@.@.@@\n"
        "@.@@@@..@.\n"
        "@@.@@@@.@@\n"
        ".@@@@@@@.@\n"
        ".@.@.@.@@@\n"
        "@.@@@.@@@@\n"
        ".@@@@@@@@.\n"
        "@.@.@@@.@.\n"
    )

def get_input_data():
    input_path = Path(__file__).parent / "assets" / "day_4_printing_department.txt"
    return input_path.read_text()

rolls = get_toy_data().strip().splitlines()


def forklift(puzzle: list[str]):
    solution = [""] * len(puzzle)
    for yi, row in enumerate(puzzle):
        for xi, col in enumerate(row):
            if col == ".":
                solution[yi] += "."
                continue
            elif col == "x":
                solution[yi] += "."
                continue
            forklift_accessible = forkliftable(puzzle, y=yi, x=xi)
            if forklift_accessible:
                assert puzzle[yi][xi] == "@"
                solution[yi] += "x"
                continue
            solution[yi] += "@"
    return solution


def forkliftable(puzzle_input: list[str], *, y, x, max_adjacent_rolls: int=4):
    if puzzle_input[y][x] == ".":
        warn(f"No roll of paper to forklift at coordinates (y={y}, x={x})!")
        return

    directions = [
        (-1, 0),   # up
        (+1, 0),   # down
        (0, -1),   # left
        (0, +1),   # right
        (-1, -1),  # up-left
        (-1, +1),  # up-right
        (+1, -1),  # down-left
        (+1, +1),  # down-right
    ]

    dirs = iter(directions)
    adjacent_rolls = 0
    while adjacent_rolls < max_adjacent_rolls:
        try:
            dy, dx = next(dirs)
        except StopIteration:
            return True
        
        # Neighbor y, x coords
        ny, nx = (y + dy, x + dx)

        # Check Bounds
        max_y, max_x = len(puzzle_input), len(puzzle_input[0])
        if ny < 0 or ny >= max_y:
            continue
        if nx < 0 or nx >= max_x:
            continue
        
        # Is there a roll in the neighbors slot
        if puzzle_input[ny][nx] == "@":
            adjacent_rolls += 1
    return False


def count_rolls(grid: list[str], count_accessible: bool=False) -> int:
    char = "x" if count_accessible else "@"
    return sum(
        1
        for row in grid
        for col in row
        if col == char
    )


# ------------------------------
# Toy data test

solution = forklift(rolls)
want_grid = (
    "..xx.xx@x.\n"
    "x@@.@.@.@@\n"
    "@@@@@.x.@@\n"
    "@.@@@@..@.\n"
    "x@.@@@@.@x\n"
    ".@@@@@@@.@\n"
    ".@.@.@.@@@\n"
    "x.@@@.@@@@\n"
    ".@@@@@@@@.\n"
    "x.x.@@@.x."
)

assert solution == want_grid.strip().splitlines()


# ------------------------------
# Part 1
puzzle = get_input_data().strip().splitlines()

part_1_solution = forklift(puzzle)

forkliftable_count = count_rolls(part_1_solution, count_accessible=True)
assert forkliftable_count == 1553

# ------------------------------
# Part 2

want_grid_final = (
    "..........\n"
    "..........\n"
    "..........\n"
    "...x@@....\n"
    "...@@@@...\n"
    "...@@@@@..\n"
    "...@.@.@@.\n"
    "...@@.@@@.\n"
    "...@@@@@..\n"
    "....@@@..."
)

rolls = get_toy_data().strip().splitlines()
rolls_orig_ = rolls.copy()
n_retries = 0
while n_retries < 1:
    prev = rolls.copy()
    rolls = forklift(rolls)
    if rolls == prev:
        n_retries += 1


# Part 2 input data
rolls = get_input_data().strip().splitlines()
n_rolls_orig = count_rolls(rolls)

check_for_accessible_rolls = True
while check_for_accessible_rolls:
    prev = rolls.copy()
    rolls = forklift(rolls)
    if rolls == prev:
        check_for_accessible_rolls = False

n_rolls_final = count_rolls(rolls)
removable_rolls = n_rolls_orig - n_rolls_final
assert removable_rolls == 8442