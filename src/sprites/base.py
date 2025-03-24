"""custom sprites classes"""

import pygame  # type: ignore
from pygame.sprite import Sprite, Group
from pygame import FRect, Surface, Vector2

from abc import ABC, abstractmethod

from src.settings import (
    WORLD_LAYERS,
    ANIMATION_SPEED
)


class BaseSprite(Sprite, ABC):
    """
    Abstract base class for all custom sprites in the game, combining the functionality
    of both Sprite and Entity classes. Provides support for rendering, animation,
    and basic movement logic.

    Attributes:
        rect (FRect): The rectangle representing the sprite's position and size.
        frames (list[Surface]): A list of animation frames for the sprite.
        frame_index (float): The current frame index for animations.
        direction (Vector2): The current movement direction of the sprite.
        facing_direction (str): The current facing direction (e.g., "up", "down").
    """

    rect = FRect

    def __init__(
        self,
            pos: tuple[int, int],
            surf: Surface,
            groups: tuple[Group, ...],
            z: object = WORLD_LAYERS["main"],
            frames: list[Surface] = None,
    ) -> None:
        """
       Initialize the base sprite.
       :param pos: The (x, y) position of the sprite.
       :param surf: The surface (image) of the sprite.
       :param groups: Groups the sprite belongs to.
       :param z: The layer index for rendering.
       :param frames: The frame index for rendering.
       """

        super().__init__(groups)

        if surf is None:
            raise ValueError("The `surf` parameter must be a valid pygame.Surface.")

        self.image = surf
        self.rect: FRect = self.image.get_frect(topleft=pos)
        self.z = z

        self.frames = frames or[surf]
        self.frame_index: float = 0.0

        # Movement
        self.direction = Vector2()
        self.facing_direction: str = "down"

    def animate(self, dt: float) -> None:
        """Handle animation logic."""
        if len(self.frames) > 1:  # Only animate if there's more than one frame
            self.frame_index += ANIMATION_SPEED * dt
            # self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def get_state(self) -> str:
        """Determine the current state of the sprite."""
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = "right" if self.direction.x > 0 else "left"
            if self.direction.y != 0:
                self.facing_direction = "down" if self.direction.y > 0 else "up"
        return f"{self.facing_direction}{'' if moving else '_idle'}"
