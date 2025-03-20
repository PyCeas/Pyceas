from typing import Dict, Tuple

import pygame

from src.states.base_state import BaseState

class Player_gui(BaseState):
    def __init__(self, game_state_manager):
        super().__init__(game_state_manager)
        