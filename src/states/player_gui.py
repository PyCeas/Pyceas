import pygame

from src.utils.currency import load_wallet


class Player_gui():
    def __init__(self, screen):
        self.font = pygame.font.Font(None, 36)
        self.screen = screen
        self.margin = 20
        self.wallet = load_wallet()
        self.player_wallet = self.wallet["player_wallet"]["quantity"]

    def draw_gui(self, screen: pygame.Surface):
        player_money = self.font.render(f"Gold: {self.player_wallet}", True, (255, 255, 255))

        text_wdith, text_height = player_money.get_size()
        x_pos = screen.get_width() - text_wdith - self.margin
        y_pos = self.margin
        self.screen.blit(player_money, (x_pos, y_pos))

        screen.blit(self.screen, dest=(0, 0))
        pygame.display.flip()  # Update the display