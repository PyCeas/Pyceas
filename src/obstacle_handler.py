import pygame


class ObstacleHandler:
    def __init__(self, player, obstacles):
        self.player = player
        self.obstacles = obstacles
        self.obstacle_damage = 15
        self.font = pygame.font.Font(None, 36)
        self.screen: pygame.Surface = pygame.Surface((600, 100), pygame.SRCALPHA)

        self.collide = None
        self.damage_applied = False
        self.message_end_time = 0

        self.is_flashing = False
        self.flashing_duration = 2000
        self.flashing_start_time = 0
        self.flash_color = "white"
        self.flash_toggle_interval = 200
        self.last_flash_toggle_time = 0
        self.current_flash_color = "red"

    def update(self, start_pos):
        self.collide = pygame.sprite.spritecollideany(self.player, self.obstacles)

        if self.collide and not self.damage_applied:
            self.player.player_hp -= self.obstacle_damage
            self.damage_applied = True
            self.message_end_time = pygame.time.get_ticks() + 2000  # Show message for 2s

        if not self.collide and self.damage_applied:
            self.damage_applied = False

        if self.player.player_hp <= 0:
            self.damage_applied = False
            self.player.player_hp = 0

            if hasattr(self.player, "rect"):
                self.player.rect.topleft = start_pos

        if self.player.rect.topleft == start_pos:
            self.player.player_hp = 100

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0, 0))  # Clear UI

        if self.collide and pygame.time.get_ticks() < self.message_end_time:
            message = self.font.render(f"The player has received -{self.obstacle_damage} damage!", True, "red2")
            self.screen.blit(message, (50, self.screen.get_height() - 100))

        if self.collide:
            if not self.is_flashing:
                self.is_flashing = True
                self.flashing_start_time = pygame.time.get_ticks()
                self.last_flash_toggle_time = self.flash_toggle_interval

        current_time = pygame.time.get_ticks()
        if self.is_flashing:
            if current_time - self.last_flash_toggle_time >= self.flash_toggle_interval:
                self.last_flash_toggle_time = current_time
                self.current_flash_color = "white" if self.current_flash_color == "red" else "red"
            self.player.player_square.fill(self.current_flash_color)

            if current_time - self.flashing_start_time > self.flashing_duration:
                self.is_flashing = False
                self.current_flash_color = "red"
        else:
            self.player.player_square.fill("red")

        screen.blit(self.screen, (155, 155))
