import json


def load_wallet():
    with open("data/wallet.json", "r") as file:
        return json.load(file)


def save_wallet(player_wallet):
    wallet_data = {"player_wallet": {"quantity": player_wallet}}
    with open("data/wallet.json", "w") as file:
        return json.dump(wallet_data, file, indent=4)


def load_inventory():
    with open("data/inventory.json", "r") as file:
        return json.load(file)
