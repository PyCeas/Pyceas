# import os

# import pygame

# from src.states.base_state import BaseState
# # from src.states.game_running import GameRunning
# from src.inventory import Chest, Inventory

# class ChestState(BaseState):
#     def __init__(self, game_state_manager, player, inventory: Inventory, chest: Chest, island):
#         super().__init__(game_state_manager)
#         self.font = pygame.font.Font(None, 36)
#         self.collide = False
#         self.player = player
#         self.island = island
#         self.chest = chest
#         self.inventory = inventory
#         self.pressed = False
#         self.main_screen = pygame.Surface((1280, 720))
#         self.screen = pygame.Surface((240, 320))

#     def update(self, events):
#         # Check collision
#         if hasattr(self.player, "rect") and hasattr(self.island, "rect"):
#             self.collide = pygame.sprite.spritecollideany(self.player, self.island)
#         else:
#             self.collide = False

#         for event in events:
#             match event.type:
#                 case pygame.KEYDOWN:
#                     if event.key == pygame.K_q:
#                         self.pressed = False
#                         self.game_state_manager.exit_state()

#     def render(self, screen: pygame.Surface):
#         if self.collide:
#             chest_add_message = self.font.render("Press E to pickup the chest!", True, (255, 255, 255))
#             self.main_screen.blit(chest_add_message, (50, screen.get_height() - 60))

#         if self.pressed:
#             confirm_message = self.font.render(f"Added {self.chest.name} to the inventory!", True, (255, 255, 255))
#             self.screen.blit(confirm_message, (50, screen.get_height() - 60))

#         screen.blit(self.screen, dest=(250, 250))
#         pygame.display.flip()

import pygame
from src.states.base_state import BaseState
from src.inventory import Chest, Inventory


class ChestState(BaseState):
    def __init__(self, game_state_manager, player, inventory: Inventory, chest: Chest, island):
        super().__init__(game_state_manager)
        self.font = pygame.font.Font(None, 36)

        self.player = player
        self.island = island
        self.chest = chest
        self.inventory = inventory

        self.collide = False
        self.pressed = False
        self.message = ""
        self.message_end_time = 0

        self.screen = pygame.Surface((1280, 720))  # Main UI surface

    def update(self, events):
        # Collision check
        self.collide = pygame.sprite.spritecollideany(self.player, self.island)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.pressed = False
                    self.game_state_manager.exit_state()

                elif event.key == pygame.K_e and self.collide:
                    if not self.pressed:
                        self.pressed = True
                        self.inventory.add_item(self.chest.name, 1)
                        self.message = f"Added {self.chest.name} to inventory!"
                        self.message_end_time = pygame.time.get_ticks() + 2000  # Show for 2s

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0))  # Clear UI surface

        if self.collide:
            prompt_text = self.font.render("Press 'E' to pick up the chest!", True, (255, 255, 255))
            self.screen.blit(prompt_text, (50, self.screen.get_height() - 100))

        if self.pressed and self.message and pygame.time.get_ticks() < self.message_end_time:
            message_text = self.font.render(self.message, True, (255, 255, 0))
            text_width, text_height = message_text.get_size()

            bg_x = 40
            bg_y = self.screen.get_height() - 60
            pygame.draw.rect(self.screen, (0, 0, 0), (bg_x, bg_y, text_width + 20, text_height + 10))
            self.screen.blit(message_text, (bg_x + 10, bg_y + 5))

        # Blit the ChestState UI surface onto the main screen
        screen.blit(self.screen, (0, 0))
        pygame.display.flip()

