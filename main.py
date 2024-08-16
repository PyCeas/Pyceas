"""Project Name: PySeas
Description: PySeas is an open-source project to create an engaging board game in Python,
inspired by Sea of Thieves. Ideal for game development enthusiasts and Python programmers
Author(s): Danilo Saiu (https://www.github.com/ultimateownsz),
Davit Alsemgeest (https://www.github.com/davidek523)
Date: 2024-09-08

Python Version: 1.0.0
Pygame Version: 0.0.1"""

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
from os.path import join
import sys

# import dataclasses and typchecking
from dataclasses import dataclass, field
from typing import List

# import pygame related
import pygame
from pytmx.util_pygame import load_pygame

# import Python specific objects, functions and functionality
from src.CLI.board import Board
from src.CLI.player import Player

# import Pygame specific objects, functions and functionality
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
import src.sprites


@dataclass
class CLI:
    """ Command Line Interface, only using print statements """

    players: List[Player] = field(init=False)
    board: Board = field(init=False)
    current_player_index: int = 0
    running: bool = False

    def __post_init__(self):
        self.clear_screen()
        self.players = [
            Player(name_of_player="player 1", player_id=0),
            Player(name_of_player="player 2", player_id=1),
        ]
        self.board = Board(self.players)

    # logic which players turn it is
    def toggle_player_index(self):
        if self.current_player_index == 0:
            self.current_player_index = 1
        else:
            self.current_player_index = 0

    @staticmethod
    def clear_screen():
        """A function made to clear the screen in the Python boardgame.
        Could be used or altered in Pygame if needed."""

        os.system("cls" if os.name == "nt" else "clear")

    def run(self):
        self.initialize_game()
        self.running = True
        while self.running:
            start_the_game = input(
                "Would you like to start the game? Press enter to continue. "
            )
            if start_the_game == "":
                self.clear_screen()
                break
        self.board.print()
        self.player_switch(self.players)

    def player_switch(self, players):
        """This decides what the current player pos is and then switch to the other player, when the player gets asked to end the turn"""

        while True:
            current_player = players[self.current_player_index]
            print(
                f"\nIt's {current_player.name_of_player.capitalize()}'s turn! Current position is {self.board.players[self.current_player_index]}"
            )

            # end_turn = False

            while True:
                roll_dice = input("\nDo you want to roll the dice? (yes/y) \n")
                if roll_dice.lower() in ["yes", "y"]:
                    # current_player.dice_roll()
                    current_player.move_player(self.board)
                    if current_player:
                        current_player.perform_action(
                            self.board,
                            new_position=self.board.players[self.current_player_index],
                        )
                    break
                else:
                    print(
                        "You made a mistake, you can only answer yes to roll the dice!"
                    )
                    continue

            stop_turn = input("\nDo you want to end your turn? (yes/no) \n")
            if stop_turn.lower() in ["yes", "y"]:
                self.toggle_player_index()
                Board(players).print()
            elif stop_turn.lower() in ["no", "n"]:
                print("\nYou must continue your turn.")
                self.toggle_player_index()
                Board(players).print()
            else:
                print("Input error. Please answer yes or no.")

    def initialize_game(self):
        print("Ahoy Mateyy To PySeas!\n")

        for player in self.players:
            while True:
                name = input(f"Enter player {player.player_id+1} name: ").strip()
                if 2 <= len(name) <= 10 and name.isalpha():
                    player.name_of_player = name
                    break
                else:
                    print(
                        "Input error. Player name should be between two characters and maximum ten characters containing only alphabets."
                    )
                    continue

        # print(f"\nAhoy {self.players[0].name_of_player.capitalize()} & {self.players[1].name_of_player.capitalize()} to the start of the game!\n")
        for player in self.players:
            player.print_info()
        return self.players


@dataclass
class GUI:
    """ Graphial User Interface vertion of the game, using pygame-ce """

    screen_size: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen: pygame.Surface = field(init=False)

    # groups
    # all_sprites: pygame.sprite.Group = field(
    #     init=False, default_factory=pygame.sprite.Group
    # )
    all_sprites: pygame.sprite.Group = pygame.sprite.Group()

    def __post_init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("PySeas")

        self.players: list[src.sprites.Player] = [src.sprites.Player()]

        self.running = True
        self.import_assets()
        self.setup(
            tmx_maps=self.tmx_map["map"], player_start_pos="Fort"
        )  # The start positions will be one of the 4 islands in the corners of the board

    def import_assets(self):
        """ load the map """
        # The map was made as a basic start for the game, it can be changes or altered if it is better for the overall flow of the game
        self.tmx_map = {
            "map": load_pygame(join(".", "data", "maps", "100x100_map.tmx"))
        }

        # # Define the path to the TMX file
        # tmx_path = os.path.join('data', 'maps', '100x100_map.tmx')
        # sprite_group = pygame.sprite.Group()

        # # Check if the file exists
        # if not os.path.exists(self.tmx_maps):
        #     print(f"Error: The file at {self.tmx_maps} does not exist.")
        #     return None

        # # Load the TMX file using load_pygame
        # tmx_data = load_pygame(tmx_path)
        # print(tmx_data.layers)

    def setup(self, tmx_maps, player_start_pos):
        """ create tiles """
        islands = tmx_maps.get_layer_by_name("Islands")
        for x, y, surface in islands.tiles():
            # print(x * TILE_SIZE, y * TILE_SIZE, surface)
            src.sprites.Tile(
                self.all_sprites,
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
            )

    def run(self) -> None:
        """ main loop of the game """
        while self.running:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self) -> None:
        """ get events like keypress or mouse clicks """
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def update(self) -> None:
        """ update the player """
        for player in self.players:
            player.update()

    def render(self) -> None:
        """ draw sprites to the canvas """
        self.screen.fill('#000000')
        self.all_sprites.draw(surface=self.screen)

        # draw players on top of the other sprites
        for player in self.players:
            player.render(surface=self.screen)

        pygame.display.update()


if __name__ == "__main__":
    # vertion choise is disabled for debugging reasons
    game = GUI()
    game.run()

    # print(
    #     """
    #       Welcome to Pyseas!
    #       Please select a version to play:
    #       1. CLI version
    #       2. GUI version"""
    # )
    # choice: str = input("Enter the number of your choice: ")
    # while choice not in ['1', '2']:
    #     choice = input("Enter the number of your choice: ")

    # if choice == "1":
    #     CLI().run()
    # elif choice == "2":
    #     GUI().run()
