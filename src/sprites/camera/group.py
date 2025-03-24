import pygame

from abc import ABC, abstractmethod

# class CameraGroup(pygame.sprite.Group, ABC):
class AllSprites(pygame.sprite.Group, ABC):
    # """A sprite group that handles every sprite and handles the camera logic"""
    """Abstract base class for camera logic and sprite rendering."""

    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        if not self.display_surface:
            raise ValueError("Display surface is not initialized")

        self.offset = pygame.math.Vector2()
        self.scale = 2.0

    @abstractmethod
    def draw(self, player_center) -> None:
        """Render sprites with camera adjustments."""
        pass