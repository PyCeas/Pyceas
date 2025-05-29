## Inventory Guide (GUI Version)

### Description of the Inventory GUI
The Inventory GUI serves as a user-friendly interface for managing in-game items. It allows players to view, interact with, and organize their inventory. 

[![PyCeas-inventory.png](https://i.postimg.cc/G3ZXHdnK/PyCeas-inventory.png)](https://postimg.cc/14rGdxtV)

### Key Features
- **Visual Display**: Items are displayed as icon, also providing name and quantity.
- **Responsive Interaction**: Interactive buttons for using, or discarding items.
- **Dynamic Updates**: Changes are reflected in real time.
- **Real Time Message Feedback**: Display message actions for better user experience. *(Refer to [utils](./UtilsGuide) for more details.)*

[![use-item.png](https://i.postimg.cc/9fK7JXpN/use-item.png)](https://postimg.cc/Y4N0SHT1)
[![remove-item.png](https://i.postimg.cc/QCkK8QrR/remove-item.png)](https://postimg.cc/H8nk37n2)

## Controls Documentation

### Controls Summary
- **Keyboard**: Press `I` to toggle the inventory screen on and off.
- **Mouse**: Click buttons to perform actions.

## Running Tests
Tests in this project use `pytest`. To run the tests:
`pytest tests/test_inventory.py`

## Testing Items

### Modifying `inventory.json`
The `data/inventory.json` file controls the data for all items in the inventory. It can be modified for testing purposes as follows:

1. Open the `inventory.json` file.
2. Add, remove, or edit item entries using the following format:
   ```json
   {
        ...
       "Gold Coin": {"type": "currency", "effect": "collect", "quantity": 1},
       ...
   }
   ```

## Key Properties

Each item in the inventory has the following properties:

- **`type`**: The classification of the item (e.g., `weapon`, `potion`, `material`).
- **`effect`**: The functional impact of the item (e.g., `damage`, `healing`, `crafting material`).
- **`quantity`**: The number of instances available for the item.

## Working with icons

### Adding a New Item Icon
To add a new item icon to the inventory:

1. Open `src/GUI/inventory_gui.py`.
2. Locate the initializer method (`self.icons: {}`).
3. Map the item name in `inventory.json` to the icon's location in the spritesheet. Use the following format:

```python
    "Gold Coin": self.extract_icon(0, 0),
```

[![icons-inventory-gui.png](https://i.postimg.cc/CMNKKL8T/icons-inventory-gui.png)](https://postimg.cc/231YcYT2)

4. Test the new item in-game to verify functionality and ensure no errors occur.

## Known Issues

1. Icons Mapping: Placeholder icons are used for certain items as not all of them 
accurately represent the icon they are linked to. 
