"""AoC 2025 Day 2: Gift Shop Inventory Validation. Key concept: String Periodicity."""
from pathlib import Path


def get_toy_data() -> str:
    """Return the toy data provided by AoC for testing."""
    return (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
        "824824821-824824827,2121212118-2121212124"
    )


def get_input_data() -> str:
    """Return the input data provided by AoC."""
    input_path = Path(__file__).resolve().parent / "assets" / "day_2_gift_shop_input.txt"
    return input_path.read_text()


def get_all_product_ids(string: str) -> list[int]:
    """Given a string of product ID ranges, return a list of all product IDs."""
    product_id_ranges = string.split(",")
    starts_stops = list(map(lambda s: s.split("-"), product_id_ranges))
    all_product_ids = []
    for start, stop in starts_stops:
        all_product_ids.extend(range(int(start), int(stop) + 1))
    return all_product_ids


def get_invalid_product_ids(product_ids: list[int]) -> list[int]:
    """Return a list of invalid product IDs from the given list."""
    invalid_product_ids = []
    for product_id in product_ids:
        if is_invalid(product_id):
            invalid_product_ids.append(product_id)
    return invalid_product_ids


def is_invalid(product_id: str) -> bool:
    """Determine if a product ID consists of a repetition of the same sequence of digits."""
    product_id = str(product_id)
    if len(product_id) % 2 != 0:
        return False
    mid_index = len(product_id) // 2
    first_half = product_id[:mid_index]
    second_half = product_id[mid_index:]
    return first_half == second_half


def is_periodic(product_id: str) -> bool:
    """Determine if string consists of a repeated substring.
    
    Uses the rotation method: https://algo.monster/liteproblems/459
    """
    product_id = str(product_id)
    return product_id in (product_id + product_id)[1:-1]


################# Part 1: String is a single repeated substring #######################


# First try with toy data from AoC
print("Testing with toy data:")
string = get_toy_data()
all_product_ids = get_all_product_ids(string)

invalid_product_ids = get_invalid_product_ids(all_product_ids)
print(f"Number of invalid product IDs: {len(invalid_product_ids)}")
assert len(invalid_product_ids) == 8, "Incorrect number of invalid product IDs found!"
assert sum(invalid_product_ids) == 1227775554, "Incorrect sum of invalid product IDs!"

# Now with our real input data
print("\nNow with real input data:")
string = get_input_data()
all_product_ids = get_all_product_ids(string)
invalid_product_ids = get_invalid_product_ids(all_product_ids)
print(f"Number of invalid product IDs: {len(invalid_product_ids)}")
print(f"Sum of invalid product IDs: {sum(invalid_product_ids)}")

############# Part 2: Detect periodicity in product IDs via rotation method ###########
#
# References:    https://algo.monster/liteproblems/459
#               https://www.baeldung.com/cs/check-string-periodicity

# First try with toy data from AoC
print("\nTesting periodicity with toy data:")
string = get_toy_data()
all_product_ids = get_all_product_ids(string)
periodic_product_ids = [pid for pid in all_product_ids if is_periodic(pid)]
print(f"Number of periodic product IDs: {len(periodic_product_ids)}")
assert len(periodic_product_ids) == 13, "Incorrect number of periodic product IDs found"
assert sum(periodic_product_ids) == 4174379265, "Incorrect sum of periodic product IDs!"

# Now with our real input data
print("\nNow with real input data:")
string = get_input_data()
all_product_ids = get_all_product_ids(string)
periodic_product_ids = [pid for pid in all_product_ids if is_periodic(pid)]
print(f"Number of periodic product IDs: {len(periodic_product_ids)}")
print(f"Sum of periodic product IDs: {sum(periodic_product_ids)}")