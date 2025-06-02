# Pathfinding and Movement System

## Overview

This document describes the pathfinding and movement system used in the game. The system utilizes the A* algorithm to
find optimal paths on a grid, allowing characters or objects to navigate from a starting point to an endpoint while
avoiding obstacles.

## Components

### Coordinate Dataclass

- **Purpose**: Represents a coordinate in the grid.
- **Attributes**:
    - `x`: The x-coordinate on the grid.
    - `y`: The y-coordinate on the grid.

### PathCache Class

- **Purpose**: Caches paths to avoid recalculating them, improving performance.
- **Methods**:
    - `get_cached_path(start, end)`: Retrieves a cached path if the start and end coordinates match.
    - `update_cache(start, end, path)`: Updates the cache with a new path.

### PathFinder Class

- **Purpose**: Finds paths on a grid using the A* algorithm.
- **Attributes**:
    - `grid`: A grid representing the game world, where `0` is walkable and `1` is blocked.
    - `_cache`: An instance of `PathCache` to store and retrieve paths.
- **Methods**:
    - `find_path(start, end)`: Finds a path from the start to the end coordinates.
    - `_calculate_path(start, end)`: Uses the A* algorithm to calculate the path.

## Pathfinding Algorithm

### A* Algorithm

- **Description**: A* is a popular pathfinding algorithm that efficiently finds the shortest path between two points on
  a grid. It uses a heuristic to estimate the cost of reaching the goal from each node, which helps in prioritizing the
  exploration of promising paths.
- **Heuristic**: The algorithm uses the Euclidean distance or Manhattan distance as a heuristic to estimate the cost.
- **Diagonal Movement**: The algorithm supports diagonal movement, which can be enabled or disabled based on the game's
  requirements.

### Movement Types

- **DiagonalMovement.always**: Allows movement in all eight possible directions (horizontal, vertical, and diagonal).
- **DiagonalMovement.never**: Restricts movement to four directions (horizontal and vertical only).
- **DiagonalMovement.only_when_no_obstacle**: Allows diagonal movement only when there are no obstacles.
- **DiagonalMovement.if_at_most_one_obstacle**: Allows diagonal movement if there is at most one obstacle.

## Usage

### Finding a Path

To find a path from a starting point to an endpoint, use the `find_path` method of the `PathFinder` class:

```python
grid_matrix = [
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

path_finder = PathFinder(grid_matrix)
start = (0, 0)
end = (3, 3)
path = path_finder.find_path(start, end)
```