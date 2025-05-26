import pygame

from src.states.base_state import BaseState

class ObstacleSate(BaseState):
    def __init__(self, game_state_manager, player, obstacles):
        super().__init__(game_state_manager)
        self.player = player
        self.obstacles = obstacles
        self.obstacle_damage = 15
        self.font = pygame.font.Font(None, 36)
        self.screen: pygame.Surface = pygame.Surface((500, 400))

    def update(self, events):
        self.collide = pygame.sprite.spritecollideany(self.player, self.obstacles)

        for event in events:
            if self.collide:
                self.player.player_hp -= self.obstacle_damage
                if self.collide == False:
                    self.game_state_manager.exit_state()

    def render(self, screen: pygame.Surface):
        if self.collide:
            self.message = self.font.render(f"The player has recieved -{self.obstacle_damage} damage!", True, (255, 255, 255))
            self.screen.blit(self.message, (50, self.screen.get_height() - 100))

        screen.blit(self.screen, (155, 155))
        pygame.display.flip()

