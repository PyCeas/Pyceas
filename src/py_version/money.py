""" handle the money system of the game """
from dataclasses import dataclass


@dataclass
class Money:
    """The money class should be called something else perhaps, we should"""

    currency: str
    worth: int
    max_worth: int = 1500000
    # self.purchase = basic_quest

    def buy(self, purchase_amount) -> None:
        """ remove some money from self.worth """
        self.worth -= purchase_amount
        self.worth = max(self.worth, 0)

    def buy_quest(self, quest) -> None:
        """ wrapper aroud buy for quests """
        if self.worth >= quest.quest_worth:
            print(
                f"You have purchesed {quest.name} for {quest.quest_worth} {self.currency}"
            )
            self.buy(quest.quest_worth)
        else:
            print("You don't have enough gold to buy a quest!")

    def sell(self, sell_amount) -> None:
        """ add money to worth """
        self.worth += sell_amount

    def sell_chest(self, chest) -> None:
        """ wrapper around sell for chests """
        if self.worth <= chest.chest_worth and self.worth >= chest.chest_worth:
            print(f"You sold {chest.name} for {chest.chest_worth} {self.currency}")
            self.sell(chest.chest_worth)
        else:
            print("You don't have the items to sell!")

    def show_money(self) -> None:
        """ print how much money do you have """
        print(f"You have now an impressive amount of {self.worth} {self.currency}")
