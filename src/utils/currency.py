import json

def load_wallet():
    with open("wallet.json", "r") as file:
        return json.load(file)

def save_wallet(wallet_data):
    with open("wallet.json", "w") as file:
        return json.dump(wallet_data, file, indent=4)

def load_inventory():
    with open("inventory.json", "r") as file:
        return json.load(file)