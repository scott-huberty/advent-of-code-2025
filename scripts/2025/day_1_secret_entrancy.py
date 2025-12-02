import argparse
from collections.abc import Iterable, Generator
from itertools import accumulate
from pathlib import Path


def turn_dial(start: int, rotation: int, dial_size: int=100) -> int:
    """Turn the dial from a starting position by a given rotation amount.

    Uses modulo arithmetic to wrap around the dial positions (0-99).
    
    Examples
    --------
    >>> turn_dial(50, 10)
    60
    >>> turn_dial(95, 10)
    5
    >>> turn_dial(5, -10)
    95
    """
    end_position = (start + rotation) % dial_size
    return end_position

# Part 1
def count_zero_landings(rotations: Iterable[int]) -> int:
    """Count the number of times the dial lands on position 0 during a series of rotations."""
    positions = apply_rotations(rotations)
    return list(positions).count(0)


def apply_rotations(rotations: Iterable[int], start: int=50,) -> Generator[int, None, None]:
    """Given a list of dial rotations, determine the number of times that the
    dial lands on position 0.
    
    
    Examples
    --------
    >>> apply_rotations(["R10", "L20", "R30", "L40"])
    """
    all_dial_landings = accumulate(rotations, turn_dial, initial=start)
    return all_dial_landings


def process_rotation(rotation: str) -> int:
    """Convert a rotation string (e.g., 'R10', 'L20') to an integer value (10, -20)."""
    sign = 1 if rotation.startswith("R") else -1
    value = int(rotation.strip("LR"))
    return sign * value


def get_default_rotations() -> list[str]:
    """Return the default list of dial rotations provided by AoC."""
    return [
        "L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze dial rotations to count how many times the dial lands on position 0." 
    )
    parser.add_argument(
        "--input_file", type=Path, required=False, default=None, help="Path to the input file containing dial rotations."
    )
    args = parser.parse_args()
    if args.input_file is None:
        # Example Case
        rotations = get_default_rotations()
    else:
        rotations = args.input_file.expanduser().resolve().read_text().splitlines()
    
    # Data Munging
    rotations = list(map(process_rotation, rotations))

    # Part 1
    zero_count = count_zero_landings(rotations)
    print(f"The dial landed on position 0 a total of {zero_count} times.")

    # Part 2
    dial_size = 100
    count = 0
    position = 50
    for rotation in rotations:
        full_turns = int(rotation / dial_size)
        count += abs(full_turns)
        # assert turn_dial(position, rotation) == rotation - full_turns * dial_size
        rotation -= dial_size * full_turns # What's left after full turns

        if not rotation:
            continue

        new_position = position + rotation
        # Either you were close to 0 and rotation is negative and now new_position is negative
        # OR position is close to 99 and rotation is positive and new_position is >= 100
        if (
            (position > 0 and new_position <= 0)
            or (position <= 99 and new_position >= 100)
        ):
            count += 1
        position = new_position % 100
    print(f"The dial passed position 0 a total of {count} times.")
    assert count == 6858, "Incorrect answer for part 2!"