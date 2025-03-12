"""
Represents a base example state in the game.
Each state must implement:
- `update`: A method that loops through and handles events.
- `render`: A method responsible for drawing the state on the given surface.
"""

from abc import ABC, abstractmethod

import pygame


class BaseState(ABC):
    """
    using an abstract class to ensure each state has the right methods
    """

    def __init__(self, game_state_manager) -> None:
        self.game_state_manager = game_state_manager

    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def update(self, events):  # return self
        """
        update current state
        handle events
        and return current state or another one
        """

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """
        render current state on a given surface
        """
