import os

import pygame
from pygame import Surface

from src.inventory import Inventory
from src.sprites.shops.shop_sprite import ShowShop
from src.states.base_state import BaseState

class HarbourState(BaseState):
    def __init__(self, game_state_manager, player, show_shop: ShowShop, inventory: Inventory):
        super().__init__(game_state_manager)
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.Surface((800, 600))

    def update(self, events):
        pass
    
    def render(self, screen: pygame.Surface):
        pass