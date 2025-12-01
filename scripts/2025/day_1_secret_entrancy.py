import argparse
from pathlib import Path

from collections import abc

from itertools import accumulate

def count_zero_landings(rotations: abc.Iterable[int]) -> int:
    positions = apply_rotations(rotations)
    return list(positions).count(0)


def apply_rotations(rotations: abc.Iterable[str], start: int=50) -> abc.Generator[int, None, None]:
    """Given a list of dial rotations, determine the number of times that the
    dial lands on position 0.
    
    
    Examples
    --------
    >>> apply_rotations(["R10", "L20", "R30", "L40"])
    """

    # Right turns are positive, left turns are negative
    signs = [1 if rot.startswith("R") else -1 for rot in rotations]
    # Cast rotations to integers
    rotations = [int(rot.strip("LR")) for rot in rotations]
    # Combine directions and rotations
    rotations = [sign * rot for sign, rot in zip(signs, rotations)]
    # Calculate cumulative positions
    positions = accumulate(rotations, turn_dial, initial=start)
    return positions


def turn_dial(start: int, rotation: int) -> int:
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

    new_position = (start + rotation) % 100
    return new_position


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
        positions = [
            "L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"
        ]
    else:
        positions = args.input_file.expanduser().resolve().read_text().splitlines()
    zero_count = count_zero_landings(positions)
    print(f"The dial landed on position 0 a total of {zero_count} times.")
