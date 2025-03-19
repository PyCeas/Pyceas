"""Project Name: PyCeas
Description: PyCeas is an open-source project to create an engaging board game in Python,
inspired by Sea of Thieves. Ideal for game development enthusiasts and Python programmers
Author(s): Danilo Saiu (https://www.github.com/ultimateownsz),
Davit Alsemgeest (https://www.github.com/davidek523)
Date: 2024-09-08

Cli Version: 1.0.0
Pygame Version: 0.0.1"""

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# import Pygame specific objects, functions and functionality
from src.game_manager import GameStateManager

if __name__ == "__main__":
    game = GameStateManager()
    game.run()
