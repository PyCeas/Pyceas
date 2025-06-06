
from src.sprites.base import BaseSprite
from pygame import Surface
from pygame.sprite import Group, Sprite

from src.settings import WORLD_LAYERS

class IslandSprite(BaseSprite):
    def __init__(
        self, 
        pos: tuple[int, int], 
        surf: Surface, 
        groups: tuple[Group, ...], 
        z: object = WORLD_LAYERS["main"],
        island_name: str = "Unnamed",
        island_id: str = "Unknown"
        )-> None:
        super().__init__(pos, surf, groups, z=z)
        self.island_name = island_name
        self.island_id = island_id