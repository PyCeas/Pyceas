import pygame

from src.inventory import Inventory

class ChestManager:
    def __init__(self, player, islands, inventory: Inventory):
        self.player = player
        self.islands = islands
        self.inventory = inventory

        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.Surface((500, 600), pygame.SRCALPHA)

    def update(self):
        pass

    def render(self):
        pass