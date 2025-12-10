from collections import Counter
from itertools import combinations
import math
from pathlib import Path

def get_toy_data():
    return (
        "162,817,812\n"
        "57,618,57\n"
        "906,360,560\n"
        "592,479,940\n"
        "352,342,300\n"
        "466,668,158\n"
        "542,29,236\n"
        "431,825,988\n"
        "739,650,466\n"
        "52,470,668\n"
        "216,146,977\n"
        "819,987,18\n"
        "117,168,530\n"
        "805,96,715\n"
        "346,949,466\n"
        "970,615,88\n"
        "941,993,340\n"
        "862,61,35\n"
        "984,92,344\n"
        "425,690,689"
    )


def get_input_data(fpath: Path=None) -> str:
    if fpath is None:
        fpath = Path(__file__).resolve().parent / "assets" / Path(__file__).with_suffix(".txt").name
    return fpath.read_text()



def test_part_1():
    puzzle = get_toy_data()
    coords = [tuple(map(int, s.split(","))) for s in puzzle.splitlines()]
    edges = compute_distances(coords)
    assert edges[0][1:] == ((162, 817, 812), (425, 690, 689))

    sizes, _ = union_find(coords, edges)
    assert sizes == [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1], f"wrong sizes!: {sizes}"
    return sizes


def compute_distances(coords):
    """Better."""
    edges = []
    for a, b in combinations(coords, 2):
        edges.append((math.dist(a, b), a, b))
    edges.sort(key=lambda x: x[0])
    return edges


def union_find(coords, edges, max_connections=10):
    dsu = DSU(coords)

    connections_made = 0

    for dist, a, b in edges:
        if max_connections is None:
            if dsu.union(a, b):
                connections_made += 1
            if connections_made == len(coords) -1:
                final_union = (a[0] * b[0])
                break
        else:
            dsu.union(a, b)
            connections_made += 1
            if connections_made == max_connections:
                final_union = (a[0] * b[0])
                break

    # After max_connections merges (max_connections), extract circuit sizes
    component_sizes = Counter()
    for item in coords:
        root = dsu.find(item)
        component_sizes[root] = dsu.size[root]
    sizes = sorted(component_sizes.values(), reverse=True)
    return sizes, final_union


class DSU:
    """Dream State University I Mean Disjoint Set Union"""
    def __init__(self, coords):
        # Each coordinate is its own parent initially.
        self.parent = {x: x for x in coords}
        self.size = {x: 1 for x in coords}

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # nothing to do
        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def solve_part_1():
    puzzle = get_input_data()
    coords = [tuple(map(int, s.split(","))) for s in puzzle.splitlines()]

    edges = compute_distances(coords)
    sizes, _ = union_find(coords, edges, max_connections=1000)
    return sizes[0] * sizes[1] * sizes[2]


def test_part_2():
    puzzle = get_toy_data()
    coords = [tuple(map(int, s.split(","))) for s in puzzle.splitlines()]

    edges = compute_distances(coords)
    sizes, final_union = union_find(coords, edges, max_connections=None)
    assert final_union == 25272
    return final_union


def solve_part_2():
    puzzle = get_input_data()
    coords = [tuple(map(int, s.split(","))) for s in puzzle.splitlines()]

    edges = compute_distances(coords)
    _, final_union = union_find(coords, edges, max_connections=None)
    return final_union



if __name__ == "__main__":
    answer = solve_part_1() 
    assert answer == 140008
    test_part_2()
    answer_2 = solve_part_2()
    assert answer_2 == 9253260633