import os
import sys

# Add the project root to sys.path to allow imports to work when running tests directly with `python`.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest

from src.inventory import Chest, Inventory, Quest
from src.utils.messaging import get_message

# Old way of writing tests using unittest
# class TestInventory(unittest.TestCase):
#     def setUp(self):
#         """Set up a new Inventory object before each test."""
#         self.inventory = Inventory()

@pytest.fixture
def inventory():
    """Set up a new Inventory object before each test."""
    return Inventory()

# Test add_item
def test_add_item_new(inventory):
    """Test adding a new item."""
    result = inventory.add_item("Sword", 1)
    expected = get_message("inventory", "add_success", item="Sword", quantity=1)
    assert inventory.items == {"Sword": 1}
    assert result == expected

def test_add_item_existing(inventory):
    """Test adding to an existing item."""
    result = inventory.add_item("Potion", 2)
    expected = get_message("inventory", "add_success", item="Potion", quantity=2)
    assert inventory.items == {"Potion": 2}
    assert result == expected

# Test remove_item
def test_remove_item_success(inventory):
    """Test successfully removing an item."""
    inventory.add_item("Potion", 3)
    result = inventory.remove_item("Potion", 2)
    expected = get_message("inventory", "remove_success", item="Potion", quantity=2)
    assert inventory.items == {"Potion": 1}
    assert result == expected


def test_remove_item_fail(inventory):
    """Test failing to remove an item not in inventory or insufficient quantity."""
    result = inventory.remove_item("Sword", 1)
    expected = get_message("inventory", "remove_fail", item="Sword", quantity=1)
    assert inventory.items == {}
    assert result == expected

# Test use_item
def test_use_item_success(inventory):
    """Test using an item."""
    inventory.add_item("Potion", 1)
    result = inventory.use_item("Potion")
    expected = get_message("inventory", "use_success", item="Potion")
    assert inventory.items == {}
    assert result == expected

def test_use_item_fail(inventory):
    """Test failing to use an item."""
    result = inventory.use_item("Potion")
    expected = get_message("inventory", "use_fail", item="Potion")
    assert inventory.items == {}
    assert result == expected

# Test add_chest
def test_add_chest(inventory):
    """Test adding a chest."""
    chest = Chest("Gold Chest")
    inventory.add_chest(chest)
    assert len(inventory.chests) == 1
    assert inventory.chests[0].name == "Gold Chest"

# Test add_quest
def test_add_quest(inventory):
    """Test adding a quest."""
    quest = Quest()
    inventory.add_quest(quest)
    assert len(inventory.quests) == 1
    assert inventory.quests[0].completed == False

# Test get_items
def test_get_items(inventory):
    """Test getting a copy of items."""
    inventory.add_item("Sword", 1)
    items = inventory.get_items()
    assert items == {"Sword": 1}
    assert items is not inventory.items  # Copy of items

# Test get_chests
def test_get_chests(inventory):
    """Test getting a copy of chests."""
    chest = Chest("Gold Chest")
    inventory.add_chest(chest)
    chests = inventory.get_chests()
    assert len(chests) == 1
    assert chests[0].name == "Gold Chest"
    assert chests is not inventory.chests  # Copy of items

# Test get_quests
def test_get_quests(inventory):
    """Test getting a copy of quests."""
    quest = Quest()
    inventory.add_quest(quest)
    quests = inventory.get_quests()
    assert len(quests) == 1
    assert quests is not inventory.quests  # Copy of items
