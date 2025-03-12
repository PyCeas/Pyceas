"""
Represents the GameRunning state, where the player controls a ship and interacts with the game world.
"""

import os
import json
import pygame
from pytmx.util_pygame import load_pygame  # type: ignore

import src.shop
from src.states.base_state import BaseState
from src.states.paused import Paused
from src.inventory import Inventory
from src.support import import_folder, coast_importer, all_character_import
from src.sprites import AnimatedSprites

from src.settings import TILE_SIZE, WORLD_LAYERS
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
        self.clock = pygame.Clock()
        self.player_inventory = Inventory()
        self.load_inventory_from_json("data/inventory.json")

        self.all_sprites = src.sprites.AllSprites()

        # The start positions will be one of the 4 islands in the corners of the board
        self.setup(player_start_pos="top_left_island")

        self.font = pygame.font.Font(None, 36)

    def setup(self, player_start_pos):
        """
        setup the map and player from the tiled file
        """
        self.tmx_map = {
            "map": load_pygame(os.path.join(".", "data", "new_maps", "100x100_map.tmx"))
        }

        self.world_frames = {
            "water": import_folder(".", "images", "tilesets", "temporary_water"),
            "coast": coast_importer(6, 6, ".", "images", "tilesets", "coast"),
            "ships": all_character_import(".", "images", "tilesets", "ships")
        }

        # Sea
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Sea").tiles():
            src.sprites.Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, WORLD_LAYERS["bg"])

        # Water animated
        for obj in self.tmx_map["map"].get_layer_by_name("Water"):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprites((x, y), self.world_frames["water"], self.all_sprites, WORLD_LAYERS["water"])

        # Shallow water
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Shallow Sea").tiles():
            src.sprites.Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, WORLD_LAYERS["bg"])

        # buildings
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Shop").tiles():
            self.shop = src.shop.ShowShop((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, WORLD_LAYERS["main"])
            print(x, y)

        # Islands
        islands = self.tmx_map["map"].get_layer_by_name("Islands")
        for x, y, surface in islands.tiles():
            src.sprites.Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, WORLD_LAYERS["bg"])

        # Enitites
        for obj in self.tmx_map["map"].get_layer_by_name("Ships"):
            if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
                self.player = src.sprites.Player(
                    pos = (obj.x, obj.y), 
                    frames = self.world_frames["ships"]["player_test_ship"], 
                    groups = self.all_sprites)

        # Coast
        for obj in self.tmx_map["map"].get_layer_by_name("Coast"):
            terrain = obj.properties["terrain"]
            side = obj.properties["side"]
            AnimatedSprites((obj.x, obj.y), self.world_frames["coast"][terrain][side], self.all_sprites, WORLD_LAYERS["bg"])

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
        dt = self.clock.tick() / 1000
        self.all_sprites.update(dt)

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
            self.player.rect.center
        )

        self.welcome_message = self.font.render("Press 'E' to interact!", True, (100, 100, 100))
        point = self.shop.rect
        collide = self.player.rect.colliderect(point)
        if collide:
            # print("Welcome to the shop!")
            screen.blit(self.welcome_message, (155, 155))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                print("Sick boots x 5")

        pygame.display.update()
