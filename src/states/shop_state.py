import os
import pygame
from pygame import Surface
from pygame.sprite import Group
from src.inventory import Inventory
from src.settings import WORLD_LAYERS
from src.states.base_state import BaseState
from src.sprites.shop.shop_sprite import ShowShop


class WindowShop(BaseState):
    def __init__(self, game_state_manager, player, show_shop: ShowShop, inventory: Inventory):
        super().__init__(game_state_manager)
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.Surface((800, 600))

        self.button_width: int = 100
        self.button_height: int = 50
        self.scroll_offset: int = 0

        self.button_actions: dict[str, tuple[pygame.Rect, pygame.Rect]] = {}
        self.inventory = inventory
        self.show_shop = show_shop
        self.player = player
        self.big_screen = pygame.Surface((1280, 720))

        self.max_visible_items: int = 5
        self.in_shop = True
        self.collide = False

        self.message = ""
        self.message_end_time = 0

        # Load sprite sheet
        sprite_sheet_path = os.path.join("images/tilesets/Treasure+.png")
        if not os.path.exists(sprite_sheet_path):
            print(f"Error: Sprite sheet not found at '{sprite_sheet_path}'")
            exit()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)

        # Extract icons using `ShowShop.extract_icon`
        self.icons = {
            "Gold Coin": ShowShop.extract_icon(self.sprite_sheet, 0, 0),
            "Silver Coin": ShowShop.extract_icon(self.sprite_sheet, 16, 0),
            # Add other icons as needed...
        }

    def update(self, events):
        # Check collision
        if hasattr(self.player, "rect") and hasattr(self.show_shop, "rect"):
            self.collide = self.player.rect.colliderect(self.show_shop.rect)
        else:
            self.collide = False

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    if event.key == pygame.K_q and self.in_shop:
                        self.in_shop = False
                        self.game_state_manager.exit_state()

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_clicks(event.pos)
                case pygame.MOUSEWHEEL:
                    self.scroll_offset = max(0, self.scroll_offset - event.y)
                    max_offset = max(0, len(self.inventory.get_items()) - self.max_visible_items)
                    self.scroll_offset = min(self.scroll_offset, max_offset)

    def render(self, screen: Surface):
        if self.collide:
            welcome_message = self.font.render("Press 'E' to enter the shop!", True, (0, 0, 0))
            self.big_screen.blit(welcome_message, (50, self.screen.get_height() - 60))

        if self.in_shop:
            self.screen.fill((0, 0, 0))

            self.button_actions = {}

            items = list(self.inventory.get_items().items())
            visible_items = items[self.scroll_offset: self.scroll_offset + self.max_visible_items]
            y_offset = 50

            for item, quantity in visible_items:
                if item in self.icons:
                    self.screen.blit(self.icons[item], (50, y_offset))

                quantity_text = self.font.render(f"x{quantity}", True, (255, 255, 255))
                self.screen.blit(quantity_text, (100, y_offset + 5))

                text = self.font.render(item, True, (255, 255, 255))
                self.screen.blit(text, (150, y_offset))

                use_button, discard_button = self.draw_buttons(400, y_offset, item)

                self.button_actions[item] = (use_button, discard_button)
                y_offset += 60

            hint_text = self.font.render("Press Q to quit the shop!", True, (200, 200, 200))
            self.screen.blit(hint_text, (50, self.screen.get_height() - 60))

            if self.message and pygame.time.get_ticks() < self.message_end_time:
                # Render the message text
                message_text = self.font.render(self.message, True, (255, 255, 0))  # Yellow

                # Measure the message text size
                text_width, text_height = message_text.get_size()

                # Message background
                message_bg_x = 40
                message_bg_y = self.screen.get_height() - 120
                message_bg_width = text_width + 20  # Add padding
                message_bg_height = text_height + 10  # Add padding

                # Draw background rectangle for the message
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),  # Black background
                    (message_bg_x, message_bg_y, message_bg_width, message_bg_height),
                )

                # Draw the message text on top of the background
                self.screen.blit(
                    message_text,
                    (message_bg_x + 10, message_bg_y + 5),  # Position text with padding
                )

            # blit tmp self.screen to the actual display (screen form the argument)
            screen.blit(self.screen, dest=(0, 0))
            pygame.display.flip()  # Update the display

    def handle_mouse_clicks(self, mouse_pos):
        for item, (use_button, discard_button) in self.button_actions.items():
            if use_button.collidepoint(mouse_pos):
                self.message = self.inventory.buy_item(item, 1)
                self.message_end_time = pygame.time.get_ticks() + 3000  # 3 seconds
            elif discard_button.collidepoint(mouse_pos):
                self.message = self.inventory.sell_item(item, 1)
                self.message_end_time = pygame.time.get_ticks() + 4000  # 4 seconds

    def draw_buttons(self, x: int, y: int, item: str) -> tuple[pygame.Rect, pygame.Rect]:
        use_button = pygame.Rect(x, y, self.button_width, self.button_height)
        discard_button = pygame.Rect(x + self.button_width + 10, y, self.button_width, self.button_height)

        pygame.draw.rect(self.screen, (0, 255, 0), use_button)  # Green
        pygame.draw.rect(self.screen, (150, 75, 0), discard_button)  # Brown

        use_text = self.font.render("Buy", True, (0, 0, 0))  # Black
        discard_text = self.font.render("Sell", True, (0, 0, 0))

        self.screen.blit(use_text, (x + 10, y + 10))
        self.screen.blit(discard_text, (x + self.button_width + 20, y + 10))

        return use_button, discard_button
