import pygame  # ignore

from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, WORLD_LAYERS
from src.sprites.camera.group import AllSprites
from src.sprites.tiles.grid_manager import GridManager


class PlayerCamera(AllSprites):
    """
    A sprite group that manages rendering and camera logic focused on the player.

    This class extends the functionality of the AllSprites group by adjusting
    sprite positions based on the player's location, creating a camera effect.
    It supports rendering sprites at different layers (background, main, foreground)
    and scales sprites dynamically based on the camera's zoom level.

    Attributes:
        display_surface (pygame.Surface): The surface to render the sprites on.
        offset (pygame.math.Vector2): The camera's offset, calculated relative to the player's position.
        scale (float): The scaling factor for rendering sprites.
    """

    def __init__(self, tmx_map=None, player_start_pos=None):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        if not self.display_surface:
            raise ValueError("Display surface is not initialized")

        if tmx_map is None:
            raise ValueError("TMX map cannot be None")
        if player_start_pos is None:
            raise ValueError("Player start position cannot be None")

        self.player_start_pos = player_start_pos
        self.tmx_map = tmx_map
        self.offset = pygame.math.Vector2()
        self.scale = 2.0
        self.grid = GridManager(tmx_map, tile_size=TILE_SIZE)
        self.player_start_pos = player_start_pos

    def draw(self, player_center, show_grid=False):
        # Calculate offsets
        self.offset.x = -(player_center[0] * self.scale - SCREEN_WIDTH / 2)
        self.offset.y = -(player_center[1] * self.scale - SCREEN_HEIGHT / 2)

        # print(f"Player Center: {player_center}")
        # print(f"Camera Offset: {self.offset}")

        # Separate sprites into layers
        background_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS["main"]]
        main_sprites = [sprite for sprite in self if sprite.z == WORLD_LAYERS["main"]]
        foreground_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS["main"]]

        # Render each layer
        for layer in (background_sprites, main_sprites, foreground_sprites):
            for sprite in layer:
                # Scale the image
                scaled_image = pygame.transform.scale(
                    sprite.image,
                    (
                        int(sprite.rect.width * self.scale),
                        int(sprite.rect.height * self.scale),
                    ),
                )

                # Adjust the rect to the new scale
                scaled_rect = scaled_image.get_rect(
                    center=(
                        int(sprite.rect.center[0] * self.scale),
                        int(sprite.rect.center[1] * self.scale),
                    )
                )

                # Add offset to the rect position
                scaled_rect.topleft = (
                    scaled_rect.topleft[0] + int(self.offset.x),
                    scaled_rect.topleft[1] + int(self.offset.y),
                )

                # Ensure display_surface is valid before blitting
                if self.display_surface is None:
                    raise ValueError("self.display_surface cannot be None")
                self.display_surface.blit(scaled_image, scaled_rect.topleft)
