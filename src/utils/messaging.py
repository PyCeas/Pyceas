import json


def get_message(category: str, key: str, **kwargs) -> str:
    """Retrieve and format a message from the JSON file."""
    try:
        with open("data/messages.json", "r") as f:
            messages = json.load(f)
        message = messages[category][key]
        return message.format(**kwargs)
    except (KeyError, FileNotFoundError):
        return "An error occurred while retrieving the message."
