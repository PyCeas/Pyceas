import pygame

from src.states.base_state import BaseState

class ObstacleSate(BaseState):
    def __init__(self, game_state_manager):
        super().__init__(game_state_manager)

    def render(self):
        pass

    def update(self, events):
        pass