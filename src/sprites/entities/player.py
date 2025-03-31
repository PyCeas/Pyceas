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

        # Use the first frame as the base surface
        first_frame = frames[0] if isinstance(frames, (list, tuple)) and frames else Surface((TILE_SIZE, TILE_SIZE))
        first_frame.fill("red")
        super().__init__(pos=pos, surf=first_frame, groups=groups)

        # Animation frames
        self.frames = frames
        self.frame_index: float = 0.0

        self.position = pos
        self.selected: bool = False
        self.valid_moves: list = []  # Stores valid moves around the player
        self.prev_tile = None

        # Inventory system
        self.inventory = Inventory()

        # Input handling
        self.mouse_have_been_pressed: bool = False

    def get_adjacent_tiles(self, grid, blocked_tiles=[]):
        """Calculate and return all valid adjacent (neighbor) tiles for the player."""

        if blocked_tiles is None:
            blocked_tiles = []
        x, y = self.rect.topleft
        tile_size = grid.block_size
        directions = [
            (0, -tile_size), (0, tile_size),    # Up, Down
            (-tile_size, 0), (tile_size, 0)     # Left, Right
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

        # if not pygame.mouse.get_pressed()[0]:
        #     self.mouse_have_been_pressed = False
        #     return
        #
        # # Get the tile coordinates from the grid
        # mouse_pos = pygame.mouse.get_pos()
        # tile_x, tile_y = grid.get_tile_coordinates(mouse_pos, self)
        #
        # if (tile_x, tile_y) and (tile_x, tile_y) in self.valid_moves:
        #     self.rect.topleft = (tile_x, tile_y)    # Instantly snap to the tile
        #     self.prev_tile = (tile_x, tile_y)   # Update previous tile

        # Reset direction
        self.direction = Vector2(0, 0)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # get the relative pos of the player from the mouse
        # to know on which axis the player will move
        delta_x = abs(self.rect.centerx - mouse_pos[0])
        delta_y = abs(self.rect.centery - mouse_pos[1])

        # Handle mouse input for movement
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_have_been_pressed = False
            return
        if self.mouse_have_been_pressed:
            return

        self.mouse_have_been_pressed = True

        # Move on the x-axis or y-axis
        if delta_x > delta_y:
            if delta_x >= (TILE_SIZE / 2):
                if mouse_pos[0] > self.rect.centerx:
                    self.direction.x = 1
                # if delta_x >= (TILE_SIZE / 2):
                #     self.direction.x = 1 if mouse_pos[0] > self.rect.centerx else -1
                else:
                    self.direction.x = -1
                    # if delta_y >= (TILE_SIZE / 2):
                    #     self.direction.y = 1 if mouse_pos[1] > self.rect.centery else -1
        else:
            if delta_y >= (TILE_SIZE / 2):
                if mouse_pos[1] > self.rect.centery:
                    self.direction.y = 1
                else:
                    self.direction.y = -1

        # Update position
        self.rect.x += self.direction.x * TILE_SIZE
        self.rect.y += self.direction.y * TILE_SIZE

        # return None

    def update(self, dt: float, grid=None) -> None:
        """Update the player's position and state."""
        if grid:
            self.get_adjacent_tiles(grid)   # Update valid moves
            self.input(grid)                # Handle input
        self.animate(dt)
