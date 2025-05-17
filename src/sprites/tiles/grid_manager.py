import pygame
from pygame import Surface
import pytmx
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

        # The display surface should be provided by the calling context, e.g., PlayerCamera
        self.display_surface: Surface = pygame.display.get_surface()

    def create_grid_matrix(self) -> list[list[int]]:
        """
        Create a grid matrix from the Tiled map.
        Each tile is represented as 0 (walkable) or 1 (non-walkable).
        """
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == 'Sea':
                    for x, y, gid in layer:
                        matrix[y][x] = 0  # Walkable
                elif layer.name == 'Islands':
                    for x, y, gid in layer:
                        matrix[y][x] = 1  # Non-walkable
        return matrix

    def find_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[list[int]]:
        """
        Find a path from start to end using A* algorithm.
        """
        start_node = self.grid.node(start[0], start[1])
        end_node = self.grid.node(end[0], end[1])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, _ = finder.find_path(start_node, end_node, self.grid)

        return [[node.x, node.y] for node in path]

    def get_tile_coordinates(self, mouse_pos: tuple[int, int], player: object) -> tuple[int, int]:
        """
        Get the tile coordinates based on mouse position.
        This is used to determine where the player can move.
        """
        x, y = mouse_pos

        return x // self.tile_size * self.tile_size, y // self.tile_size * self.tile_size

    def draw(self, mouse_pos: tuple[int, int]):
        """
        Draw the grid on the screen.
        Highlight the tile under the mouse cursor.
        """
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.display_surface, (0, 255, 0, 50), rect, 1)  # Draw grid lines

        start = (mouse_pos[0] // self.tile_size, mouse_pos[1] // self.tile_size)
        end = (self.width - 1, self.height - 1)
        path = self.find_path(start, end)
        for x, y in path:
            rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(self.display_surface, (0, 255, 0, 50), rect, 2)

# class GridManager:
#     """Handles grid rendering and interaction."""
#
#     def __init__(
#         self,
#         display_surface: pygame.Surface,
#         tile_size: int = TILE_SIZE,
#         grid_color: str = "grey",
#         hover_color: str = "azure4"
#     ):
#         self.display_surface: pygame.Surface = display_surface
#         self.tile_size: int = tile_size
#         self.grid_color: str = grid_color
#         self.hover_color: str = hover_color
#         self.overlay_alpha: int = 50    # Transparency level (0-255)
#         self.block_size: int = 64
#         self.coordinates: dict[tuple[int, int], tuple[int, int]] = {}
#
#     def draw(self, mouse_pos: tuple[int, int], valid_moves: set[tuple[int, int]] = None) -> None:
#
#         overlay: Surface = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 0))  # Fully transparent background
#
#         font = pygame.font.SysFont("Arial", 12)
#
#         for x in range(0, self.display_surface.get_width(), self.block_size):
#             for y in range(0, self.display_surface.get_height(), self.block_size):
#                 rect = pygame.Rect(x, y, self.block_size, self.block_size)
#
#                 # Highlight valid tiles
#                 if valid_moves and (x, y) in valid_moves:
#                     pygame.draw.rect(overlay, (0, 255, 0, 100), rect)
#                 elif rect.collidepoint(mouse_pos):
#                     pygame.draw.rect(overlay, (0, 0, 255, 100), rect)
#
#                 # Draw grid lines
#                 pygame.draw.rect(self.display_surface, self.grid_color, rect, 1)
#                 self.coordinates[(x, y)] = (x // self.block_size, y // self.block_size)
#
#                 # Render the x, y integers
#                 text = font.render(f"({self.coordinates[(x, y)][0]}, {self.coordinates[(x, y)][1]})", True, (0, 0, 0))
#                 text_rect = text.get_rect(center=rect.center)
#                 self.display_surface.blit(text, text_rect)
#
#         # Blit the transparent overlay onto the display surface
#         self.display_surface.blit(overlay, (0, 0))
#
#     def get_tile_coordinates(self, mouse_pos: tuple[int, int], player: object) -> tuple[int, int]:
#         x, y = mouse_pos
#         player_x, player_y = player.position
#         max_distance: int = 6
#
#         # Calculate the distance from the player's position to the mouse position
#         distance = ((x - player_x) ** 2 + (y - player_y) ** 2) ** 0.5
#
#         return (x // self.block_size * self.block_size, y // self.block_size * self.block_size) if distance > max_distance else None
#
#     def get_coordinates(self, x, y):
#         """Returns the coordinates of a tile at position (x, y)."""
#
#         return self.coordinates.get((x, y))