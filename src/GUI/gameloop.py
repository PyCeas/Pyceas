# import sys

# # import dataclasses and typchecking
# from dataclasses import dataclass, field
# from os.path import join

# # import pygame related
# import pygame
# from pytmx.util_pygame import load_pygame  # type: ignore

# import src.sprites

# # import Pygame specific objects, functions and functionality
# from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, WORLD_LAYERS
# from src.sprites import AnimatedSprites
# from src.support import all_character_import, coast_importer, import_folder


# @dataclass
# class GUI:
#     """Graphial User Interface vertion of the game, using pygame-ce"""

#     screen_size: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
#     screen: pygame.Surface = field(init=False)

#     # groups
#     # all_sprites: pygame.sprite.Group = field(
#     #     init=False, default_factory=pygame.sprite.Group
#     # )

#     def __post_init__(self):
#         pygame.init()
#         self.screen = pygame.display.set_mode(self.screen_size)
#         pygame.display.set_caption("PySeas")
#         self.clock = pygame.Clock()

#         # self.players: list[src.sprites.Player] = [src.sprites.Player()]

#         self.all_sprites = src.sprites.AllSprites()
#         self.running = True
#         self.import_assets()
#         self.setup(
#             tmx_maps=self.tmx_map["map"], player_start_pos="top_left_island"
#         )  # The start positions will be one of the 4 islands in the corners of the board
#         self.camera_mode = "drag"

#     def import_assets(self):
#         """load the map"""
#         # The map was made as a basic start for the game, it can be changes or altered if it is better for the overall
#         flow of the game
#         self.tmx_map = {
#             "map": load_pygame(join(".", "data", "new_maps", "100x100_map.tmx"))
#         }

#         self.world_frames = {
#             "water": import_folder(".", "images", "tilesets", "water"),
#             "coast": coast_importer(6, 6, ".", "images", "tilesets", "coast"),
#             "ships": all_character_import(".", "images", "tilesets", "ships"),
#         }
#         # print(self.world_frames["ships"])

#     def setup(self, tmx_maps, player_start_pos):
#         """create tiles"""

#         # Sea
#         for x, y, surface in tmx_maps.get_layer_by_name("Sea").tiles():
#             src.sprites.Sprite(
#                 (x * TILE_SIZE, y * TILE_SIZE),
#                 surface,
#                 self.all_sprites,
#                 WORLD_LAYERS["bg"],
#             )

#         # Water animated
#         for obj in tmx_maps.get_layer_by_name("Water"):
#             for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
#                 for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
#                     AnimatedSprites(
#                         (x, y),
#                         self.world_frames["water"],
#                         self.all_sprites,
#                         WORLD_LAYERS["water"],
#                     )

#         # Shallow water
#         for x, y, surface in tmx_maps.get_layer_by_name("Shallow Sea").tiles():
#             src.sprites.Sprite(
#                 (x * TILE_SIZE, y * TILE_SIZE),
#                 surface,
#                 self.all_sprites,
#                 WORLD_LAYERS["bg"],
#             )

#         # Islands
#         islands = tmx_maps.get_layer_by_name("Islands")
#         for x, y, surface in islands.tiles():
#             src.sprites.Sprite(
#                 (x * TILE_SIZE, y * TILE_SIZE),
#                 surface,
#                 self.all_sprites,
#                 WORLD_LAYERS["bg"],
#             )

#         # Enitites
#         for obj in tmx_maps.get_layer_by_name("Ships"):
#             if obj.name == "Player" and obj.properties["pos"] == player_start_pos:
#                 self.player = src.sprites.Player(
#                     pos=(obj.x, obj.y),
#                     frames=self.world_frames["ships"]["player_test_ship"],
#                     groups=self.all_sprites,
#                 )

#         # Coast
#         for obj in tmx_maps.get_layer_by_name("Coast"):
#             terrain = obj.properties["terrain"]
#             side = obj.properties["side"]
#             AnimatedSprites(
#                 (obj.x, obj.y),
#                 self.world_frames["coast"][terrain][side],
#                 self.all_sprites,
#                 WORLD_LAYERS["bg"],
#             )

#     def run(self) -> None:
#         """main loop of the game"""
#         while self.running:
#             self.handle_events()
#             self.render()

#     def handle_events(self) -> None:
#         """get events like keypress or mouse clicks"""
#         for event in pygame.event.get():
#             match event.type:
#                 case pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()

#     def render(self) -> None:
#         """draw sprites to the canvas"""
#         dt = self.clock.tick() / 1000
#         self.screen.fill("#000000")

#         self.all_sprites.update(dt)
#         self.all_sprites.draw(
#             self.player.rect.center,
#             self.player.player_preview,
#             self.player.player_preview_rect,
#         )

#         """No need to loop through the players because it is now in the sprite group AllSprites"""
#         # draw players on top of the other sprites
#         # for player in self.players:
#         #     player.render(surface=self.screen)

#         pygame.display.update()
