# Coordinate Conversions Guide

## Overview

This document explains how to convert between grid (tile) coordinates and pixel coordinates in the context of game
development. These conversions are essential for translating game logic positions to screen positions and vice versa.

### Description of the Grid coordinates

The grid coordinates are a system used to represent the position of tiles on the game board. Each tile is represented by
a pair of coordinates, which can be converted to pixel coordinates for rendering on the screen.

## Coordinate System

### Grid (Tile) Coordinates

- **Description**: Grid coordinates represent the position of a tile on the game board
- **Notation**: The x and y-axis as `(tile_x, tile_y)`, where `tile_x` is the column and `tile_y` is the row.
- **Example**: `(16, 10)` refers to the tile at column 16 and row 10.

### Pixel Coordinates

- **Description**: Pixel coordinates represent the exact position on the screen, measured in pixels,
- **Notation**: Denoted as `(pixel_x, pixel_y)`.
- **Example**: `(256, 160)` refers to the pixel at x=256 and y=160.

## Conversion Between Coordinate System

```py

# Constants
TILE_SIZE: int = 16

# From grid to pixel conversion
tile_x, tile_y: int = 16, 10
pixel_x: int = tile_x * TILE_SIZE  # 256
pixel_y: int = tile_y * TILE_SIZE  # 160

# From pixel to grid conversion
grid_x: int = pixel_x // TILE_SIZE  # 16
grid_y: int = pixel_y // TILE_SIZE  # 10
```

## Conversion in mathematical notation

For grid (position) to pixel conversion:

$$
\begin{align*}
\text{pixel}_x &= \text{tile}_x \times \text{TILE_SIZE} \\
\text{pixel}_y &= \text{tile}_y \times \text{TILE_SIZE}
\end{align*}
$$

Given $\text{TILE_SIZE} = 16$, $\text{tile_x} = 16$, and $\text{tile_y} = 10$

$$
\begin{align*}
\text{256}_x &= \text{16}_x \times \text{16} \\
\text{160}_y &= \text{10}_y \times \text{16}
\end{align*}
$$

For pixel (position) to grid conversion:

$$
\begin{align*}
\text{grid}_x &= \left\lfloor \frac{\text{pixel}_x}{\text{TILE_SIZE}} \right\rfloor \\
\text{grid}_y &= \left\lfloor \frac{\text{pixel}_y}{\text{TILE_SIZE}} \right\rfloor
\end{align*}
$$

Given $\text{TILE_SIZE} = 16$, $\text{tile_x} = 256$, and $\text{tile_y} = 160$

$$
\begin{align*}
\text{16}_x &= \left\lfloor \frac{\text{256}_x}{\text{16}} \right\rfloor \\
\text{10}_y &= \left\lfloor \frac{\text{160}_y}{\text{16}} \right\rfloor
\end{align*}
$$