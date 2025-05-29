import pygame  # type: ignore

from src.inventory import Inventory
from src.settings import TILE_SIZE


class InventoryGUI:
    """Graphical User Interface to display the player's inventory."""

    def __init__(self, screen: pygame.Surface, inventory: Inventory) -> None:
        self.screen: pygame.Surface = screen
        self.inventory: Inventory = inventory
        self.font: pygame.font.Font = pygame.font.Font(None, 36)
        self.running: bool = False

        # Scrolling inventory
        self.scroll_offset: int = 0
        self.max_visible_items: int = 10
        self.item_height: int = 60

        # Load a sprite sheet and extract the icons (Testing purposes)
        # To be replaced when:
        # 1) Sprite sheet has been decided.
        # 2) A 'Buy', 'Found' or 'Add' in-game feature has been implemented
        self.sprite_sheet = pygame.image.load("images/tilesets/Treasure+.png").convert_alpha()
        self.icons: dict[str, pygame.Surface] = {
            "Gold Coin": self.extract_icon(0, 0),
            "Silver Coin": self.extract_icon(16, 0),
            "Coin Stack (1)": self.extract_icon(32, 0),
            "Coin Stack (2)": self.extract_icon(48, 0),
            "Circular Gem": self.extract_icon(64, 0),
            "Single Gold Bar": self.extract_icon(0, 16),
            "Gold Bar Stack": self.extract_icon(16, 16),
            "Treasure Block": self.extract_icon(32, 16),
            "Golden Crown": self.extract_icon(0, 32),
            "Ornate Cup": self.extract_icon(16, 32),
            "Golden Figurine": self.extract_icon(32, 32),
            "Simple Sword": self.extract_icon(0, 48),
            "Ornate Sword": self.extract_icon(16, 48),
            "Double-Bladed Axe": self.extract_icon(32, 48),
            "Spear": self.extract_icon(48, 48),
            "Circular Shield": self.extract_icon(64, 48),
            "Golden Trophy": self.extract_icon(0, 64),
            "Candelabra": self.extract_icon(16, 64),
            "Potion (Red)": self.extract_icon(0, 80),
            "Potion (Blue)": self.extract_icon(16, 80),
            "Potion (Green)": self.extract_icon(32, 80),
            "Square Jar": self.extract_icon(48, 80),
            "Cake": self.extract_icon(0, 96),
            "Donut": self.extract_icon(16, 96),
            "Bread": self.extract_icon(32, 96),
            "Rug Tile": self.extract_icon(0, 112),
            "Geometric Pattern": self.extract_icon(16, 112),
            "Glowing Orb (Blue)": self.extract_icon(0, 128),
            "Glowing Orb (Red)": self.extract_icon(16, 128),
            "Glowing Orb (Green)": self.extract_icon(32, 128),
            "Golden Ring": self.extract_icon(48, 128),
            "Amulet": self.extract_icon(64, 128),
            "Scroll": self.extract_icon(0, 144),
            "Key": self.extract_icon(16, 144),
            "Tool": self.extract_icon(32, 144),
            "Dragon (Red)": self.extract_icon(0, 160),
            "Dragon (Green)": self.extract_icon(16, 160),
            "Dragon (Black)": self.extract_icon(32, 160),
            "Dragon (White)": self.extract_icon(48, 160),
            "Gem Cluster": self.extract_icon(0, 176),
            "Glowing Crystal": self.extract_icon(16, 176),
        }

        # Button dimensions
        self.button_width: int = 100
        self.button_height: int = 50

        # Initialize button actions
        self.button_actions: dict[str, tuple[pygame.Rect, pygame.Rect]] = {}

        # Action messages
        self.message: str = ""
        self.message_end_time: int = 0  # Time to display the message

    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle events like keypress or mouse wheel."""

        if event.type == pygame.MOUSEWHEEL:
            # Adjust scroll offset
            self.scroll_offset = max(0, self.scroll_offset - event.y)
            max_offset = max(0, len(self.inventory.get_items()) - self.max_visible_items)
            self.scroll_offset = min(self.scroll_offset, max_offset)

    def extract_icon(self, x: int, y: int, size: int = TILE_SIZE) -> pygame.Surface:
        """Extract a single icon from the sprite sheet."""

        return self.sprite_sheet.subsurface((x, y, size, size))

    def draw_buttons(self, x: int, y: int, item: str) -> tuple[pygame.Rect, pygame.Rect]:
        """Draw Use and Discard buttons for a specific item."""

        use_button: pygame.Rect = pygame.Rect(x, y, self.button_width, self.button_height)
        discard_button: pygame.Rect = pygame.Rect(x + self.button_width + 10, y, self.button_width, self.button_height)

        pygame.draw.rect(self.screen, (0, 255, 0), use_button)  # Green
        pygame.draw.rect(self.screen, (150, 75, 0), discard_button)  # Brown

        use_text: pygame.Surface = self.font.render("Use", True, (0, 0, 0))  # Black
        discard_text: pygame.Surface = self.font.render("Discard", True, (0, 0, 0))

        self.screen.blit(use_text, (x + 10, y + 10))
        self.screen.blit(discard_text, (x + self.button_width + 20, y + 10))

        return use_button, discard_button

    def draw(self) -> None:
        """Draw the inventory overlay."""

        self.screen.fill((0, 0, 0))  # Solid Black background

        # Reset button actions
        self.button_actions: dict[str, tuple[pygame.Rect, pygame.Rect]] = {}

        # Draw the inventory items
        items: list = list(self.inventory.get_items().items())
        visible_items: list = items[self.scroll_offset : self.scroll_offset + self.max_visible_items]
        y_offset: int = 50  # Start below the title

        for item, quantity in visible_items:
            # Draw icon
            if item in self.icons:
                self.screen.blit(self.icons[item], (50, y_offset))

            # Draw quantity next to the icon
            quantity_text = self.font.render(f"x{quantity}", True, (255, 255, 255))
            self.screen.blit(quantity_text, (100, y_offset + 5))

            # Draw item name (move text to the right)
            text = self.font.render(item, True, (255, 255, 255))
            self.screen.blit(text, (150, y_offset))

            # Draw buttons
            use_button, discard_button = self.draw_buttons(400, y_offset, item)

            # Store button references for event handling
            self.button_actions[item] = (use_button, discard_button)
            y_offset += 60  # Move down for the next item

        # Draw a hint
        hint_text = self.font.render("Press 'I' to close inventory", True, (200, 200, 200))  # Light gray text
        self.screen.blit(hint_text, (50, self.screen.get_height() - 60))

        # Display an action message above the hint
        if self.message and pygame.time.get_ticks() < self.message_end_time:
            # Render the message text
            message_text = self.font.render(self.message, True, (255, 255, 0))  # Yellow

            # Measure the message text size
            text_width, text_height = message_text.get_size()

            # Message background
            message_bg_x: int = 40
            message_bg_y: int = self.screen.get_height() - 120
            message_bg_width: int = text_width + 20  # Add padding
            message_bg_height: int = text_height + 10  # Add padding

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

    def handle_mouse_click(self, mouse_pos: tuple[int, int]) -> None:
        """Handle mouse clicks on buttons."""

        for item, (use_button, discard_button) in self.button_actions.items():
            if use_button.collidepoint(mouse_pos):
                self.message = self.inventory.use_item(item)  # `self.message` stores strings
                self.message_end_time = pygame.time.get_ticks() + 3000  # 3 seconds
            elif discard_button.collidepoint(mouse_pos):
                self.message = self.inventory.remove_item(item, 1)
                self.message_end_time = pygame.time.get_ticks() + 4000  # 4 seconds
