from typing import Dict, Tuple

import pygame

from src.states.base_state import BaseState
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Player_gui():
    def __init__(self, screen):
        self.font = pygame.font.Font(None, 36)
        self.screen = screen
        self.margin = 20
        self.wallet = {}

    def draw_gui(self, screen: pygame.Surface):
        for item, quantity in self.wallet:
            player_money = self.font.render(f"Gold: {quantity}", True, (255, 255, 255))

        text_wdith, text_height = player_money.get_size()
        x_pos = screen.get_width() - text_wdith - self.margin
        y_pos = self.margin
        self.screen.blit(player_money, (x_pos, y_pos))

        screen.blit(self.screen, dest=(0, 0))
        pygame.display.flip()  # Update the display