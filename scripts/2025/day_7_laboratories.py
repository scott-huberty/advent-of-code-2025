from functools import cache
from pathlib import Path

def get_toy_data():
    return (
        ".......S.......\n"
        "...............\n"
        ".......^.......\n"
        "...............\n"
        "......^.^......\n"
        "...............\n"
        ".....^.^.^.....\n"
        "...............\n"
        "....^.^...^....\n"
        "...............\n"
        "...^.^...^.^...\n"
        "...............\n"
        "..^...^.....^..\n"
        "...............\n"
        ".^.^.^.^.^...^.\n"
        "..............."
    )

def get_input_data(fpath: Path=None) -> str:
    if fpath is None:
        fpath = Path(__file__).resolve().parent / "assets" / "day_7_laboratories.txt"
    return fpath.read_text()


def test_part_1():
    puzzle = get_toy_data()
    n_splits, grid = part_1(puzzle)
    assert n_splits == 21
    return n_splits, grid


def solve_part_1():
    puzzle = get_input_data()
    n_splits, grid = part_1(puzzle)
    return n_splits, grid


def part_1(puzzle):
    grid = [list(row) for row in puzzle.splitlines()]
    
    S_index = grid[0].index("S")
    n_splits = 0
    beam_locs = [S_index]
    for row in grid[1:]:
        locs_update = beam_locs.copy()
        for idx in beam_locs:
            if row[idx] == ".":
                row[idx] = "|"
            elif row[idx] == "^":
                locs_update.remove(idx)
                locs_update.extend([idx-1, idx+1])
                locs_update = sorted(set(locs_update))
                n_splits += 1
            else:
                raise RuntimeError()
        beam_locs = locs_update
    return n_splits, grid

def redraw(grid) -> None:
    for row in grid:
        print("".join(row))


def count_paths(grid):
    """Part 2"""
    n_rows, n_cols = len(grid), len(grid[0])
    S_index = grid[0].index("S")
    grid[1][S_index] = "|"
    
    start_row, start_col = 1, S_index
    PIPE = {"|", "^"}

    @cache
    def dfs(r, c):
        if r == n_rows - 1:
            return 1
        n_paths = 0
        curr = grid[r][c]
        nr = r + 1
        if curr == "|":
            # From a vertical pipe, continue straight down only.
            nc = c
            if 0 <= nc < n_cols and grid[nr][nc] in PIPE:
                n_paths += dfs(nr, nc)
        elif curr == "^":
            # From a splitter, branch down-left and down-right.
            for nc in (c - 1, c + 1):
                if 0 <= nc < n_cols and grid[nr][nc] in PIPE:
                    n_paths += dfs(nr, nc)
        else:
            # Not on a valid path cell; no paths from here.
            return 0
        return n_paths
    return dfs(start_row, start_col)

if __name__ == "__main__":
    # Part 1
    _, grid = test_part_1()
    # Part 2
    n_paths = count_paths(grid)
    assert n_paths == 40

    # Real
    # Part 1
    n_splits, grid = solve_part_1()
    assert n_splits == 1550
    n_paths = count_paths(grid)
    assert n_paths == 9897897326778


