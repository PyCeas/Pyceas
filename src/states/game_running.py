"""
Represents the GameRunning state, where the player controls a ship and interacts with the game world.
"""

import os
import json
import pygame
from pytmx.util_pygame import load_pygame  # type: ignore
from typing import List
import random

from src.states.base_state import BaseState
from src.states.paused import Paused
from src.inventory import Inventory

from src.settings import TILE_SIZE
import src.sprites


class GameRunning(BaseState):
    """
    Represents the GameRunning state, where the player controls a ship and interacts with the game world.

    Responsibilities:
      - Loads the game map and player starting position.
      - Manages player inventories.
      - Updates game entities.
      - Renders the game world on the screen.
      - Handles player switching.
    """

    def __init__(self, game_state_manager) -> None:
        super().__init__(game_state_manager)

        self.players = []
        self.current_player_index = 0
        self.all_sprites = src.sprites.AllSprites()

        # store dice rolls and turn order
        self.dice_rolls = None
        self.turn_order = None
        
        # Initialize player inventory
        self.player_inventory = Inventory()
        self.load_inventory_from_json("data/inventory.json")


        # The start positions will be one of the 4 islands in the corners of the board
        self.setup(player_start_positions=["top_left_island", "bottom_right_island"])

        # Roll dice to determine turn order
        self.roll_dice(self.game_state_manager.screen)

    def setup(self, player_start_positions: List[str]) -> None:
        """
        setup the map and player from the tiled file
        """
        self.tmx_map = {
            "map": load_pygame(os.path.join(".", "data", "maps", "100x100_map.tmx"))
        }

        # Islands
        islands = self.tmx_map["map"].get_layer_by_name("Islands")
        for x, y, surface in islands.tiles():
            src.sprites.Tile(
                self.all_sprites,
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
            )

        # Objects
        ships_layer = self.tmx_map["map"].get_layer_by_name("Ships")
        for idx, obj in enumerate(ships_layer):
            print(f"Object name: {obj.name}, Properties: {obj.properties}")
            for starting_position in player_start_positions:
                if obj.name == "Player" and obj.properties["pos"] == starting_position:
                    player_name = f"Player {idx + 1}"  # Player 1, Player 2, etc.
                    player = src.sprites.Player(name=obj.name, pos=(obj.x, obj.y), groups=self.all_sprites)
                    self.players.append(player)
        
        if not self.players:
            raise ValueError("No player starting positions found in the map.")
        
        if len(self.players) < 2: # for now, we require at least two players
            raise ValueError("At least two player starting positions are required.")

    def load_inventory_from_json(self, file_path: str):
        """Load initial inventory items from JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item_name, properties in items.items():
                    quantity = properties.get("quantity", 1)  # Default to 1 if missing
                    for player in self.players:
                        player.player_inventory.add_item(item_name, quantity)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: The file at {file_path} does not exist.")

    def roll_dice(self, screen) -> None:
        """Roll dice for each player and determine turn order."""
        self.dice_rolls = {player.name: random.randint(1, 6) for player in self.players}

        # sort players by their dice rolls (highest roll goes first)
        sorted_players = sorted(
            self.dice_rolls.items(), key=lambda player: player[1], reverse=True
        )

        # display the dice rolls using placeholders
        self.display_dice(screen, self.dice_rolls)

        font = pygame.font.Font(None, 48)
        screen.fill((0, 0, 0))  # Clear the screen

        # show the player who goes first
        starting_player = font.render(
            f"{sorted_players[0][0]} goes first!", True, (255, 255, 255)
        )
        screen.blit(starting_player, (10, 300))

        pygame.display.update()

        # return sorterd players for turn order
        return [p[0] for p in sorted_players]
    
    def display_dice(self, screen, dice_rolls):
        """Display rectangles as placeholders for dice results."""
        font = pygame.font.Font(None, 48)

        x_offset = 100
        y_offset = 100

        for idx, (player_name, roll) in enumerate(dice_rolls.items()):
            # draw rectancle placeholder
            pygame.draw.rect(screen, (255, 0, 0), (x_offset, y_offset, 100, 100))

            # display the dice roll inside the rectangle
            text = font.render(str(roll), True, (255, 255, 255))
            screen.blit(text, (x_offset + 30, y_offset + 30))

            # display the player's name below the rectangle
            name_text = font.render(player_name, True, (255, 255, 255))
            screen.blit(name_text, (x_offset, y_offset + 120))

            x_offset += 150 # shift to the right for the next player

        pygame.display.update()

    def display_turn_indicator(self, screen: pygame.Surface) -> None:
        """Display the current player's turn indicator."""
        font = pygame.font.Font(None, 36)
        current_player_name = self.players[self.current_player_index].name
        text = font.render(f"{current_player_name}'s turn", True, (255, 255, 255))
        screen.blit(text, (10, 10)) # position the text at the top-left corner

    def switch_player(self):
        """
        switch to the next player
        """
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.dice_rolls = None  # reset dice rolls when switching players
    
    def update(self, events) -> None:
        """
        update each sprites and handle events
        """

        self.active_player = self.players[self.current_player_index]

        self.all_sprites.update()

        # get events like keypress or mouse clicks
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:  # Toggle inventory with "I" key
                    self.game_state_manager.enter_state(
                        Paused(self.game_state_manager, self.player_inventory)
                    )
                elif event.key == pygame.K_SPACE:  # trigger dice roll with space key
                    turn_order = self.roll_dice(self.game_state_manager.screen)
                    # self.players = [player for player in self.players if player.name in turn_order]
                elif event.key == pygame.K_RETURN:  # switch player with enter key
                    self.switch_player()

    def render(self, screen) -> None:
        """draw sprites to the canvas"""
        screen.fill("#000000")
        self.all_sprites.draw(
            self.active_player.rect.center,
            self.active_player.player_preview,
            self.active_player.player_preview_rect,
        )
        self.display_turn_indicator(screen) # display turn indicator

        # display the dice rolls using placeholders
        if self.dice_rolls:
            self.display_dice(screen, self.dice_rolls)

        pygame.display.update()
