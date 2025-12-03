"""AoC 2025 Day 3: Lobby Layout - Joltage Maximization. Key concept: Monotonic Stack."""
from pathlib import Path


def get_toy_data() -> str:
    """Return the AoC example Joltage data."""
    return (
        "987654321111111\n"
        "811111111111119\n"
        "234234234234278\n"
        "818181911112111\n"
    )


def get_input_data() -> str:
    """Return the AoC input Joltage data."""
    input_path = Path(__file__).resolve().parent / "assets" / "day_3_lobby.txt"
    return input_path.read_text()


def max_joltage(bank: str, n_cells: int=2) -> str:
    """
    Given a digit string `foo` and the number of digits `remaining`
    to keep, return the lexicographically largest possible number
    formed by removing len(foo) - remaining digits (keeping order).
    """
    # How many digits we can delete
    k = len(bank) - n_cells
    stack: list[str] = []

    for d in bank:
        # While we can still remove digits and the last chosen digit
        # is smaller than the current one, pop it to make the number larger.
        while k > 0 and stack and stack[-1] < d:
            import pdb; pdb.set_trace()
            stack.pop()
            k -= 1
        stack.append(d)

    # If we still have removals left, drop from the end
    if k > 0:
        stack = stack[:-k]

    return int("".join(stack))


banks = get_toy_data().strip().split("\n")
max_voltages = []
for bank in banks:
    voltage = max_joltage(bank)
    max_voltages.append(voltage)
max_voltage = sum(max_voltages)

assert max_voltages == [98, 89, 78, 92]
assert max_voltage == 357

banks = get_input_data().strip().split("\n")
max_voltages = []
for bank in banks:
    voltage = max_joltage(bank)
    max_voltages.append(voltage)
max_voltage = sum(max_voltages)

print(f"The highest possible total voltage is {max_voltage}.")
assert max_voltage == 16946

# Part 2 - now with 12 cells per bank
banks = get_toy_data().strip().split("\n")

max_voltages = []
for bi, bank in enumerate(banks):
    voltage = max_joltage(bank, n_cells=12)
    max_voltages.append(voltage)
max_voltage = sum(max_voltages)
assert max_voltages == [987654321111, 811111111119, 434234234278, 888911112111]
assert max_voltage == 3121910778619

# Part 2 with input data:
banks = get_input_data().strip().split("\n")
max_voltages = []
for bi, bank in enumerate(banks):
    voltage = max_joltage(bank, n_cells=12)
    max_voltages.append(voltage)
max_voltage = sum(max_voltages)
print(f"The highest possible total voltage with 12 cells is {max_voltage}.")