import pygame  # ignore

from src.settings import SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_LAYERS
from src.sprites.camera.group import AllSprites


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

    def draw(self, player_center):
        # Calculate offsets
        self.offset.x = -(player_center[0] * self.scale - SCREEN_WIDTH / 2)
        self.offset.y = -(player_center[1] * self.scale - SCREEN_HEIGHT / 2)

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
