import pygame

from src.settings import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, ANIMATION_SPEED, WORLD_LAYERS

class ShowShop(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = WORLD_LAYERS["main"]):
        super().__init__(groups)

        self.image  = pygame.Surface((32, 32))
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
# class