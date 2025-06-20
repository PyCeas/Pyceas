import numpy as np
import pygame  # type: ignore
import pytmx
from pygame import Surface  # type: ignore

from src.settings import TILE_SIZE
from src.sprites.tiles.pathfinding import PathFinder


class GridManager:
    def __init__(
            self, tmx_map: pytmx.TiledMap = None, tile_size: int = TILE_SIZE, grid_matrix: np.ndarray | None = None
    ):
        if grid_matrix is not None:
            self.grid_matrix = grid_matrix
            self.height, self.width = grid_matrix.shape
            self.tmx_map = None
        else:
            if tmx_map is None:
                raise ValueError("Either tmx_map or grid_matrix must be provided")
            self.tmx_map = tmx_map
            self.width = tmx_map.width  # Number of tiles wide
            self.height = tmx_map.height  # Number of tiles high
            self.grid_matrix = self.create_grid_matrix()
        self.tile_size = tile_size
        self.path_finder = PathFinder(self.grid_matrix)

        self.display_surface: Surface | None = pygame.display.get_surface()
        self.font = pygame.font.SysFont(None, 12)
        self.coordinate_surfaces = self._preload_coordinates_surfaces()

    def _preload_coordinates_surfaces(self):
        coordinate_surfaces = {}
        for y in range(self.height):
            for x in range(self.width):
                text_surface = self.font.render(f"{x}, {y}", True, (255, 255, 255))
                coordinate_surfaces[(x, y)] = text_surface.convert_alpha()
        return coordinate_surfaces

    def create_grid_matrix(self) -> np.ndarray:
        """
        Create a grid matrix from the Tiled map.
        Each tile is represented as 0 (walkable) or 1 (non-walkable).
        """
        if self.tmx_map is None:
            raise ValueError("TMX map must be None when creating grid matrix")
        matrix = np.zeros((self.height, self.width), dtype=int)  # Initialize with zeros (walkable)
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == "Sea":
                    for x, y, gid in layer:
                        matrix[y, x] = 0  # Walkable
                elif layer.name == "Islands" or layer.name == "Shallow Sea":
                    for x, y, gid in layer:
                        matrix[y, x] = 1  # Non-walkable
        return matrix

    # Not the best way to do this, but it works for now
    def find_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[list[int]]:
        return self.path_finder.find_path(start, end)

    def get_tile_coordinates(
            self,
            mouse_pos: tuple[int, int],
            camera_offset: pygame.math.Vector2 | None = None,
            camera_scale: float | None = None,
    ) -> tuple[int, int]:
        """
        Get the tile indices (x, y) based on mouse position.
        This is used to determine where the player can move.

        Args:
            mouse_pos (tuple[int, int]): The current mouse position.
            camera_offset (tuple[int, int], optional): The camera offset from PlayerCamera (Vector2)
            camera_scale (float, optional): The camera scale from PlayerCamera (float)
        """
        if camera_offset is None:
            camera_offset = pygame.math.Vector2()
        if camera_scale is None:
            camera_scale = 1.0
        world_x, world_y = self._convert_mouse_to_world(mouse_pos, camera_offset, camera_scale)
        grid_x, grid_y = self._convert_world_to_grid(world_x, world_y)
        return self._clamp_grid_coordinates(grid_x, grid_y)

    @staticmethod
    def _convert_mouse_to_world(
            mouse_pos: tuple[int, int], camera_offset: pygame.math.Vector2, camera_scale: float
    ) -> tuple[float, float]:
        # Adjust the mouse position to world coordinates by reversing the camera's position and scale
        world_x = (mouse_pos[0] - camera_offset.x) / camera_scale
        world_y = (mouse_pos[1] - camera_offset.y) / camera_scale
        return world_x, world_y

    def _convert_world_to_grid(self, world_x: float, world_y: float) -> tuple[int, int]:
        # Convert world coordinates to grid coordinates
        grid_x = int(world_x // self.tile_size)
        grid_y = int(world_y // self.tile_size)
        return grid_x, grid_y

    def _clamp_grid_coordinates(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        # Clamp grid coordinates to the grid boundaries
        grid_x = max(0, min(self.width - 1, grid_x))
        grid_y = max(0, min(self.height - 1, grid_y))
        return grid_x, grid_y

    def draw(
            self,
            player_pos: tuple[int, int],
            mouse_pos: tuple[int, int],
            camera_offset: pygame.math.Vector2 | None = None,
            camera_scale: float | None = None,
            visible_radius: int | None = None,
    ) -> None:
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
        if camera_offset is None:
            camera_offset = pygame.math.Vector2()
        if camera_scale is None:
            camera_scale = 1.0
        if visible_radius is None:
            visible_radius = 5
        player_grid_x, player_grid_y = self._convert_world_to_grid(*player_pos)
        mouse_grid_x, mouse_grid_y = self.get_tile_coordinates(mouse_pos, camera_offset, camera_scale)

        visible_start_x, visible_start_y, visible_end_x, visible_end_y = self._calculate_visible_area(
            player_grid_x, player_grid_y, visible_radius
        )

        self._draw_grid_lines(
            visible_start_x, visible_start_y, visible_end_x, visible_end_y, camera_offset, camera_scale
        )

        self._draw_path(player_grid_x, player_grid_y, mouse_grid_x, mouse_grid_y, camera_offset, camera_scale)

        self._draw_mouse_indicator(mouse_grid_x, mouse_grid_y, camera_offset, camera_scale)

    def _calculate_visible_area(
            self, player_grid_x: int, player_grid_y: int, visible_radius: int
    ) -> tuple[int, int, int, int]:
        visible_start_x = max(0, player_grid_x - visible_radius)
        visible_start_y = max(0, player_grid_y - visible_radius)
        visible_end_x = min(self.width, player_grid_x + visible_radius + 1)
        visible_end_y = min(self.height, player_grid_y + visible_radius + 1)
        return visible_start_x, visible_start_y, visible_end_x, visible_end_y

    def _draw_grid_lines(
            self,
            visible_start_x: int,
            visible_start_y: int,
            visible_end_x: int,
            visible_end_y: int,
            camera_offset: pygame.math.Vector2,
            camera_scale: float,
    ) -> None:
        for y in range(visible_start_y, visible_end_y):
            for x in range(visible_start_x, visible_end_x):
                if self.display_surface is None:
                    raise RuntimeError("Display surface must be initialized")
                screen_x, screen_y = self._convert_to_screen_coordinates(x, y, camera_offset, camera_scale)
                rect = pygame.Rect(screen_x, screen_y, self.tile_size * camera_scale, self.tile_size * camera_scale)
                pygame.draw.rect(self.display_surface, "dark grey", rect, 1)  # Draw grid lines

                text_surface = self.coordinate_surfaces[(x, y)]
                text_rect = text_surface.get_rect(
                    center=(screen_x + self.tile_size * camera_scale / 2, screen_y + self.tile_size * camera_scale / 2)
                )
                self.display_surface.blit(text_surface, text_rect)

    def _convert_to_screen_coordinates(
            self, x: int, y: int, camera_offset: pygame.math.Vector2, camera_scale: float
    ) -> tuple[float, float]:
        world_x = x * self.tile_size
        world_y = y * self.tile_size
        screen_x = world_x * camera_scale + camera_offset.x
        screen_y = world_y * camera_scale + camera_offset.y
        return screen_x, screen_y

    def _draw_path(
            self,
            start_x: int,
            start_y: int,
            end_x: int,
            end_y: int,
            camera_offset: pygame.math.Vector2,
            camera_scale: float,
    ) -> None:
        start = (start_x, start_y)
        end = (end_x, end_y)

        if 0 <= start[0] < self.width and 0 <= start[1] < self.height:
            path = self.path_finder.find_path(start, end)
            for x, y in path:
                if self.display_surface is None:
                    raise RuntimeError("Display surface must be initialized")
                screen_x, screen_y = self._convert_to_screen_coordinates(x, y, camera_offset, camera_scale)
                rect = pygame.Rect(screen_x, screen_y, self.tile_size * camera_scale, self.tile_size * camera_scale)
                pygame.draw.rect(self.display_surface, "green", rect, 2)  # Draw path tiles

    def _draw_mouse_indicator(
            self, mouse_grid_x: int, mouse_grid_y: int, camera_offset: pygame.math.Vector2, camera_scale: float
    ) -> None:
        if self.display_surface is None:
            raise RuntimeError("Display surface must be initialized")
        dot_x = mouse_grid_x * self.tile_size * camera_scale + camera_offset.x
        dot_y = mouse_grid_y * self.tile_size * camera_scale + camera_offset.y
        pygame.draw.circle(self.display_surface, (0, 255, 0), (dot_x, dot_y), 5)  # Green circle at tile coordinates
