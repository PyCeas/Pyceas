import pygame
import random
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
        self.chest_collected = False
        self.message = ""
        self.message_end_time = 0

        self.screen = pygame.Surface((500, 400))  # Main UI surface

        self.sprite_sheet = pygame.image.load("images/tilesets/Treasure+.png").convert_alpha()
        self.icons = {
            "Wooden chest": self.extract_icon(0, 144),
            "Golden chest": self.extract_icon(0, 160),
            "Silver chest": self.extract_icon(0, 176),
            "Mimic chest": self.extract_icon(0, 192),
            "Voyage scroll": self.extract_icon(176, 176),
        }

        chest_name, chest_icon = random.choice(list(self.icons.items()))
        self.chest_name = chest_name
        self.chest_icon = chest_icon

    def extract_icon(self, x, y, size=16):
        return self.sprite_sheet.subsurface((x, y, size, size))

    def update(self, events):
        # Collision check
        self.collide = pygame.sprite.spritecollideany(self.player, self.island)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.pressed = False
                    self.game_state_manager.exit_state()

                elif event.key == pygame.K_e and self.collide:
                    if not self.pressed and not self.collide.chest_collected:
                        self.pressed = True
                        self.collide.chest_collected = True
                        self.message = self.inventory.add_item(self.chest_name, 1)
                        self.message_end_time = pygame.time.get_ticks() + 2000  # Show for 2s
                    elif not self.pressed and self.collide.chest_collected:
                        self.collected_message = "There are no chest nor voyage's here anymore!"
                        self.collected_message_end_time = pygame.time.get_ticks() + 2000

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0))  # Clear UI surface

        y_offset = 150

        # Only draw the chest icon if it hasn't been collected
        if self.collide and not getattr(self.collide, "chest_collected", False):
            scaled_icon = pygame.transform.scale(self.chest_icon, (64, 64))
            if self.chest_icon:
                self.screen.blit(scaled_icon, (215, y_offset))

        # Show prompt if player is colliding with the island
        if self.collide:
            if getattr(self.collide, "chest_collected", False):
                prompt_text = self.font.render("No chest or voyage available here.", True, (200, 100, 100))
            else:
                prompt_text = self.font.render("Press 'E' to pick up the chest!", True, (255, 255, 255))

            self.screen.blit(prompt_text, (50, self.screen.get_height() - 100))

        # Show message if a chest was just picked up
        if self.pressed and self.message and pygame.time.get_ticks() < self.message_end_time:
            message_text = self.font.render(self.message, True, (255, 255, 0))
            text_width, text_height = message_text.get_size()

            bg_x = 40
            bg_y = self.screen.get_height() - 60
            pygame.draw.rect(self.screen, (0, 0, 0), (bg_x, bg_y, text_width + 20, text_height + 10))
            self.screen.blit(message_text, (bg_x + 10, bg_y + 5))

        # Optionally: show the "no chest" message as a timed message too
        if hasattr(self, "collected_message") and pygame.time.get_ticks() < self.collected_message_end_time:
            no_chest_text = self.font.render(self.collected_message, True, (180, 0, 0))
            self.screen.blit(no_chest_text, (50, self.screen.get_height() - 70))

        # Blit the ChestState UI surface onto the main screen
        screen.blit(self.screen, (400, 125))
        pygame.display.flip()
