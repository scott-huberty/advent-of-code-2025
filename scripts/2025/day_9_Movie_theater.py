from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from operator import itemgetter
from pathlib import Path
from typing import List, Sequence, Tuple


# -----------------------------------------------------------------------------
# Data loading
# -----------------------------------------------------------------------------

def get_toy_data() -> str:
    return (
        "7,1\n"
        "11,1\n"
        "11,7\n"
        "9,7\n"
        "9,5\n"
        "2,5\n"
        "2,3\n"
        "7,3"
    )


def get_input_data(fpath: Path | None = None) -> str:
    if fpath is None:
        base = Path(__file__).resolve().parent
        fname = Path(__file__).with_suffix(".txt").name
        fpath = base / "assets" / fname
    return fpath.read_text()


# -----------------------------------------------------------------------------
# Geometry primitives
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Point:
    x: int
    y: int


def parse_points(text: str) -> List[Point]:
    return [Point(*map(int, line.split(","))) for line in text.splitlines()]


# ---- Rectangle helpers ------------------------------------------------------

def rect_area(a: Point, b: Point) -> int:
    """Inclusive axis-aligned rectangle area between diagonal corners."""
    return (abs(b.x - a.x) + 1) * (abs(b.y - a.y) + 1)


def rect_corners(a: Point, b: Point) -> List[Point]:
    """Return the four corners of the axis-aligned rectangle."""
    xmin, xmax = sorted((a.x, b.x))
    ymin, ymax = sorted((a.y, b.y))
    return [
        Point(xmin, ymin),
        Point(xmin, ymax),
        Point(xmax, ymin),
        Point(xmax, ymax),
    ]


def rect_edges(a: Point, b: Point) -> List[Tuple[Point, Point]]:
    """Return the four edges of the rectangle (each as a segment)."""
    p = rect_corners(a, b)
    # p = [LL, UL, LR, UR] in sorted order
    ll, ul, lr, ur = p
    return [
        (ll, lr),   # bottom
        (ul, ur),   # top
        (ll, ul),   # left
        (lr, ur),   # right
    ]


# ---- Segment / orientation helpers -----------------------------------------

def segments_properly_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """
    True if segments p1→q1 and p2→q2 intersect at an interior point
    (touching or colinear overlap does *not* count).
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # Strict intersection
    if (o1 * o2 < 0) and (o3 * o4 < 0):
        return True

    # Touching or overlapping is *not* proper
    if o1 == 0 and on_segment(p1, p2, q1):
        return False
    if o2 == 0 and on_segment(p1, q2, q1):
        return False
    if o3 == 0 and on_segment(p2, p1, q2):
        return False
    if o4 == 0 and on_segment(p2, q1, q2):
        return False

    return False


# ---- Point-in-polygon -------------------------------------------------------

def point_in_polygon(pt: Point, vertices: Sequence[Point]) -> bool:
    """
    Ray casting point-in-polygon test; returns True if inside or on the boundary.
    """
    inside = False
    n = len(vertices)

    for i in range(n):
        a = vertices[i]
        b = vertices[(i + 1) % n]  # i.e. if a is the very last vertice, b will be the first vertice
        # Boundary check
        if on_segment(a, pt, b):
            return True

        # Ray intersection check
        intersects = (a.y > pt.y) != (b.y > pt.y)
        if intersects:
            x_at_y = a.x + (b.x - a.x) * (pt.y - a.y) / (b.y - a.y)
            if pt.x <= x_at_y:
                inside = not inside

    return inside


def on_segment(a: Point, b: Point, c: Point) -> bool:
    """Return True if point b lies on segment a→c (inclusive)."""
    return (
        min(a.x, c.x) <= b.x <= max(a.x, c.x) and
        min(a.y, c.y) <= b.y <= max(a.y, c.y) and
        orientation(a, b, c) == 0
    )


def orientation(a: Point, b: Point, c: Point) -> int:
    """
    Orientation of triplet (a,b,c):
        > 0   counter-clockwise
        < 0   clockwise
        = 0   colinear
    """
    return (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)

# -----------------------------------------------------------------------------
# Polygon containment logic
# -----------------------------------------------------------------------------


def rect_is_inside_polygon(a: Point, b: Point, edges: Sequence[Tuple[Point, Point]]) -> bool:
    """
    Return True if the rectangle defined by diagonal corners a and b is fully
    inside or on the boundary of the polygon defined by `edges`.

    Conditions:
    - All rectangle corners inside/on polygon.
    - No rectangle edge properly intersects any polygon edge.
    """
    # Build polygon vertices from ordered edges
    verts = [start for start, _ in edges]  # this is the list of red tiles
    # Close the loop
    # verts.append(edges[0][0])

    # Corner test
    corners = rect_corners(a, b)
    if not all(point_in_polygon(pt, verts) for pt in corners):
        return False

    # Proper intersection check
    rect_sides = rect_edges(a, b)
    for rs0, rs1 in rect_sides:
        for pe0, pe1 in edges:
            if segments_properly_intersect(rs0, rs1, pe0, pe1):
                return False

    return True


# -----------------------------------------------------------------------------
# Main execution
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    USE_TOY = True

    text = get_toy_data() if USE_TOY else get_input_data()
    red_tiles = parse_points(text)

    # Build polygon edges (cyclic)
    polygon_edges = [
        (pt, red_tiles[i - 1]) for i, pt in enumerate(red_tiles)
    ]

    # -------------------------------------------------------------------------
    # Part 1: largest rectangle from any two corners
    # -------------------------------------------------------------------------
    rectangles = sorted(
        ((rect_area(a, b), a, b) for a, b in combinations(red_tiles, 2)),
        key=itemgetter(0),
        reverse=True,
    )

    largest_area = rectangles[0][0]
    print(f"9.1 - Biggest rectangle: {largest_area}")

    if USE_TOY:
        assert largest_area == 50

    # -------------------------------------------------------------------------
    # Part 2: largest rectangle fully inside the polygon
    # -------------------------------------------------------------------------
    # The Polygon formed by drawing a line that follows the red tiles:
    # # e,g with the Toy Data:
    #
    #
    #
    # ..............
    # .......0+++1..
    # .......+...+..
    # ..6++++7...+..
    # ..+........+..
    # ..5++++++4.+..
    # .........+.+..
    # .........3+2..
    # ..............

    
    # Since rectangles are sorted by size in descending order, we can stop after
    # The first valid one.
    for (area, a, b) in rectangles:
        if rect_is_inside_polygon(a, b, polygon_edges):
            break
    else:
        raise RuntimeError("No Rectangles lay entirely inside the Polygon!")

    # best_area, best_a, best_b = max(valid_rects, key=itemgetter(0))
    print(f"9.2 - Biggest rectangle: {area}")

    if USE_TOY:
        assert area == 24
        assert (a, b) == (Point(9, 5), Point(2, 3))
