class Player(Entity):
    """Move tile-by-tile on a grid"""

    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

        self.grid_pos = pygame.math.Vector2(
            pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        )  # Store player's position in grid coordinates
        self.target_grid_pos = self.grid_pos.copy()  # Target position on the grid
        self.rect.topleft = (self.grid_pos.x * TILE_SIZE, self.grid_pos.y * TILE_SIZE)  # Align rect with the grid
        self.mouse_have_been_pressed = False

    def snap_to_grid(self):
        """Ensure the player's rect is perfectly aligned with the grid"""
        self.rect.topleft = (self.grid_pos.x * TILE_SIZE, self.grid_pos.y * TILE_SIZE)

    def input(self):
        """Handle mouse input to move the player on the grid"""
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_have_been_pressed = False
            return

        if self.mouse_have_been_pressed:
            return

        self.mouse_have_been_pressed = True

        # Get mouse position and convert it to grid coordinates
        mouse_pos = pygame.mouse.get_pos()
        mouse_grid_pos = pygame.math.Vector2(
            mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE
        )

        # Check if the mouse click is on an adjacent tile
        delta = mouse_grid_pos - self.grid_pos
        if delta.length() == 1:  # Ensure it's exactly one tile away
            self.target_grid_pos = mouse_grid_pos

    def update(self):
        """Update the player's position"""
        if self.grid_pos != self.target_grid_pos:
            # Move the player one step closer to the target position
            delta = self.target_grid_pos - self.grid_pos
            if delta.x != 0:
                self.grid_pos.x += delta.x / abs(delta.x)  # Move horizontally
            elif delta.y != 0:
                self.grid_pos.y += delta.y / abs(delta.y)  # Move vertically

            self.snap_to_grid()
