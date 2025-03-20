from typing import Dict, Tuple

import pygame

from src.states.base_state import BaseState
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player_gui():
    def __init__(self, screen):
        self.font = pygame.font.Font(None, 36)
        self.screen = screen

    # def update(self, events):
    #     for event in events:
    #         match event.type:
    #             case pygame.KEYDOWN:
    #                 if pygame.K_o:
    #                     self.game_state_manager.exit_state()

    def draw_gui(self, screen: pygame.Surface):
        player_money = self.font.render("Gold: N/A", True, (200, 200, 200))
        self.screen.blit(player_money, (50, screen.get_height() - 60))

        screen.blit(self.screen, dest=(0, 0))
        pygame.display.flip()  # Update the display