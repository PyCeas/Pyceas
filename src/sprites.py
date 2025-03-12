"""custom sprites classes"""

import pygame  # type: ignore
from pygame import FRect

from src.inventory import Inventory
from src.settings import (
    ANIMATION_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    WORLD_LAYERS,
)


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.z = WORLD_LAYERS["main"]

        # graphics
        self.frame_index, self.frames = 0, frames
        self.facing_direction = "down"

        # movement
        self.direction = pygame.math.Vector2()
        # self.speed = 250

        # sprite setup
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("red")
        # self.image = self.frames[self.get_state()][self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        # self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = "right" if self.direction.x > 0 else "left"
            if self.direction.y != 0:
                self.facing_direction = "down" if self.direction.x > 0 else "up"
        return f"{self.facing_direction}{'' if moving else '_idle'}"


class AllSprites(pygame.sprite.Group):
    """A sprite group that handles every sprite and handles the camera logic"""

    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        if not self.display_surface:
            raise ValueError("Display surface is not initialized")

        self.offset = pygame.math.Vector2()
        self.scale = 2.0

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

            # scaling of the ghost preview
            # scaled_preview = pygame.transform.scale(player_preview,
            # (int(player_preview_rect.width * self.scale), int(player_preview_rect.height * self.scale)))
            # scaled_preview_rect = scaled_preview.get_rect(center=(
            # player_preview_rect.center[0] * self.scale, player_preview_rect.center[1] * self.scale))
            # scaled_preview_rect.topleft += self.offset

            # self.display_surface.blit(scaled_preview, scaled_preview_rect.topleft)

    # method for zooming (might be usefull later?)
    # def set_scale(self, scale):
    #     self.scale = max(scale, 0.1)


class Player(Entity):
    """move tile by tile"""

    rect: FRect

    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

        # Ensure self.image is not None
        if self.image is None:
            raise ValueError("self.image cannot be None")

        # ghost preview
        self.player_preview = self.image.copy()
        self.player_preview.set_alpha(128)

        self.inventory = Inventory()
        self.mouse_have_been_pressed: bool = False
        self.draggin = False
        self.offset_x = 0
        self.offset_y = 0

    def input(self) -> None:
        """move the player and show a ghost to preview the move"""
        # Reset direction
        self.direction = pygame.math.Vector2(0, 0)

        # gost preview
        mouse_pos = pygame.mouse.get_pos()

        # get the relative pos of the player from the mouse
        # to know on wich axis the player will move
        delta_x = abs(self.rect.centerx - mouse_pos[0])
        delta_y = abs(self.rect.centery - mouse_pos[1])

        # #  move the gost on the x axis
        # self.player_preview_rect = self.rect.copy()
        # if delta_x > delta_y:
        #     if delta_x < (TILE_SIZE / 2):
        #         # don't move the gost if the mouse is on the player hitbox
        #         self.player_preview_rect.x = self.rect.x
        #     elif mouse_pos[0] > self.rect.centerx:
        #         # go right
        #         self.player_preview_rect.x = self.rect.x + TILE_SIZE
        #     else:
        #         # go left
        #         self.player_preview_rect.x = self.rect.x - TILE_SIZE
        # # move the gost on the y axis
        # else:
        #     if delta_y < (TILE_SIZE / 2):
        #         # don't move if the mouse is on the player hitbox
        #         self.player_preview_rect.y = self.rect.y
        #     elif mouse_pos[1] > self.rect.centery:
        #         # go down
        #         self.player_preview_rect.y = self.rect.y + TILE_SIZE
        #     else:
        #         # go up
        #         self.player_preview_rect.y = self.rect.y - TILE_SIZE

        # move the player
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_have_been_pressed = False
            return
        if self.mouse_have_been_pressed:
            return

        self.mouse_have_been_pressed = True

        # move on the x axis
        if delta_x > delta_y:
            if delta_x >= (TILE_SIZE / 2):
                if mouse_pos[0] > self.rect.centerx:
                    self.direction.x = 1
                else:
                    self.direction.x = -1
        else:
            if delta_y >= (TILE_SIZE / 2):
                if mouse_pos[1] > self.rect.centery:
                    self.direction.y = 1
                else:
                    self.direction.y = -1

        self.rect.x += self.direction.x * TILE_SIZE
        self.rect.y += self.direction.y * TILE_SIZE

        # return None

    def update(self, dt) -> None:
        """blit player image and gost preview to a given surface"""
        self.input()
        self.animate(dt)


class Tile(pygame.sprite.Sprite):
    """Handle tiles for the map"""

    def __init__(
        self,
        *groups: pygame.sprite.Group,
        pos: tuple[float, float],
        surf: pygame.Surface,
        name: str | None = None,
    ) -> None:
        r"""
        Initialize a Tile instance.

        Args:
            *groups (pygame.sprite.Group): One or more sprite groups that this tile will belong to.
            pos (Tuple[float, float]): The top-left position where the tile will be placed on the screen.
            surf (pygame.Surface): The surface (image) that will be drawn for this tile.
            name (Optional[str]): An optional name for the tile.

        Note:
            There is a known typing error related to missing type parameters for the generic type 'Group' in pygame.
            You may see warnings like:
            - src\\sprites.py:107: error: Missing type parameters for generic type 'Group' [type-arg]
            - src\\GUI\\game_manager.py:45: error: Missing type parameters for generic type 'SpriteGroup' [type-arg]

            These errors can be ignored for now, as they are related to type annotations in pygame's codebase.
        """
        super().__init__(*groups)

        self.pos = pos
        self.surf = surf
        self.name = name

        self.image: pygame.Surface = self.surf
        self.rect: pygame.FRect = self.image.get_frect(topleft=self.pos)

    def draw(self, display_surface: pygame.Surface, offset: tuple[float, float] = (0, 0)) -> None:
        """Could be useful for a camera?"""
        offset_rect = self.rect.move(offset)
        display_surface.blit(self.image, offset_rect)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surf: pygame.Surface, groups, z=WORLD_LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.z = z


class AnimatedSprites(Sprite):
    def __init__(self, pos, frames, groups, z=WORLD_LAYERS["main"]):
        self.frame_index, self.frames = 0, frames
        super().__init__(pos, frames[self.frame_index], groups, z)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)
