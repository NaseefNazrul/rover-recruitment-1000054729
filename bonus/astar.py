"""A* path planner for a rover on a grid map.

this file has 5 bugs. Find them, fix them, and explain them.

The map is a 2D grid. grid[y][x] is the cost to drive INTO that cell:
    WALL (-1) = rock, the rover cannot go there
    1         = normal ground
    5         = sand (slow, costs more)

The rover moves up, down, left or right (no diagonal moves).
"""
import heapq

WALL = -1


def cell_cost(grid, x, y):
    """Cost to drive into cell (x, y). Returns WALL if it is a rock."""
    return grid[y][x]   # As it iterates through row first


def heuristic(a, b):
    """Guess of the cost from cell a to cell b (Manhattan distance)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Wrong formula 


def neighbours(grid, node):
    """All cells next to `node` that the rover can drive into."""
    x, y = node
    height = len(grid)
    width = len(grid[0])
    result = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:      # Out of bounds
            if cell_cost(grid, nx, ny) != WALL:
                result.append((nx, ny))
    return result


def build_path(came_from, current):
    """Walk back from the goal to the start using came_from."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(grid, start, goal):
    """Find the cheapest path from start to goal.

    Returns (path, cost, explored):
        path     = list of (x, y) cells from start to goal, or None if no path
        cost     = total cost of the path, or None if no path
        explored = set of cells that A* took out of the open list
    """
    open_list = [(heuristic(start, goal), start)]  # items are (f, cell)
    g = {start: 0}           # best known cost from start to each cell
    came_from = {}           # came_from[cell] = the cell we came from
    explored = set()

    while open_list: # Infinite loop
        f, current = heapq.heappop(open_list)
        if current in explored:
            continue
        explored.add(current)

        if current == goal:
            return build_path(came_from, current), g[current], explored

        for nb in neighbours(grid, current):
            new_g = g[current] + cell_cost(grid, nb[0], nb[1])       # g(x) + cost
            if nb not in g or new_g < g[nb]:
                g[nb] = new_g
                came_from[nb] = current
                heapq.heappush(open_list, (new_g + heuristic(nb, goal), nb))

    return None, None, explored
