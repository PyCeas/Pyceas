import pygame
import pygame.locals
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

        self.screen = pygame.Surface((500, 400))  # Main UI surface
        
        self.sprite_sheet = pygame.image.load('images/tilesets/Treasure+.png').convert_alpha()
        self.icons = {
            "Wooden_chest": self.extract_icon(144, 0),
            "Silver_chest": self.extract_icon(160, 0),
            "Golden_chest": self.extract_icon(176, 0),
            "Mimic_chest": self.extract_icon(192, 0)
        }

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
        screen.blit(self.screen, (400, 125))
        pygame.display.flip()

