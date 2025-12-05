from pathlib import Path


def get_toy_data() -> str:
    return (
        "3-5\n"
        "10-14\n"
        "16-20\n"
        "12-18\n"
        "\n"
        "1\n"
        "5\n"
        "8\n"
        "11\n"
        "17\n"
        "32\n"
    )


def get_input_data() -> str:
    input_path = Path(__file__).parent / "assets" / "day_5_cafeteria.txt"
    return input_path.read_text()


def get_fresh_ids(db: str) -> set[int]:
    id_ranges, available_ids = parse_database(db)
    fresh_ids = []
    for ingredient_id in available_ids:
        if any(
            lower_bound <= ingredient_id <= upper_bound
            for (lower_bound, upper_bound)
            in id_ranges
        ):
            fresh_ids.append(ingredient_id)
    return fresh_ids


def parse_database(db: str, unique_id_ranges: bool=False) -> tuple[list[tuple[int, int]], list[int]]:
    id_ranges, available_ids = map(str.splitlines, db.split("\n\n"))
    available_ids = list(map(int, available_ids))
    # id_ranges = [sorted(map(int, foo.split("-"))) for foo in id_ranges]
    id_ranges = sorted(
        [
            tuple(int(part) for part in this_range.split("-"))
            for this_range in id_ranges
        ]
    )
    if unique_id_ranges:
        id_ranges = remove_overlap(id_ranges)
    return id_ranges, available_ids


def remove_overlap(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    result = []
    current_start = -1
    current_stop = -1

    for start, stop in sorted(ranges):
        if start > current_stop:
            # This segment start after the last segment stops
            # Just add it to the result
            result.append((start, stop))
            current_start, current_stop = start, stop
        else:
            # Segments overlap, replaace
            result[-1] = (current_start, max(current_stop, stop))
            # Current start already guaranteed to be lower
            current_stop = max(current_stop, stop)
    return result


def inclusive_count(start, stop):
    return (stop - start) + 1


def test_part_1():
    db = get_toy_data()
    # spoiled_ids = get_spoiled_ids(db)
    # assert spoiled_ids == {1, 8, 32}
    fresh = get_fresh_ids(db)
    n_fresh = len(fresh)
    assert n_fresh == 3
    assert fresh == [5, 11, 17]


def solve_part_1():
    db = get_input_data()
    fresh_ids = get_fresh_ids(db)
    assert len(fresh_ids) == 613
    return len(fresh_ids)
    
def test_part_2():
    db = get_toy_data()
    id_ranges, _ = parse_database(db)
   
def test_part_2():
    db = get_toy_data()
    id_ranges, _ = parse_database(db, unique_id_ranges=True)
    n_fresh_ids = sum(inclusive_count(start, stop) for (start, stop) in id_ranges)
    assert n_fresh_ids == 14


def solve_part_2():
    db = get_input_data()
    id_ranges, _ = parse_database(db, unique_id_ranges=True)
    n_fresh_ids = sum(inclusive_count(start, stop) for (start, stop) in id_ranges)
    return n_fresh_ids


if __name__ == "__main__":
    test_part_1()
    part_1_answer = solve_part_1()
    print(f"Available Ingredient IDs that are FRESH (part 1): {part_1_answer}")
    test_part_2()
    part_2_answer = solve_part_2()
    assert part_2_answer == 336495597913098
    print(f"Number of fresh Ingredient IDS (part 2): {part_2_answer}")