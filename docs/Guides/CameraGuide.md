# Camera Guide

The word `world` refers in this context to the `pytmx` map, which is the game world where the player interacts with
tiles.

## Overview

This document explains how to handle camera offset and scale in a game development context. Understanding these concepts
is crucial for accurate rendering and interaction with the game world.

## Camera Offset

- **Purpose**: The camera offset shifts the visible area of the game world to center the player or a specific point of
  interest on the screen.
- **Effect**: The player stays centered or the view follows the player.
- **Conversion**: When converting screen (mouse) coordinates to world coordinates, the camera offset must be subtracted
  from the mouse position, it's necessary to adjust for the camera offset to get the correct position in the game world.

## Camera Scale (Zoom)

- **Purpose**:The camera scale changes the size of the tiles on the screen.
- **Effect**: This affects how the game world is displayed and how the player interacts with it.
- **Conversion**: The scale factor is used to convert between pixel coordinates and grid coordinates.
- To convert between screen and world coordinates, you must divide by the camera scale.

## Importance

Properly accounting for camera offset and scale is essential for:

- Ensuring that the game world is rendered correctly on the screen.
- Allowing accurate interaction with the game world, such as clicking on tiles or objects.
- Maintaining consistency between the visual representation and the underlying game logic.
- Making sure that mouse clicks correspond to the correct positions in the game world.

## In Code

```python
# Constants
TILE_SIZE = 16  # Define the size of each tile in pixels
camera_offset_x, camera_offset_y = 100, 50  # Example camera offset values
camera_scale = 1.5  # Example camera scale value

# Mouse position
mouse_x, mouse_y = 320, 240  # Example mouse coordinates

# Convert mouse position to world coordinates
world_x = (mouse_x - camera_offset_x) / camera_scale
world_y = (mouse_y - camera_offset_y) / camera_scale

# Convert world position to grid (tile) coordinates
grid_x = int(world_x // TILE_SIZE)
grid_y = int(world_y // TILE_SIZE)
```