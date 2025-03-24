import  pygame
from src.sprites.base import BaseSprite

class Tile(BaseSprite):
    """Handle tiles for the map"""

    def __init__(
        self,
        *groups: pygame.sprite.Group,
        pos: tuple[float, float],
        surf: pygame.Surface,
        name: str | None = None,
    ) -> None:
        r"""
        Initialize a Tile instance.

        Args:
            *groups (pygame.sprite.Group): One or more sprite groups that this tile will belong to.
            pos (Tuple[float, float]): The top-left position where the tile will be placed on the screen.
            surf (pygame.Surface): The surface (image) that will be drawn for this tile.
            name (Optional[str]): An optional name for the tile.

        Note:
            There is a known typing error related to missing type parameters for the generic type 'Group' in pygame.
            You may see warnings like:
            - src\\base.py:107: error: Missing type parameters for generic type 'Group' [type-arg]
            - src\\GUI\\game_manager.py:45: error: Missing type parameters for generic type 'SpriteGroup' [type-arg]

            These errors can be ignored for now, as they are related to type annotations in pygame's codebase.
        """
        super().__init__(*groups)

        self.pos = pos
        self.surf = surf
        self.name = name

        self.image: pygame.Surface = self.surf
        self.rect: pygame.FRect = self.image.get_frect(topleft=self.pos)

    def draw(self, display_surface: pygame.Surface, offset: tuple[float, float] = (0, 0)) -> None:
        """Could be useful for a camera?"""
        offset_rect = self.rect.move(offset)
        display_surface.blit(self.image, offset_rect)