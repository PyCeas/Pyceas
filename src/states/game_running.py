"""
Represents the GameRunning state, where the player controls a ship and interacts with the game world.
"""

import os
import json
import pygame
from pytmx.util_pygame import load_pygame  # type: ignore

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
      - Manages player inventory.
      - Updates game entities.
      - Renders the game world on the screen.
    """

    def __init__(self, game_state_manager) -> None:
        super().__init__(game_state_manager)

        # Initialize player inventory
        self.player_inventory = Inventory()
        self.load_inventory_from_json("data/inventory.json")

        self.all_sprites = src.sprites.AllSprites()

        # The start positions will be one of the 4 islands in the corners of the board
        self.setup(player_start_pos="top_left_island")

    def setup(self, player_start_pos):
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
        for obj in self.tmx_map["map"].get_layer_by_name("Ships"):
            if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
                self.player = src.sprites.Player((obj.x, obj.y), self.all_sprites)

    def load_inventory_from_json(self, file_path: str):
        """Load initial inventory items from JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item_name, properties in items.items():
                    quantity = properties.get("quantity", 1)  # Default to 1 if missing
                    self.player_inventory.add_item(item_name, quantity)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: The file at {file_path} does not exist.")

    def update(self, events) -> None:
        """
        update each sprites and handle events
        """

        self.all_sprites.update()

        # get events like keypress or mouse clicks
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:  # Toggle inventory with "I" key
                    self.game_state_manager.enter_state(
                        Paused(self.game_state_manager, self.player_inventory)
                    )

    def render(self, screen) -> None:
        """draw sprites to the canvas"""
        screen.fill("#000000")
        self.all_sprites.draw(
            self.player.rect.center,
            self.player.player_preview,
            self.player.player_preview_rect,
        )

        pygame.display.update()
