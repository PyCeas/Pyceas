# Grid Manager Guide

The word `world` refers in this context to the `pytmx` map, which is the game world where the player interacts with
tiles.

### Key Features

- **Grid Drawing**: The grid is drawn on the screen, allowing players to see the layout of the game world.
- **Pathfinding Visualization**: The system can visualize the pathfinding process, showing the route taken by the AI or
  player.
- **Edge Case Handling**: The system handles edge cases, such as clicks outside the `pytmx` remain withing the bounds of
  the `pytmx map`.
- **Mouse Indicator**: A mouse indicator is rendered to show the current tile under the mouse cursor, helping players
  understand where they are clicking.
- **Coordinate Conversion**: The system handles the conversion between grid coordinates and pixel coordinates, ensuring
  accurate rendering and interaction with the game world.
- **Customizable Grid Size**: The grid size can be adjusted to fit different game worlds, allowing for flexibility in
  design.

## Controls Documentation

### Controls Summary

- **Keyboard**: Press `G` to toggle the grid on and off.
- **Mouse**: When the grid is enabled, clicking on a tile will show its pixel coordinates.
  Without it, you can still click on the tile, but it will not show the pixel coordinates and the grid will not be
  drawn.

## Coordinate Systems

### Mouse Coordinates Summary

- **Description**: Represents the position of the mouse cursor on the screen.
- **Notation**: Denoted as `(mouse_x, mouse_y)`.

### World Coordinates Summary

- **Description**: Represents the position in the game world, accounting for camera offset and scale.
- **Notation**: Denoted as `(world_x, world_y)`.

### Grid Coordinates Summary

- **Description**: Represents the position of a tile in the grid, based on the world coordinates.
- **Notation**: Denoted as `(grid_x, grid_y)`.

### Screen (Pixel) Coordinates Summary

- **Description**: Represents the position on the screen in pixels.
- **Notation**: Denoted as `(screen_x, screen_y)`.

## Conversion Processes

### Mouse to World Coordinates

- **Description**: Converts mouse coordinates to world coordinates by adjusting for camera offset and scale.

**Mathematical Notation**:

$$
\begin{align*}
\text{world\_x} &= \frac{\text{mouse\_x} - \text{camera\_offset.x}}{\text{camera\_scale}} \\
\text{world\_y} &= \frac{\text{mouse\_y} - \text{camera\_offset.y}}{\text{camera\_scale}}
\end{align*}
$$

**Code Example**:

```python
def _convert_mouse_to_world(mouse_pos, camera_offset, camera_scale):
    world_x = (mouse_pos[0] - camera_offset.x) / camera_scale
    world_y = (mouse_pos[1] - camera_offset.y) / camera_scale
    return world_x, world_y
```

## Running Tests

Tests in the project use `pytest`. To run the tests:
`pytest tests/test_grid_manager.py`

## No Collisions Implemented Yet

- With the rework, you can still move over objects, like 'Islands,' this is intentional and needs to be changed later on
  with enhancements.
- The ` 0` is the tile that is walkable, and the `1` is the tile that is not walkable. This is a placeholder for future
  collision detection implementation.