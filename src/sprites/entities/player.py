import pygame
from pygame import Surface, Vector2, FRect
from pygame.sprite import Group

from src.inventory import Inventory
from src.settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from src.sprites.base import BaseSprite


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

        # Initialize the player sprite
        player_square = frames[0] if isinstance(frames, (list, tuple)) and frames else Surface((TILE_SIZE, TILE_SIZE))
        player_square.fill("red")
        super().__init__(pos=pos, surf=player_square, groups=groups)

        # Animation frames
        self.frames = frames
        self.frame_index: float = 0.0

        self.position = pos
        self.selected: bool = False
        self.valid_moves: list = []  # Stores validly move around the player
        self.prev_tile = None
        self.path = []  # Stores the path to the destination tile

        # Inventory system
        self.inventory = Inventory()

        # Input handling
        self.mouse_have_been_pressed: bool = False

    def get_neighbor_tiles(self, grid, blocked_tiles=None):
        """Calculate and return all valid adjacent (neighbor) tiles for the player."""

        if blocked_tiles is None:
            blocked_tiles = []

        x, y = self.rect.topleft
        tile_size = grid.tile_size
        directions = [
            (0, -tile_size), (0, tile_size),  # Up, Down
            (-tile_size, 0), (tile_size, 0),  # Left, Right
            (-tile_size, -tile_size), (tile_size, -tile_size),  # Diagonal: Top-left, Top-right
            (-tile_size, tile_size), (tile_size, tile_size)  # Diagonal: Bottom-left, Bottom-right
        ]
        self.valid_moves = [
            (x + dx, y + dy)
            for dx, dy in directions
            if 0 <= x + dx < SCREEN_WIDTH
               and 0 <= y + dy < SCREEN_HEIGHT
               and (x + dx, y + dy) not in blocked_tiles
        ]


    def input(self, grid) -> None:
        """Handle player movement using instant tile-based logic"""

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        if not pygame.mouse.get_pressed()[0]:
            self.mouse_have_been_pressed = False
            return
        if self.mouse_have_been_pressed:
            return

        self.mouse_have_been_pressed = True

        # Calculate the tile coordinates from the grid
        tile_x, tile_y = grid.get_tile_coordinates(mouse_pos, self)
        player_tile = (self.rect.x // grid.tile_size, self.rect.y // grid.tile_size)
        target_tile = (tile_x // grid.tile_size, tile_y // grid.tile_size)

        # Find a path using A* algorithm
        path = grid.find_path(player_tile, target_tile)
        if path and len(path) > 1:
            # Move to the next tile in the path
            # self.path = path[1:] (will automatically find the fastest path)
            next_tile = path[1]
            self.rect.topleft = (next_tile[0] * grid.tile_size, next_tile[1] * grid.tile_size)
            self.prev_tile = player_tile

    def update(self, dt: float, grid=None) -> None:
        """Update the player's position and state."""
        if grid:
            self.get_neighbor_tiles(grid)  # Update valid moves
            self.input(grid)                # Handle input
            if self.path:
                next_tile = self.path.pop(0)
                self.rect.topleft = (next_tile[0] * grid.tile_size, next_tile[1] * grid.tile_size)
        # self.animate(dt)
