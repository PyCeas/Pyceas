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

    def update(self):
        self.collide = pygame.sprite.spritecollideany(self.player, self.obstacles)

        if self.collide and not self.damage_applied:
            self.player.player_hp -= self.obstacle_damage
            self.damage_applied = True
            self.message_end_time = pygame.time.get_ticks() + 2000  # Show message for 2s

        if not self.collide and self.damage_applied:
            self.damage_applied = False

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0, 0))  # Clear UI

        if self.collide and pygame.time.get_ticks() < self.message_end_time:
            message = self.font.render(f"The player has received -{self.obstacle_damage} damage!", True, "red2")
            self.screen.blit(message, (50, self.screen.get_height() - 100))

        screen.blit(self.screen, (155, 155))
        # pygame.display.flip()
