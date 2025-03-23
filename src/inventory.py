"""
inventory class for the players
this file contain types of items, like Chest
"""

from src.utils.messaging import get_message
from src.utils.currency import load_inventory, load_wallet, save_wallet


class Chest:
    """contain loot, and worth"""

    def __init__(self, name: str) -> None:
        self.name = name


class Quest:
    """TODO: make the docstrings"""

    def __init__(self) -> None:
        self.completed = False


class Inventory:
    """Manage player's inventory, including money, item, chests, and quests"""

    def __init__(self) -> None:
        # Currency
        self.money: int = 0
        self.wallet = load_wallet()
        self.price = load_inventory()
        self.player_wallet = self.wallet["player_wallet"]["quantity"]

        # Item management
        self.items: dict[str, int] = {}  # name: quantity

        # Special attributes:
        self.chests: list[Chest] = []
        self.quests: list[Quest] = []

    # General item management
    def add_item(self, item_name: str, quantity: int) -> str:
        """Add an item to the inventory"""
        if item_name in self.items:
            self.items[item_name] += quantity
            return get_message("inventory", "add_success", item=item_name, quantity=quantity)
        else:
            self.items[item_name] = quantity
            return get_message("inventory", "add_success", item=item_name, quantity=quantity)

    def remove_item(self, item_name: str, quantity: int) -> str:
        """Remove an item from the inventory. Return True if successful."""
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]
            return get_message("inventory", "remove_success", item=item_name, quantity=quantity)
        return get_message("inventory", "remove_fail", item=item_name, quantity=quantity)

    def use_item(self, item_name: str) -> str:
        """Use an item, applying its effect. Return a message."""
        if self.remove_item(item_name, 1) == get_message("inventory", "remove_success", item=item_name, quantity=1):
            return get_message("inventory", "use_success", item=item_name)
        return get_message("inventory", "use_fail", item=item_name)
    
    def buy_item(self, item_name, quantity):
        if item_name in self.items:
            self.items[item_name] += quantity
            self.player_wallet -= 50
            self.save_gold = save_wallet(self.player_wallet)
            return get_message("shop_inventory", "buy_success", item=item_name, quantity=quantity)
        else:
            self.items[item_name] = quantity
            return get_message("shop_inventory", "buy_success", item=item_name, quantity=quantity)

    def sell_item(self, item_name, quantity):
        if item_name in self.items and self.items[item_name] >= quantity:
            if "price" in self.price.get(item_name, {}):
                self.item_price = self.price[item_name]["price"]
                self.items[item_name] -= quantity
                self.player_wallet += self.item_price
                self.save_gold = save_wallet(self.player_wallet)
                if self.items[item_name] == 0:
                    del self.items[item_name]
                return get_message("shop_inventory", "sell_success", item=item_name, quantity=quantity)
        return get_message("shop_inventory", "sell_fail", item=item_name, quantity=quantity)

    def get_items(self) -> dict[str, int]:
        """Return a copy of the items dictionary."""
        return self.items.copy()
    
    def get_money(self):
        return self.money

    # Methods for Chest and Quest
    def add_chest(self, chest: Chest) -> None:
        """Add a chest to the inventory."""
        self.chests.append(chest)

    def get_chests(self) -> list[Chest]:
        """Return a copy of the chests list."""
        return self.chests.copy()

    def add_quest(self, quest: Quest) -> None:
        """Add a quest to the inventory."""
        self.quests.append(quest)

    def get_quests(self) -> list[Quest]:
        """Return a copy of the quests list."""
        return self.quests.copy()
