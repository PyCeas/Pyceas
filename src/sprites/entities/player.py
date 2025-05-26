import pygame
from pygame import Surface, Vector2
from pygame.sprite import Group

from src.inventory import Inventory
from src.settings import TILE_SIZE
from src.sprites.base import BaseSprite


class Player(BaseSprite):
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

        # Ghost preview
        self.player_preview = first_frame.copy()
        self.player_preview.set_alpha(128)

        # Inventory system
        self.inventory = Inventory()

        # Input handling
        self.mouse_have_been_pressed: bool = False

        # Hp points
        self.player_hp = 100

    def input(self) -> None:
        """move the player and show a ghost to preview the move"""

        # Reset direction
        self.direction = Vector2(0, 0)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # get the relative pos of the player from the mouse
        # to know on which axis the player will move
        delta_x = abs(self.rect.centerx - mouse_pos[0])
        delta_y = abs(self.rect.centery - mouse_pos[1])

        # #  move the ghost on the x-axis
        # self.player_preview_rect = self.rect.copy()
        # if delta_x > delta_y:
        #     if delta_x < (TILE_SIZE / 2):
        #         # don't move the ghost if the mouse is on the player hit box
        #         self.player_preview_rect.x = self.rect.x
        #     elif mouse_pos[0] > self.rect.centerx:
        #         # go right
        #         self.player_preview_rect.x = self.rect.x + TILE_SIZE
        #     else:
        #         # go left
        #         self.player_preview_rect.x = self.rect.x - TILE_SIZE
        # # move the ghost on the y-axis
        # else:
        #     if delta_y < (TILE_SIZE / 2):
        #         # don't move if the mouse is on the player hit box
        #         self.player_preview_rect.y = self.rect.y
        #     elif mouse_pos[1] > self.rect.centery:
        #         # go down
        #         self.player_preview_rect.y = self.rect.y + TILE_SIZE
        #     else:
        #         # go up
        #         self.player_preview_rect.y = self.rect.y - TILE_SIZE

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

    def update(self, dt: float) -> None:
        """Update the player's position and state."""
        self.input()
        self.animate(dt)
