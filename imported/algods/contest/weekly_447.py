from typing import List



def countCoveredBuildings(n: int, buildings: List[List[int]]) -> int:
    # set for O(1) lookups
    building_set = {(x, y) for x, y in buildings}

    # maps for each direction to find closest buildings
    left_building = {}  # Key: (row, col), Value: closest building to the left
    right_building = {}  # Key: (row, col), Value: closest building to the right
    up_building = {}  # Key: (row, col), Value: closest building above
    down_building = {}  # Key: (row, col), Value: closest building below

    # Precompute closest buildings in each direction
    # Left to right pass
    for row in range(1, n+1):
        last_building = None
        for col in range(1, n+1):
            if (row, col) in building_set:
                last_building = (row, col)
            if last_building:
                left_building[(row, col)] = last_building

    # Right to left pass
    for row in range(1, n+1):
        last_building = None
        for col in range(n, 0, -1):
            if (row, col) in building_set:
                last_building = (row, col)
            if last_building:
                right_building[(row, col)] = last_building

    # Top to bottom pass
    for col in range(1, n+1):
        last_building = None
        for row in range(1, n+1):
            if (row, col) in building_set:
                last_building = (row, col)
            if last_building:
                up_building[(row, col)] = last_building

    # Bottom to top pass
    for col in range(1, n+1):
        last_building = None
        for row in range(n, 0, -1):
            if (row, col) in building_set:
                last_building = (row, col)
            if last_building:
                down_building[(row, col)] = last_building

    covered_count = 0
    for bx, by in buildings:
        # Check if this building can see other buildings in all 4 directions
        has_left = left_building.get((bx, by - 1)) is not None if by > 1 else False
        has_right = right_building.get((bx, by + 1)) is not None if by < n else False
        has_up = up_building.get((bx - 1, by)) is not None if bx > 1 else False
        has_down = down_building.get((bx + 1, by)) is not None if bx < n else False

        if has_left and has_right and has_up and has_down:
            covered_count += 1

    return covered_count

res = countCoveredBuildings(3, [[1,2],[2,2],[3,2],[2,1],[2,3]])
print(res)