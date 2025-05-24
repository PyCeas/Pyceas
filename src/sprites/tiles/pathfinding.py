from dataclasses import dataclass

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


@dataclass(frozen=True)
class Coordinate:
    """A simple data class to represent a coordinate in the grid."""
    x: int
    y: int


class PathCache:
    def __init__(self) -> None:
        """
        Storing the start and end coordinates along with the path to avoid recalculating paths in a cached manner.
        """
        self.start: Coordinate | None = None
        self.end: Coordinate | None = None
        self.path: list[Coordinate] | None = None

    def get_cached_path(self, start: Coordinate, end: Coordinate) -> list[Coordinate] | None:
        """
        Retrieve the cached path if the start and end coordinates match.

        :param start: The starting coordinate.
        :param end: The ending coordinate.
        :return: The cached path or None if not found.
        """
        if self.start == start and self.end == end:
            return self.path
        return None

    def update_cache(self, start: Coordinate, end: Coordinate, path: list[Coordinate]) -> None:
        """
        Update the cache with a new path.

        :param start: The starting coordinate.
        :param end: The ending coordinate.
        :param path: The path to cache.
        """
        self.start = start
        self.end = end
        self.path = path

class PathFinder:
    MOVEMENT_TYPE = DiagonalMovement.always

    def __init__(self, grid_matrix):
        """
        Initialize the PathFinder with a grid matrix.

        :param grid_matrix: A 2D list representing the grid where 0 is walkable and 1 is blocked.
        """
        self.grid = Grid(matrix=grid_matrix)
        self._cache = PathCache()

    def find_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[list[int]]:
        """
        Find a path from start to end using A* algorithm.

        Args:
            start (tuple[int, int]): The starting tile coordinates (x, y).
            end (tuple[int, int]): The ending tile coordinates (x, y).
        """

        start_coord = Coordinate(start[0], start[1])
        end_coord = Coordinate(end[0], end[1])

        cached_path = self._cache.get_cached_path(start_coord, end_coord)
        if cached_path:
            return [[coord.x, coord.y] for coord in cached_path]

        self.grid.cleanup()  # Reset the grid state
        path = self._calculate_path(start_coord, end_coord)

        path_coordinates = [Coordinate(node.x, node.y) for node in path]
        self._cache.update_cache(start_coord, end_coord, path_coordinates)

        return [[coord.x, coord.y] for coord in path_coordinates]

    def _calculate_path(self, start: Coordinate, end: Coordinate) -> list:
        """Calculate the path using A* algorithm."""

        start_node = self.grid.node(start.x, start.y)
        end_node = self.grid.node(end.x, end.y)
        finder = AStarFinder(diagonal_movement=self.MOVEMENT_TYPE)
        path, _ = finder.find_path(start_node, end_node, self.grid)
        return path
