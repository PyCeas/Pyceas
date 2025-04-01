import heapq
from typing import Any

from src.sprites.tiles.grid_manager import GridManager

def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    """Calculate the Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start: tuple[int, int], goal: tuple[int, int], grid: GridManager, blocked_tiles: set[tuple[int, int]]) -> \
list[Any] | bool:
    if blocked_tiles is None:
        blocked_tiles = set()

    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-directional movement
    close_set = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (f_score[start], start))

    grid_width = grid.display_surface.get_width() // grid.block_size
    grid_height = grid.display_surface.get_height() // grid.block_size

    while oheap:
        current = heapq.heappop(oheap)[1]
        print(f"Current node: {current}")

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            tentative_g_score = g_score[current] + 1

            if 0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height:
                if neighbor in blocked_tiles:
                    print(f"Blocked tile: {neighbor}")
                    continue
            else:
                print(f"Out of bounds: {neighbor}")
                continue

            if neighbor in close_set and tentative_g_score >= g_score.get(neighbor, 0):
                print(f"Already evaluated: {neighbor}")
                continue

            if tentative_g_score < g_score.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (f_score[neighbor], neighbor))
                print(f"Added to open set: {neighbor}, f_score: {f_score[neighbor]}")

    print("No path found.")
    return False