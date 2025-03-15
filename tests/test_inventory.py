import os
import sys

# Add the project root to sys.path to allow imports to work when running tests directly with `python`.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest

from src.inventory import Chest, Inventory, Quest


class TestInventory(unittest.TestCase):
    def setUp(self):
        """Set up a new Inventory object before each test."""
        self.inventory = Inventory()

    # Test add_item
    def test_add_item_new(self):
        """Test adding a new item."""
        result = self.inventory.add_item("Sword", 1)
        self.assertEqual(self.inventory.items, {"Sword": 1})
        self.assertEqual(result, "Successfully added 1 Sword(s) to your inventory.")

    def test_add_item_existing(self):
        """Test adding to an existing item."""
        self.inventory.add_item("Potion", 1)
        result = self.inventory.add_item("Potion", 2)
        self.assertEqual(self.inventory.items, {"Potion": 3})
        self.assertEqual(result, "Successfully added 2 Potion(s) to your inventory.")

    # Test remove_item
    def test_remove_item_success(self):
        """Test successfully removing an item."""
        self.inventory.add_item("Potion", 3)
        result = self.inventory.remove_item("Potion", 2)
        self.assertEqual(self.inventory.items, {"Potion": 1})
        self.assertEqual(result, "Successfully removed 2 Potion(s) from your inventory.")

    def test_remove_item_fail(self):
        """Test failing to remove an item not in inventory or insufficient quantity."""
        result = self.inventory.remove_item("Sword", 1)
        self.assertEqual(self.inventory.items, {})
        self.assertEqual(result, "Cannot remove 1 Sword(s), insufficient quantity.")

    # Test use_item
    def test_use_item_success(self):
        """Test using an item."""
        self.inventory.add_item("Potion", 1)
        result = self.inventory.use_item("Potion")
        self.assertEqual(self.inventory.items, {})
        self.assertEqual(result, "You used Potion.")

    def test_use_item_fail(self):
        """Test failing to use an item."""
        result = self.inventory.use_item("Potion")
        self.assertEqual(self.inventory.items, {})
        self.assertEqual(result, "You dont' have Potion in your inventory.")

    # Test add_chest
    def test_add_chest(self):
        """Test adding a chest."""
        chest = Chest("Gold Chest")
        self.inventory.add_chest(chest)
        self.assertEqual(len(self.inventory.chests), 1)
        self.assertEqual(self.inventory.chests[0].name, "Gold Chest")

    # Test add_quest
    def test_add_quest(self):
        """Test adding a quest."""
        quest = Quest()
        self.inventory.add_quest(quest)
        self.assertEqual(len(self.inventory.quests), 1)
        self.assertFalse(self.inventory.quests[0].completed)

    # Test get_items
    def test_get_items(self):
        """Test getting a copy of items."""
        self.inventory.add_item("Sword", 1)
        items = self.inventory.get_items()
        self.assertEqual(items, {"Sword": 1})
        self.assertIsNot(items, self.inventory.items)  # Copy of items

    # Test get_chests
    def test_get_chests(self):
        """Test getting a copy of chests."""
        chest = Chest("Gold Chest")
        self.inventory.add_chest(chest)
        chests = self.inventory.get_chests()
        self.assertEqual(len(chests), 1)
        self.assertIsNot(chests, self.inventory.chests)  # Copy of items

    # Test get_quests
    def test_get_quests(self):
        """Test getting a copy of quests."""
        quest = Quest()
        self.inventory.add_quest(quest)
        quests = self.inventory.get_quests()
        self.assertEqual(len(quests), 1)
        self.assertIsNot(quests, self.inventory.quests)  # Copy of items


if __name__ == "__main__":
    unittest.main()
