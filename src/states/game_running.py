"""
Represents the GameRunning state, where the player controls a ship and interacts with the game world.
"""

import json
import os

import pygame  # type: ignore
from pytmx.util_pygame import load_pygame  # type: ignore

from src.inventory import Inventory
from src.settings import TILE_SIZE, WORLD_LAYERS
from src.sprites.animations import AnimatedSprites
from src.sprites.base import BaseSprite
from src.sprites.camera.player import PlayerCamera
from src.sprites.entities.player import Player
from src.sprites.tiles.grid_manager import GridManager
from src.states.base_state import BaseState
from src.states.paused import Paused
from src.states.shop_state import ShowShop, WindowShop
from src.support import all_character_import, coast_importer, import_folder


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

        # Camera group
        self.all_sprites = PlayerCamera()

        # Render the grid
        self.grid_manager = GridManager(self.all_sprites.display_surface, TILE_SIZE)
        self.show_grid: bool = True

        # The start positions will be one of the 4 islands in the corners of the board
        self.setup(player_start_pos="top_left_island")

        self.font = pygame.font.Font(None, 36)
        self.shop_window = pygame.Surface((800, 600))
        self.in_shop = False

    def setup(self, player_start_pos: str) -> None:
        """
        set up the map and player from the tiled file
        """
        self.tmx_map = {"map": load_pygame(os.path.join(".", "data", "new_maps", "100x100_map.tmx"))}

        self.world_frames = {
            "water": import_folder(".", "images", "tilesets", "temporary_water"),
            "coast": coast_importer(6, 6, ".", "images", "tilesets", "coast"),
            "ships": all_character_import(".", "images", "tilesets", "ships"),
        }

        # Initialize self.player to None by default
        # self.player = None

        # Sea
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Sea").tiles():
            BaseSprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
                groups=(self.all_sprites,),
                z=WORLD_LAYERS["bg"],
            )

        # Water animated
        for obj in self.tmx_map["map"].get_layer_by_name("Water"):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprites(
                        pos=(x, y),
                        frames=self.world_frames["water"],
                        groups=(self.all_sprites,),
                        z=WORLD_LAYERS["water"],
                    )

        # Shallow water
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Shallow Sea").tiles():
            BaseSprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surface, groups=(self.all_sprites,), z=WORLD_LAYERS["bg"]
            )

        # Buildings
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Shop").tiles():
            self.shop = ShowShop(
                pos=(x * TILE_SIZE, y * TILE_SIZE), surface=surface, groups=(self.all_sprites,), z=WORLD_LAYERS["main"]
            )

        # Islands
        islands = self.tmx_map["map"].get_layer_by_name("Islands")
        for x, y, surface in islands.tiles():
            BaseSprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
                groups=(self.all_sprites,),
                z=WORLD_LAYERS["bg"],
            )

            # Enitites
            for obj in self.tmx_map["map"].get_layer_by_name("Ships"):
                if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
                    print(f"Creating Player at ({obj.x}, {obj.y})")  # Debugging
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.world_frames["ships"]["player_test_ship"],
                        groups=(self.all_sprites,),
                    )
                    break  # Stops after the first match

        # Coast
        for obj in self.tmx_map["map"].get_layer_by_name("Coast"):
            terrain = obj.properties["terrain"]
            side = obj.properties["side"]
            AnimatedSprites(
                pos=(obj.x, obj.y),
                frames=self.world_frames["coast"][terrain][side],
                groups=(self.all_sprites,),
                z=WORLD_LAYERS["bg"],
            )

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

        collide = self.player.rect.colliderect(self.shop.rect) if self.player else False
        dt = self.clock.tick() / 1000
        self.all_sprites.update(dt)

        # Handle player movement and grid snapping
        if self.player:
            self.player.update(dt, grid=self.grid_manager)

        # get events like keypress or mouse clicks
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:  # Toggle inventory with "I" key
                    self.game_state_manager.enter_state(Paused(self.game_state_manager, self.player_inventory))
                elif collide and event.key == pygame.K_e:
                    self.game_state_manager.enter_state(
                        WindowShop(self.game_state_manager, self.player, self.shop, self.player_inventory)
                    )
                elif event.key == pygame.K_g:  # Toggle grid with "G" key
                    self.show_grid = not self.show_grid

    def render(self, screen) -> None:
        """draw sprites to the canvas"""
        screen.fill("#000000")
        self.all_sprites.draw(
            self.player.rect.center,
            show_grid=self.show_grid
        )

        pygame.display.update()
