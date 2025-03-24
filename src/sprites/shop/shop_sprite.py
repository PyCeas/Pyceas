from pygame import Surface
from pygame.sprite import Group

from src.sprites.base import BaseSprite
from src.settings import WORLD_LAYERS


class ShowShop(BaseSprite):
    def __init__(
        self,
        pos: tuple[int, int],
        surface: Surface,
        groups: tuple[Group, ...],
        z=WORLD_LAYERS["main"],
    ):
        super().__init__(pos, surface, groups, z)

        self.image = Surface((32, 32))
        self.image.fill("white")
        # Compatibility check for get_frect
        if hasattr(self.image, "get_frect"):
            self.rect = self.image.get_frect(topleft=pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.z = z

    @staticmethod
    def extract_icon(sprite_sheet: Surface, x: int, y: int, size: int = 16) -> Surface:
        """
        Extract a single icon from a sprite sheet.

        Args:
            sprite_sheet (Surface): The loaded sprite sheet image.
            x (int): The x-coordinate of the top-left corner of the icon.
            y (int): The y-coordinate of the top-left corner of the icon.
            size (int): The width and height of the icon (square). Defaults to 16.

        Returns:
            Surface: A pygame.Surface object representing the extracted icon.
        """
        return sprite_sheet.subsurface((x, y, size, size))
