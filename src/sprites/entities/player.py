import math

import pygame
from pygame import Surface, Vector2, FRect
from pygame.sprite import Group

from src.inventory import Inventory
from src.pathfinding import a_star_search
from src.settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from src.sprites.base import BaseSprite
from src.sprites.tiles.grid_manager import GridManager


class Player(BaseSprite):
    """Handles player interaction with the grid, using instant tile movement."""
    rect: FRect


    def __init__(
        self,
        pos: tuple[int, int],
        frames: list[Surface],
        groups: tuple[Group, ...] = (),
    ) -> None:
        """
        Initialize the player.
        :param pos: Starting position of the player.
        :param frames: A list of frames for player animation.
        :param groups: Sprite groups the player belongs to.
        """

        # Use the first frame as the base surface
        first_frame = frames[0] if isinstance(frames, (list, tuple)) and frames else Surface((TILE_SIZE, TILE_SIZE))
        first_frame.fill("red")
        super().__init__(pos=pos, surf=first_frame, groups=groups)

        # Animation frames
        self.frames = frames
        self.frame_index: float = 0.0

        self.position = (pos[0] // TILE_SIZE, pos[1] // TILE_SIZE)  # Convert to tile coordinates
        self.target_tile = None
        self.valid_moves: list = [] # Stores valid moves around the player
        self.path = []
        self.speed: int = 200    # Pixels per second

        # Inventory system
        self.inventory = Inventory()

        # Input handling
        self.mouse_pressed: bool = False

    def get_adjacent_tiles(self, grid, blocked_tiles=None):
        """Calculate and return all valid adjacent tiles."""

        if blocked_tiles is None:
            blocked_tiles = []
        x, y = self.position

        directions = [
            (0, -1), (0, 1),    # Up, Down
            (-1, 0), (1, 0)     # Left, Right
        ]
        self.valid_moves = [
            (x + dx, y + dy)
            for dx, dy in directions
            if 0 <= x + dx < SCREEN_WIDTH
               and 0 <= y + dy < SCREEN_HEIGHT
               and (x + dx, y + dy) not in blocked_tiles
        ]

    def input(self, grid: GridManager, blocked_tiles: set[tuple[int, int]]) -> None:
        """Handle player movement and validate adjacent tiles."""

        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        # print(f"Mouse position: {mouse_pos}")

        if pygame.mouse.get_pressed()[0]:  # Left click
            tile_x, tile_y = grid.get_tile_coordinates(mouse_pos)
            print(f"Tile coordinates: {tile_x}, {tile_y}")
            if tile_x is not None and tile_y is not None:
                if (tile_x, tile_y) != self.position:
                    self.target_tile = (int(tile_x), int(tile_y))
                    self.path = self.calculate_path(self.position, self.target_tile, grid, blocked_tiles)
                    if not self.path:
                        print("No valid path found.")
                    else:
                        print(f"Path: {self.path}")

                if (tile_x, tile_y) in self.valid_moves:  # Move only to valid tiles
                    self.rect.topleft = (tile_x * grid.block_size, tile_y * grid.block_size)
                    self.position = (tile_x, tile_y)
                    # print(f"Moved to: {self.rect.topleft}")

    @staticmethod
    def calculate_path(start: tuple[int, int], target: tuple[int, int], grid: GridManager,
                       blocked_tiles: set[tuple[int, int]]) -> list[tuple[int, int]]:
        """Calculate the path from start to target using A*."""
        return a_star_search(start, target, grid, blocked_tiles)

    def move_along_path(self, dt: float) -> None:
        """Move the player along the calculated path."""
        if self.path:
            next_tile = self.path[0]
            next_pos = (next_tile[0] * TILE_SIZE, next_tile[1] * TILE_SIZE)
            distance = math.hypot(next_pos[0] - self.position[0], next_pos[1] - self.position[1])
            if distance < self.speed * dt:
                self.rect.topleft = next_pos
                self.position = next_tile
                self.path.pop(0)
            else:
                direction = ((next_pos[0] - self.rect.x) / distance, (next_pos[1] - self.rect.y) / distance)
                self.rect.x += direction[0] * self.speed * dt
                self.rect.y += direction[1] * self.speed * dt


    def update(self, dt: float, grid=None, blocked_tiles: set[tuple[int, int]] = None) -> None:
        """Update the player's position and state."""

        # print(f"Player instance created: {id(self)}")
        if grid:
            self.get_adjacent_tiles(grid, blocked_tiles)   # Update valid moves
            self.input(grid, blocked_tiles)     # Handle input
            grid.draw_path(self.path)       # Draw the path on the grid
        self.move_along_path(dt)         # Move along the path
        self.animate(dt)
