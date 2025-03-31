from abc import ABC

import pygame
from pygame import Surface

from src.settings import TILE_SIZE

class GridManager:
    """Handles grid rendering and interaction."""

    def __init__(
        self,
        display_surface: pygame.Surface,
        tile_size: int = TILE_SIZE,
        grid_color: str = "grey",
        hover_color: str = "azure4"
    ):
        self.display_surface: pygame.Surface = display_surface
        self.tile_size: int = tile_size
        self.grid_color: str = grid_color
        self.hover_color: str = hover_color
        self.overlay_alpha: int = 50    # Transparency level (0-255)
        self.block_size: int = 64
        self.coordinates: dict[tuple[int, int], tuple[int, int]] = {}

    def draw(self, mouse_pos: tuple[int, int], valid_moves: set[tuple[int, int]] = None) -> None:
        
        overlay: Surface = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))  # Fully transparent background
        
        font = pygame.font.SysFont("Arial", 12)
        
        for x in range(0, self.display_surface.get_width(), self.block_size):
            for y in range(0, self.display_surface.get_height(), self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                
                # Highlight valid tiles
                if valid_moves and (x, y) in valid_moves:
                    pygame.draw.rect(overlay, (0, 255, 0, 100), rect)
                elif rect.collidepoint(mouse_pos):
                    pygame.draw.rect(overlay, (0, 0, 255, 100), rect)

                # Draw grid lines
                pygame.draw.rect(self.display_surface, self.grid_color, rect, 1)
                self.coordinates[(x, y)] = (x // self.block_size, y // self.block_size)

                # Render the x, y integers
                text = font.render(f"({self.coordinates[(x, y)][0]}, {self.coordinates[(x, y)][1]})", True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.display_surface.blit(text, text_rect)

        # Blit the transparent overlay onto the display surface
        self.display_surface.blit(overlay, (0, 0))

    def get_tile_coordinates(self, mouse_pos: tuple[int, int], player: object) -> tuple[int, int]:
        x, y = mouse_pos
        player_x, player_y = player.position
        max_distance: int = 6

        # Calculate the distance from the player's position to the mouse position
        distance = ((x - player_x) ** 2 + (y - player_y) ** 2) ** 0.5

        return (x // self.block_size * self.block_size, y // self.block_size * self.block_size) if distance > max_distance else None

    def get_coordinates(self, x, y):
        """Returns the coordinates of a tile at position (x, y)."""

        return self.coordinates.get((x, y))