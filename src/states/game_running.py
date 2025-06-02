"""
Represents the GameRunning state, where the player controls a ship and interacts with the game world.
"""

import json
import os

import pygame  # type: ignore
from pytmx.util_pygame import load_pygame  # type: ignore

from src.inventory import Inventory
from src.obstacle_handler import ObstacleHandler
from src.settings import TILE_SIZE, WORLD_LAYERS
from src.sprites.animations import AnimatedSprites
from src.sprites.base import BaseSprite
from src.sprites.camera.player_camera import PlayerCamera
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

        # Render the grid
        self.grid_manager: GridManager | None = None  # Initialize grid_manager as None
        self.show_grid: bool = True

        sprite_group: pygame.sprite.Group = pygame.sprite.Group()  # Initialize sprite group
        self.all_sprites: PlayerCamera  # Initialize all_sprites as PlayerCamera

        # The start positions will be one of the 4 islands in the corners of the board
        self.setup(player_start_pos="top_left_island", sprite_group=sprite_group)

        # Create the player camera and add all sprites to it
        sprites = list(sprite_group)
        self.all_sprites = PlayerCamera(self.tmx_map["map"], self.player.rect.topleft)
        for sprite in sprites:
            self.all_sprites.add(sprite)

        self.font = pygame.font.Font(None, 36)
        self.shop_window = pygame.Surface((800, 600))
        self.in_shop = False

        self.obstacle_handler = ObstacleHandler(self.player, self.obstacle_group)

    def setup(self, player_start_pos: str, sprite_group=None) -> None:
        if sprite_group is None:
            sprite_group = pygame.sprite.Group()

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

        # Sea
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Sea").tiles():
            BaseSprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
                groups=(sprite_group,),
                z=WORLD_LAYERS["bg"],
            )

        # Water animated
        for obj in self.tmx_map["map"].get_layer_by_name("Water"):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprites(
                        pos=(x, y),
                        frames=self.world_frames["water"],
                        groups=(sprite_group,),
                        z=WORLD_LAYERS["water"],
                    )

        # Shallow water
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Shallow Sea").tiles():
            BaseSprite(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surface, groups=(sprite_group,), z=WORLD_LAYERS["bg"])

        # Buildings
        for x, y, surface in self.tmx_map["map"].get_layer_by_name("Shop").tiles():
            self.shop = ShowShop(
                pos=(x * TILE_SIZE, y * TILE_SIZE), surface=surface, groups=(sprite_group,), z=WORLD_LAYERS["main"]
            )

        self.obstacle_group: pygame.sprite.Group = pygame.sprite.Group()
        obstacles = self.tmx_map["map"].get_layer_by_name("Obstacles")
        for x, y, surface in obstacles.tiles():
            BaseSprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
                groups=(sprite_group, self.obstacle_group),
                z=WORLD_LAYERS["bg"],
            )

        obstacles = self.tmx_map["map"].get_layer_by_name("Obstacles")
        for x, y, surface in obstacles.tiles():
            BaseSprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
                groups=(sprite_group, self.obstacle_group),
                z=WORLD_LAYERS["bg"],
            )

        # Islands
        islands = self.tmx_map["map"].get_layer_by_name("Islands")
        for x, y, surface in islands.tiles():
            BaseSprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=surface,
                groups=(sprite_group,),
                z=WORLD_LAYERS["bg"],
            )

        # Entities
        for obj in self.tmx_map["map"].get_layer_by_name("Ships"):
            if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
                # Cast the player position to int and snap to the grid
                grid_x = int(obj.x / TILE_SIZE) * TILE_SIZE
                grid_y = int(obj.y / TILE_SIZE) * TILE_SIZE
                # print(f"Player Position: ({grid_x, grid_y})")
                self.player = Player(
                    pos=(grid_x, grid_y),
                    frames=self.world_frames["ships"]["player_test_ship"],
                    groups=(sprite_group,),
                )

        # Coast
        for obj in self.tmx_map["map"].get_layer_by_name("Coast"):
            terrain = obj.properties["terrain"]
            side = obj.properties["side"]
            AnimatedSprites(
                pos=(obj.x, obj.y),
                frames=self.world_frames["coast"][terrain][side],
                groups=(sprite_group,),
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

        collide: bool = (
            self.player is not None
            and self.shop is not None
            and isinstance(self.player.rect, (pygame.Rect, pygame.FRect))
            and isinstance(self.shop.rect, (pygame.Rect, pygame.FRect))
            and self.player.rect.colliderect(self.shop.rect)
        )
        self.obstacle_collision = pygame.sprite.spritecollideany(self.player, self.obstacle_group)
        dt = self.clock.tick() / 1000
        self.all_sprites.update(dt)
        self.obstacle_handler.update()

        # Handle player movement and grid snapping
        if isinstance(self.all_sprites, PlayerCamera):
            camera_offset = self.all_sprites.offset
            scale = self.all_sprites.scale
        else:
            camera_offset = pygame.math.Vector2()
            scale = 1.0
        self.player.update(dt, grid=self.grid_manager, camera_offset=camera_offset, camera_scale=scale)

        # get events like keypress or mouse clicks
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:  # Toggle inventory with "I" key
                    self.game_state_manager.enter_state(Paused(self.game_state_manager, self.player_inventory))
                elif event.key == pygame.K_g:  # Toggle grid with "G" key
                    self.show_grid = not self.show_grid
                elif collide and event.key == pygame.K_e:
                    self.game_state_manager.enter_state(
                        WindowShop(self.game_state_manager, self.player, self.shop, self.player_inventory)
                    )

    def render(self, screen) -> None:
        """Draw sprites to the canvas."""
        screen.fill("#000000")
        if isinstance(self.all_sprites, PlayerCamera):
            self.all_sprites.draw(self.player.rect.center, show_grid=self.show_grid)
        self.obstacle_handler.render(screen)
        self.message = self.font.render(f"Player's Health: {self.player.player_hp}", True, (0, 0, 0))
        screen.blit(self.message, (50, screen.get_height() - 100))

        # Pass the player's position to the draw method
        if self.player and self.grid_manager is not None:
            mouse_pos = pygame.mouse.get_pos()
            if self.show_grid:
                self.grid_manager.draw(
                    player_pos=(int(self.player.rect.topleft[0]), int(self.player.rect.topleft[1])),
                    mouse_pos=mouse_pos,
                    camera_offset=self.all_sprites.offset,
                    camera_scale=self.all_sprites.scale,
                    visible_radius=5,
                )

            # Get tile coordinates with camera offset and scale
            tile_x, tile_y = self.grid_manager.get_tile_coordinates(
                mouse_pos, self.all_sprites.offset, self.all_sprites.scale
            )

            # Convert grid coordinates to screen coordinates
            dot_x = tile_x * TILE_SIZE * self.all_sprites.scale + self.all_sprites.offset.x
            dot_y = tile_y * TILE_SIZE * self.all_sprites.scale + self.all_sprites.offset.y

            # Draw the green dot at the screen coordinates
            pygame.draw.circle(screen, (0, 255, 0), (dot_x, dot_y), 5)  # Green circle at tile coordinates

        pygame.display.update()
