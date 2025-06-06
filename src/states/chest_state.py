import random
from typing import List, Optional

import pygame

from src.inventory import Chest, Inventory
# from src.states.base_state import BaseState
from src.sprites.islands.island_sprite import IslandSprite


class ChestState:
    def __init__(
        self,
        player: pygame.sprite.Sprite,
        inventory: Inventory,
        chest: Chest,
        island: pygame.sprite.Group[IslandSprite],
    ) -> None:
        self.font = pygame.font.Font(None, 36)

        self.player: pygame.sprite.Sprite = player
        self.island: pygame.sprite.Group = island
        self.chest: Chest = chest
        self.inventory: Inventory = inventory

        # collide can be None or a Sprite
        self.collide: Optional[pygame.sprite.Sprite] = None
        self.pressed: bool = False
        self.chest_collected: bool = False
        self.message: str = ""
        self.message_end_time: int = 0
        self.collected_message: str = ""
        self.collected_message_end_time: int = 0

        self.screen: pygame.Surface = pygame.Surface((500, 400), pygame.SRCALPHA)

        self.sprite_sheet: pygame.Surface = pygame.image.load("images/tilesets/Treasure+.png").convert_alpha()
        self.icons: dict[str, pygame.Surface] = {
            "Wooden chest": self.extract_icon(0, 144),
            "Golden chest": self.extract_icon(0, 160),
            "Silver chest": self.extract_icon(0, 176),
            "Mimic chest": self.extract_icon(0, 192),
            "Voyage scroll": self.extract_icon(176, 176),
        }

        chest_name, chest_icon = random.choice(list(self.icons.items()))
        self.chest_name: str = chest_name
        self.chest_icon: pygame.Surface = chest_icon
        self.collected_islands: set = set()

    def extract_icon(self, x: int, y: int, size: int = 16) -> pygame.Surface:
        return self.sprite_sheet.subsurface((x, y, size, size))

    def update(self) -> None:
        # Collision check, can be None if no collision
        self.collide = pygame.sprite.spritecollideany(self.player, self.island)

        if self.collide and hasattr(self.collide, "island_id"):
            self.chest_collected = True
            current_island_id = self.collide.island_id
            print(current_island_id)

            if current_island_id not in self.collected_islands:
                self.collected_islands.add(current_island_id)

    def render(self, screen: pygame.Surface) -> None:
        self.screen.fill((0, 0, 0, 0))  # Clear UI surface

        if self.collide:
            island_id = self.collide.island_id

            if island_id not in self.collected_islands:
                self.collected_islands.add(island_id)
                self.message = self.font.render(f"You just found a {self.chest_name}!", True, (0, 0, 0))
                self.inventory.add_item(self.chest_name, 1)
                self.message_end_time = pygame.time.get_ticks() + 3000  # Show message for 3 seconds
            else:
                self.message = self.font.render("There are no chests or voyages on this island!", True, (0, 0, 0))
                self.message_end_time = pygame.time.get_ticks() + 3000

        if pygame.time.get_ticks() < self.message_end_time:
            self.screen.blit(self.message, (50, self.screen.get_height() - 100))

        screen.blit(self.screen, (400, 125))
        pygame.display.flip()
