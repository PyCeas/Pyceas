import pygame

from pygame import Surface
from src.inventory import Inventory

class ChestManager:
    def __init__(self, player, islands, inventory: Inventory):
        self.player = player
        self.islands = islands
        self.inventory = inventory

        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.Surface((500, 600), pygame.SRCALPHA)

    def update(self):
        self.collide = pygame.sprite.spritecollideany(self.player, self.islands)

        if self.collide:
            print("Collision")

    def render(self, screen: Surface):
        self.screen.fill((0, 0, 0, 0))

        if self.collide:
            self.message = self.font.render("TEST MESSAGE", True, (0, 0, 0))
            self.screen.blit(self.message, (155, 155))


        
        screen.blit(self.screen, (250, 250))