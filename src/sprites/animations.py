import pygame  # type: ignore
from pygame.sprite import Group  # type: ignore

from src.settings import ANIMATION_SPEED, WORLD_LAYERS
from src.sprites.base import BaseSprite


class AnimatedSprites(BaseSprite):
    def __init__(
        self,
        pos: tuple[int, int],
        frames: list[pygame.Surface],
        groups: tuple[Group, ...],
        z: int = WORLD_LAYERS["main"],
    ):
        super().__init__(pos, frames[0], groups, z)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]  # Use the first frame

    def animate(self, dt: float) -> None:
        """Handle frame-based animation."""

        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt: float) -> None:
        self.animate(dt)
