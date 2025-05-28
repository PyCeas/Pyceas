import os
import sys

# Add the project root to sys.path to allow imports to work when running tests directly with `python`.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pygame
import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.sprites.tiles.grid_manager import GridManager


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize Pygame for the test session."""
    pygame.init()
    pygame.font.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Grid Manager Test")
    yield
    pygame.quit()


@pytest.fixture
def grid_manager():
    grid = np.zeros((10, 10), dtype=int)  # 10x10 walkable grid
    return GridManager(grid_matrix=grid, tile_size=64)


# --- Tests ---
def test_grid_matrix_shape(grid_manager):
    assert grid_manager.grid_matrix.shape == (10, 10)


def test_grid_matrix_walkable(grid_manager):
    # All tiles should be walkable (0)
    assert np.all(grid_manager.grid_matrix == 0)


@given(
    mouse_x=st.integers(min_value=0, max_value=99),
    mouse_y=st.integers(min_value=0, max_value=99),
    offset_x=st.integers(min_value=-50, max_value=50),
    offset_y=st.integers(min_value=-50, max_value=50),
    scale=st.floats(min_value=0.5, max_value=2.0),
)
def test_get_tile_coordinates_hypothesis(mouse_x, mouse_y, offset_x, offset_y, scale):
    grid = np.zeros((10, 10), dtype=int)  # 10x10 walkable grid
    grid_manager = GridManager(grid_matrix=grid, tile_size=10)
    mouse_pos = (mouse_x, mouse_y)
    camera_offset = pygame.math.Vector2(offset_x, offset_y)
    camera_scale = scale
    x, y = grid_manager.get_tile_coordinates(mouse_pos, camera_offset, camera_scale)
    assert 0 <= x < grid_manager.width
    assert 0 <= y < grid_manager.height


def test_convert_mouse_to_world(grid_manager):
    mouse_pos = (10, 20)
    camera_offset = pygame.math.Vector2(2, 3)
    camera_scale = 2.0
    world_x, world_y = grid_manager._convert_mouse_to_world(mouse_pos, camera_offset, camera_scale)
    assert world_x == (10 - 2) / 2.0
    assert world_y == (20 - 3) / 2.0


@pytest.mark.parametrize(
    "tile_size, world_x, world_y, expected_x, expected_y",
    [
        (1, 5.7, 8.2, 5, 8),
        (16, 5.7, 8.2, 0, 0),
        (32, 5.7, 8.2, 0, 0),
        (64, 5.7, 8.2, 0, 0),
        (16, 20.0, 33.0, 1, 2),
        (64, 128.0, 192.0, 2, 3),
    ],
)
def test_convert_world_to_grid(tile_size, world_x, world_y, expected_x, expected_y):
    grid = np.zeros((10, 10), dtype=int)
    grid_manager = GridManager(grid_matrix=grid, tile_size=tile_size)
    grid_x, grid_y = grid_manager._convert_world_to_grid(world_x, world_y)
    assert grid_x == expected_x
    assert grid_y == expected_y


def test_clamp_grid_coordinates(grid_manager):
    # In bounds
    assert grid_manager._clamp_grid_coordinates(5, 5) == (5, 5)
    # Out of bounds
    assert grid_manager._clamp_grid_coordinates(-1, 0) == (0, 0)
    assert grid_manager._clamp_grid_coordinates(0, -1) == (0, 0)
    assert grid_manager._clamp_grid_coordinates(20, 5) == (9, 5)
    assert grid_manager._clamp_grid_coordinates(5, 20) == (5, 9)


def test_manual_inspect_grid_manager(grid_manager):
    """Creates a pygame window to see the grid manager visually."""
    import time

    print("Manual inspection: Close the window to exit.")
    running = True
    player_pos = (5, 5)  # Example player position
    mouse_pos = (0, 0)  # Example mouse position
    camera_offset = pygame.math.Vector2()
    camera_scale = 1.0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        grid_manager.draw(
            player_pos=player_pos,
            mouse_pos=mouse_pos,
            camera_offset=camera_offset,
            camera_scale=camera_scale,
            visible_radius=5,
        )
        pygame.display.flip()
        time.sleep(0.01)
