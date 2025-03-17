import pygame

from src.settings import WORLD_LAYERS
from src.states.base_state import BaseState
from src.inventory import Inventory
from typing import Tuple, Dict

class ShowShop(pygame.sprite.Sprite, BaseState):
    def __init__(self, pos, surface, groups, z = WORLD_LAYERS["main"]):
        super().__init__(groups)

        self.image  = pygame.Surface((32, 32))
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.Surface((800, 600))

        self.button_width = 100
        self.button_height = 50

        self.button_actions: Dict[str, Tuple[pygame.Rect, pygame.Rect]] = {}
        self.inventory = Inventory()

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def render(self, screen):
        return super().render(screen)
    
    def handle_mouse_clicks(self, mouse_pos):
        for item, (use_button, discard_button) in self.button_actions.items():
            if use_button.collidepoint(mouse_pos):
                self.message = self.inventory.use_item(item)  # `self.message` stores strings
                self.message_end_time = pygame.time.get_ticks() + 3000  # 3 seconds
            elif discard_button.collidepoint(mouse_pos):
                self.message = self.inventory.remove_item(item, 1)
                self.message_end_time = pygame.time.get_ticks() + 4000  # 4 seconds
    
    def draw_buttons(self, x: int, y: int, item: str) -> Tuple[pygame.Rect, pygame.Rect]:
        use_button = pygame.Rect(x, y, self.button_width, self.button_height)
        discard_button = pygame.Rect(x + self.button_width + 10, y, self.button_width, self.button_height)

        pygame.draw.rect(self.screen, (0, 255, 0), use_button)  # Green
        pygame.draw.rect(self.screen, (150, 75, 0), discard_button)  # Brown

        use_text = self.font.render("Use", True, (0, 0, 0))  # Black
        discard_text = self.font.render("Discard", True, (0, 0, 0))

        self.screen.blit(use_text, (x + 10, y + 10))
        self.screen.blit(discard_text, (x + self.button_width + 20, y + 10))

        return use_button, discard_button
