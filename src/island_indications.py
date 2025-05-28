import pygame

class IslandsIndicators:
    def __init__(self, player, island):
        self.player = player
        self.island = island

        self.font = pygame.font.Font("fonts/antiquity-print.ttf", 36)
        self.screen: pygame.Surface = pygame.Surface((600, 300), pygame.SRCALPHA)

        self.collide = None
        self.alpha = 0
        self.fade_speed = 3
        self.message_end_time = 0
        self.fading_in = False

    def update(self):
        previous_collide = self.collide
        self.collide = pygame.sprite.spritecollideany(self.player, self.island)

        if self.collide and not previous_collide:
            self.message_end_time = pygame.time.get_ticks() + 5000
            self.alpha = 0
            self.fading_in = True

        if self.fading_in and self.alpha < 255:
            self.alpha += self.fade_speed
            if self.alpha > 255:
                self.alpha = 255

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0, 0))

        if self.collide and pygame.time.get_ticks() < self.message_end_time:
            message_surface = self.font.render("Welcome to the island", True, (0, 0, 0))
            message_surface.set_alpha(self.alpha)
            self.screen.blit(message_surface, (50, self.screen.get_height() - 100))
        else:
            self.fading_in = False
            # self.collide = None  # Optional: reset collision

        screen.blit(self.screen, (155, 155))