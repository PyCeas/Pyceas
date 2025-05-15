import os

import pygame

from src.states.base_state import BaseState
# from src.states.game_running import GameRunning
from src.inventory import Chest, Inventory

class ChestState(BaseState):
    def __init__(self, game_state_manager, player, inventory: Inventory, chest: Chest, island):
        super().__init__(game_state_manager)
        self.font = pygame.font.Font(None, 36)
        self.collide = False
        self.player = player
        self.island = island
        self.chest = chest
        self.inventory = inventory
        self.pressed = False

    def update(self, events):
        # Check collision
        if hasattr(self.player, "rect") and hasattr(self.island, "rect"):
            self.collide = pygame.sprite.spritecollideany(self.player, self.island)
        else:
            self.collide = False

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.inventory.add_chest(self.chest)
                        self.pressed = True
                        self.game_state_manager.exit_state()

    def render(self, screen: pygame.Surface):
        if self.collide:
            chest_add_message = self.font.render("Press E to pickup the chest", True, (0, 0, 0))
            screen.blit(chest_add_message, (50, screen.get_height() - 60))

        if self.pressed:
            confirm_message = self.font.render(f"Added {self.chest.name} to the inventory!", True, (0, 0, 0))
            screen.blit(confirm_message, (50, screen.get_height() - 60))
