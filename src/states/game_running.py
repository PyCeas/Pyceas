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

        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()

        # Render the grid
        self.grid_manager = None  # Initialize grid_manager as None
        self.show_grid: bool = True

        # The start positions will be one of the 4 islands in the corners of the board
        self.setup(player_start_pos="top_left_island")

        self.font = pygame.font.Font(None, 36)
        self.shop_window = pygame.Surface((800, 600))
        self.in_shop = False

    def setup(self, player_start_pos: str) -> None:
        # Load the TMX map and make it an attribute of the class
        self.tmx_map = {"map": load_pygame(os.path.join(".", "data", "new_maps", "100x100_map.tmx"))}
        if not self.tmx_map:
            raise ValueError("Failed to load the TMX map")

        # Initialize the grid manager
        self.grid_manager = GridManager(self.tmx_map["map"], TILE_SIZE)

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

        # Entities
        for obj in self.tmx_map["map"].get_layer_by_name("Ships"):
            if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
                # Cast the player position to int and snap to the grid
                grid_x = int(obj.x / TILE_SIZE) * TILE_SIZE
                grid_y = int(obj.y / TILE_SIZE) * TILE_SIZE
                self.player = Player(
                    pos=(grid_x, grid_y),
                    frames=self.world_frames["ships"]["player_test_ship"],
                    groups=(self.all_sprites,),
                )
        # print(f"Player Position: {self.player.rect.topleft}")

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

        # Create a new PlayerCamera with all the sprites
        sprites = list(self.all_sprites)  # Get all sprites from the temporary group
        self.all_sprites = PlayerCamera(self.tmx_map["map"], self.player.rect.topleft)
        # Add all sprites to the new camera group
        for sprite in sprites:
            self.all_sprites.add(sprite)

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

        # Pass the player's position to the draw method
        if self.player:
            mouse_pos = pygame.mouse.get_pos()
            self.grid_manager.draw(
                player_pos=self.player.rect.topleft,
                mouse_pos=mouse_pos,
                camera_offset=self.all_sprites.offset,
                camera_scale=self.all_sprites.scale,
            )

        # Draw the tile coordinates on the screen
        tile_x, tile_y = self.grid_manager.get_tile_coordinates(mouse_pos, self.player)
        tile_pos = (tile_x, tile_y)
        pygame.draw.circle(screen, (0, 255, 0), tile_pos, 5)  # Green circle at tile coordinates

        pygame.display.update()
