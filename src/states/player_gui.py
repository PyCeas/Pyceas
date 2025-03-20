from typing import Dict, Tuple

import pygame

from src.states.base_state import BaseState
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player_gui(BaseState):
    def __init__(self, game_state_manager):
        super().__init__(game_state_manager)
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def udpate(self, events):
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if pygame.K_o:
                        self.game_state_manager.exit_state()

    def render(self, screen: pygame.Surface):
        player_money = self.font.render("Gold: N/A", True, (200, 200, 200))
        screen.blit(player_money, (50, self.screen.get_height() - 60))