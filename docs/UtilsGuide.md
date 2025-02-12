# UtilsGuide.md

## Utility: `messaging.py`

This utility module provides functionality for retrieving and formatting messages stored in a centralized JSON file. It simplifies message management and allows for better modularity, multi-language support, and scalability across the game.

---

### File: `src/utils/messaging.py`

#### Function: `get_message(category: str, key: str, **kwargs) -> str`

Retrieve and format a message from a JSON file located at `data/messages.json`.

**Parameters:**
- `category` (`str`): The category of the message (e.g., `"inventory"`).
- `key` (`str`): The specific key for the desired message (e.g., `"add_success"`).
- `**kwargs`: Dynamic keyword arguments for formatting placeholders in the message.

**Returns:**
- The formatted message string from the JSON file.
- If the message is not found or the file is missing, a default error message is returned: `"An error occurred while retrieving the message."`

### Usage Examples

[![utils-usage.png](https://i.postimg.cc/MHvbCbWH/utils-usage.png)](https://postimg.cc/WqckrZqc)

## Possible Expansion
The messaging.py utility can be expanded to other areas of the game, including:

- Multi-language support by replacing or extending data/messages.json with localized versions.
- General feedback and logging, ensuring consistency across UI and gameplay mechanics.
- Integration with game state management for dynamic message generation.

## Best Practices
### Error Handling:

- Ensure data/messages.json is correctly formatted and accessible.
- Validate category and key inputs to avoid KeyError.

- Message Consistency:
  - Keep all game-related messages in the JSON file for easier updates and consistency.

- Localization:
  - Prepare data/messages.json to support multi-language keys for localization, e.g., en, es, ko.