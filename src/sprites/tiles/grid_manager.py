import pygame
from pygame import Surface
import pytmx
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

from src.settings import TILE_SIZE

class GridManager:

    def __init__(self, tmx_map: pytmx.TiledMap, tile_size: int = TILE_SIZE):
        if tmx_map is None:
            raise ValueError("tmx_map cannot be None")

        self.tmx_map = tmx_map
        self.tile_size = tile_size
        self.width = tmx_map.width  # Number of tiles wide
        self.height = tmx_map.height  # Number of tiles high
        self.grid_matrix = self.create_grid_matrix()
        self.grid = Grid(matrix=self.grid_matrix)
        self._cached_start = None
        self._cached_end = None
        self._cached_path = []

        self.display_surface: Surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(None, 12)
        self.coordinate_surfaces = {}

        for y in range(self.height):
            for x in range(self.width):
                text_surface = self.font.render(f"{x}, {y}", True, (255, 255, 255))
                self.coordinate_surfaces[(x, y)] = text_surface.convert_alpha()

    def create_grid_matrix(self) -> np.ndarray:
        """
        Create a grid matrix from the Tiled map.
        Each tile is represented as 0 (walkable) or 1 (non-walkable).
        """
        matrix = np.zeros((self.height, self.width), dtype=int)  # Initialize with zeros (walkable)
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == 'Sea':
                    for x, y, gid in layer:
                        matrix[y, x] = 0  # Walkable
                elif layer.name == 'Islands' or layer.name == 'Shallow Sea':
                    for x, y, gid in layer:
                        matrix[y, x] = 1  # Non-walkable
        return matrix

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

    def get_tile_coordinates(self, mouse_pos: tuple[int, int], camera_offset: pygame.math.Vector2 = None,
                             camera_scale: float = None) -> tuple[int, int]:
        """
        Get the tile indices (x, y) based on mouse position.
        This is used to determine where the player can move.

        Args:
            mouse_pos (tuple[int, int]): The current mouse position.
            camera_offset (tuple[int, int], optional): The camera offset from PlayerCamera (Vector2)
            camera_scale (float, optional): The camera scale from PlayerCamera (float)
        """

        # Reverse the camera transformations to get world coordinates
        world_x = (mouse_pos[0] - camera_offset.x) / camera_scale
        world_y = (mouse_pos[1] - camera_offset.y) / camera_scale

        # Convert world coordinates to grid coordinates
        grid_x = int(world_x // self.tile_size)
        grid_y = int(world_y // self.tile_size)

        # Clamp grid coordinates to the grid boundaries
        grid_x = max(0, min(self.width - 1, grid_x))
        grid_y = max(0, min(self.height - 1, grid_y))

        return grid_x, grid_y

    def draw(self,
             player_pos: tuple[int, int],
             mouse_pos: tuple[int, int],
             camera_offset: pygame.math.Vector2 = None,
             camera_scale: float = None,
             visible_radius: int = None) -> None:
        """
        Draw the grid on the screen.
        Highlight the tile under the mouse cursor.

        Args:
            player_pos (tuple[int, int]): The current player position.
            mouse_pos (tuple[int, int]): The current mouse position.
            camera_offset (tuple[int, int], optional): The camera offset from PlayerCamera (Vector2)
            camera_scale (float, optional): The camera scale from PlayerCamera (float)
            visible_radius (int, optional): The radius of the visible area around the player.
        """

        # Convert player position to grid coordinates
        player_grid_x = int(player_pos[0] // self.tile_size)
        player_grid_y = int(player_pos[1] // self.tile_size)

        # Get mouse grid coordinates with camera offset and scale
        mouse_grid_x, mouse_grid_y = self.get_tile_coordinates(mouse_pos, camera_offset, camera_scale)

        # Calculate the visible area based on camera offset and scale
        visible_start_x = max(0, player_grid_x - visible_radius)
        visible_start_y = max(0, player_grid_y - visible_radius)
        visible_end_x = min(self.width, player_grid_x + visible_radius + 1)
        visible_end_y = min(self.height, player_grid_y + visible_radius + 1)

        for y in range(visible_start_y, visible_end_y):
            for x in range(visible_start_x, visible_end_x):
                # Calculate world position
                world_x = x * self.tile_size
                world_y = y * self.tile_size

                # Convert to screen coordinates
                screen_x = world_x * camera_scale + camera_offset.x
                screen_y = world_y * camera_scale + camera_offset.y

                rect = pygame.Rect(screen_x, screen_y,
                                   self.tile_size * camera_scale,
                                   self.tile_size * camera_scale)
                pygame.draw.rect(self.display_surface, "dark grey", rect, 1)  # Draw grid lines

                # Calculate the position to draw the text (center of the tile)
                text_surface = self.coordinate_surfaces[(x, y)]

                # Calculate the position to draw the text (center of the tile)
                text_rect = text_surface.get_rect(center=(screen_x + self.tile_size * camera_scale / 2,
                                                          screen_y + self.tile_size * camera_scale / 2))

                # Draw the text on the screen
                self.display_surface.blit(text_surface, text_rect)

        # Clamp pathfinding start and end points to the grid boundaries
        start = (player_grid_x, player_grid_y)
        end = (mouse_grid_x, mouse_grid_y)

        # Path finding and drawing a path
        if 0 <= start[0] < self.width and 0 <= start[1] < self.height:
            path = self.find_path(start, end)
            for x, y in path:
                # Convert path coordinates to the screen position
                screen_x = x * self.tile_size * camera_scale + camera_offset.x
                screen_y = y * self.tile_size * camera_scale + camera_offset.y
                rect = pygame.Rect(screen_x, screen_y,
                                   self.tile_size * camera_scale,
                                   self.tile_size * camera_scale)
                pygame.draw.rect(self.display_surface, "green", rect, 2)  # Draw path tiles

        # Draw the green dot at the mouse grid coordinates
        dot_x = mouse_grid_x * self.tile_size * camera_scale + camera_offset.x
        dot_y = mouse_grid_y * self.tile_size * camera_scale + camera_offset.y
        pygame.draw.circle(self.display_surface, (0, 255, 0), (dot_x, dot_y), 5)  # Green circle at tile coordinates
