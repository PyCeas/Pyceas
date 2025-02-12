import sys
import warnings
import pygame
import pygame.freetype

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
TILE_SIZE = 16
FPS = 60


if not getattr(pygame, "IS_CE", False):
    raise ImportError(
        "The game requires Pygame CE to function. "
        "(hint: type pip uninstall pygame and then pip install pygame-ce)"
    )

if sys.version_info < (3, 12):
    warnings.warn(
        f"The project is currently running under Python "
        f"{sys.version_info.major}.{sys.version_info.minor}. "
        f"Consider upgrading to 3.12 or the most recent version available "
        f"before running the game further.",
        DeprecationWarning,
    )
