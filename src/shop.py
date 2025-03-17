import pygame

from src.settings import WORLD_LAYERS
from src.states.base_state import BaseState

class ShowShop(pygame.sprite.Sprite, BaseState):
    def __init__(self, pos, surface, groups, z = WORLD_LAYERS["main"]):
        super().__init__(groups)

        self.image  = pygame.Surface((32, 32))
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def render(self, screen):
        return super().render(screen)
