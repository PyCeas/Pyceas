from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class PathFinder:
    def __init__(self, grid_matrix):
        """
        Initialize the PathFinder with a grid matrix.

        :param grid_matrix: A 2D list representing the grid where 0 is walkable and 1 is blocked.
        """
        self.grid = Grid(matrix=grid_matrix)
        self._cached_start = None
        self._cached_end = None
        self._cached_path = None

    def find_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[list[int]]:
        """
        Find a path from start to end using A* algorithm.

        Args:
            start (tuple[int, int]): The starting tile coordinates (x, y).
            end (tuple[int, int]): The ending tile coordinates (x, y).
        """
        if start == self._cached_start and end == self._cached_end:
            return self._cached_path

        self.grid.cleanup()  # Reset the grid state

        start_node = self.grid.node(start[0], start[1])
        end_node = self.grid.node(end[0], end[1])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, _ = finder.find_path(start_node, end_node, self.grid)

        self._cached_start = start
        self._cached_end = end
        self._cached_path = [[node.x, node.y] for node in path]
        return self._cached_path
