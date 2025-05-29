"""
main game loop
structure of the game, using a stack of states
"""

import sys
import pygame

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# import basestate for typehint
from src.states.base_state import BaseState
from src.states.game_running import GameRunning


class GameStateManager:
    """
    Manages the main game loop and the structure of the game using a stack of states.

    This class is responsible for:
    - Initializing Pygame and setting up the main screen.
    - Managing a stack of game states, allowing for seamless transitions (e.g., from gameplay to paused state).
    - Handling Pygame events and delegating them to the active state.
    - Running the main game loop with controlled frame rate.
    """

    def __init__(self) -> None:
        # init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PyCeas")

        self.clock = pygame.Clock()
        self.running = True
        self.events: list[pygame.event.Event] = []
        self.states_stack: list[BaseState] = []

        # instanciate the initial state
        self.states_stack.append(GameRunning(self))

    def __str__(self) -> str:
        """
        return a string representing the stack
        e.g. : >MainMenu>GameRunning>Paused
        """
        stack_repr: str = ""
        for state in self.states_stack:
            stack_repr += ">" + str(state)
        return stack_repr

    def enter_state(self, state: BaseState) -> None:
        """
        append state to the stack
        """
        self.states_stack.append(state)

    def exit_state(self) -> BaseState:
        """
        pop and return the last state
        """
        if len(self.states_stack) == 0:
            raise ValueError("the stack is empty")
        return self.states_stack.pop()

    def _handle_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def run(self) -> None:
        """main loop of the game"""
        while self.running:
            self._handle_events()

            # give the pygame events to each states
            # to ensure that pygame.event.get() is only called once per frame
            self.states_stack[-1].update(self.events)

            self.states_stack[-1].render(self.screen)

            # magic value, use a FPS const in settings or delta time
            self.clock.tick(FPS)
