# PyCeas - Open Source Pirate (Adventure) Board Game

[![Discord](https://discord.com/api/guilds/1272287320934056066/widget.png)](https://discord.gg/s2P9fZbeZs)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://www.freecodecamp.org/news/how-to-make-your-first-pull-request-on-github-3/)
[![License](https://img.shields.io/github/license/PyCeas/PyCeas)](https://github.com/PyCeas/Pyceas/blob/main/LICENSE)

## Table of Contents
- [PyCeas - Open Source Pirate (Adventure) Board Game](#pyceas---open-source-pirate-adventure-board-game)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Game Design Document](#game-design-document)
  - [Why Join PyCeas?](#why-join-pyceas)
  - [Getting Started](#getting-started)
    - [Clone the Repository](#clone-the-repository)
    - [Install Python](#install-python)
    - [Set up a virtual environment](#set-up-a-virtual-environment)
    - [Install Required Software](#install-required-software)
    - [Run the project](#run-the-project)
    - [Deactivate the Virtual Environment:](#deactivate-the-virtual-environment)
  - [Reporting bugs \& requesting features](#reporting-bugs--requesting-features)
    - [Local Development](#local-development)
    - [Linting and Formatting for developers](#linting-and-formatting-for-developers)
  - [License](#license)
    - [Why we chose AGPL](#why-we-chose-agpl)
  - [Relevant Links](#relevant-links)

## Project Description

PyCeas is an opensource project that aims to create a 2D, top down, turn based board game in Pygame. Where players become pirates and control their own ship. Using a card-based dice system, players explore a dynamic map, complete quests, and battle rival pirates. This game is designed to be engaging and using interactive elements using tools called Python and Pygame-CE, but you don't need to be a programmer to get involved or enjoy it!

> If you like the project, but just don't have time to contribute, that's fine. You could help us out to show support and appreciation of the project by:
> - 🌟 Starring the project
> - 🗣️ Sharing it on social media or at meetups.
> - 📄 Mention the project in your own repositories or documentation.

## Game Design Document
Every game needs thorough documentation, and you can find our Game Design Document (GGD) [here](./docs/Game%20Design%20Document/GGD.md).

## Why Join PyCeas?

- **Increasing your skills**: Learn and improve your Python and Pygame skills through practical, hands-on development.
- **Learn about game development**: Explore the world of game development and design, gaining valuable experience along the way.
- **Create something enjoyable**: Contributing to a project that results in a game you and others can enjoy.
- **Join our community on [Discord](https://discord.gg/MZ5MHqDnGW)**: Whether you want to help with ideas, give feedback, or simply enjoy the game, everyone is welcome!

> [!NOTE]
>
> This project was previously known as **PySeas** and has been renamed to **PyCeas**.
> If you have already cloned the repository under the old name, update your local repository’s remote URL:
>
> ```
> git remote set-url origin https://github.com/PyCeas/Pyceas.git
> ```

## Getting Started

No need to worry if you are new to programming. This guide will walk you through the setup step by step. by the end, you'll have everything ready to run the PyCeas project.


### Clone the Repository
First you'll need to copy the PyCeas project to your computer through a process called "cloning".
```
  git clone https://github.com/PyCeas/Pyceas.git

```

### Install Python
Check if Python is installed on your system. You can check by running the following command in your terminal prompt: 

- ##### For Mac Users:
  1. Open the terminal and install Python using `Homebrew`. If Homebrew is not installed, [follow these instructions](https://brew.sh/):
  ```bash
  brew install python3
  ```
  1. After installation, verify it by running:
  ```bash
  python3 --version
  ```

- ##### For Linux Users
  1. Open the terminal and update your package list:
  ```bash
  sudo apt update
  ```
  2. Install Python
  ```bash
  sudo apt install python3
  ```
  3. After installation, verify it by running:
  ```bash
  python3 --version
  ```

- ##### For Windows Users
  1. Download the Python installer from the [official Python website](https://www.python.org/downloads/).
  2. Run the installer and follow the on-screen instructions.
  3. Make sure to check the box "Add Python to PATH" before clicking "Install Now".
  4. After installation, verify by running:
  ```bash
  python --version
  ```


### Set up a virtual environment
A virtual environment is like a seperate space on your computer where you can install the software needed for this project without affecting other programs.

- ##### For Mac or Linux Users:
  - In your terminal, navigate to the folder where you downloaded the project (usually the 'PyCeas' folder) using the 'cd' command:
    ```bash
    cd PyCeas
    ```
  - Set up the virtual environment by typing: 
    ```bash
    python3 -m venv venv
    ```
  - Activate the virtual environment:
     ```bash
     source venv/bin/activate
     ```

- ##### For Windows Users:
    - Open Command Prompt and navigate to the 'PyCeas' folder (where you downloaded the project) using the 'cd' command:
    ```bash
    cd PyCeas
    ```
    - Set up the virtual environment by typing:
    ```bash
    python -m venv venv
    ```
    - Activate the virtual environment:
    ```bash
    venv\Scripts\activate
    ```
  
### Install Required Software
Now, you'll need to install the necessary software that the project depends on.
  - Make sure you're still in the 'PyCeas' directory/folder and that the virtual environment is active.
  - Install the software by typing the following command:
  ```bash
  pip install -r requirements.txt # For running the game (runtime dependencies)
  ```
This installs everything you need to run the project.
  - If you plan to do any local development or modifications, also run:
  ```bash
  pip install -r requirements_dev.txt # For local development
  ```

This step is optional and only needed if you want to make changes to the project.
### Run the project
Now you are ready to start the project!
  - Simply type:
  ```bash
  python main.py
  ```
  - The project should start running, and you'll see it in action!

### Deactivate the Virtual Environment:
When you’re done working, you can deactivate the virtual environment using:
```bash
deactivate
```

## Reporting bugs & requesting features
If you find something that's not working right or have an idea to make our project better, you can let us know by opening an `Issue` here on [Github](https://github.com/PyCeas/Pyceas/issues). An issue is just a way to tell us about a problem or suggest a new feature.

We use [Github Projects](https://github.com/orgs/PyCeas/projects/3) to organize and keep track of these issues, so we can make sure everything gets the attention it needs.

Before submitting an issue, check out our **[Contributor Guide](https://github.com/PyCeas/.github/blob/main/.github/ISSUE_TEMPLATE/contributor_guide.md)** for detailed instructions on:
- **Reporting Bugs:** Learn how to describe issues effectively to help us resolve them quickly.
- **Proposing Enhancements:** Follow our steps to suggest features and improvements.

If you need more help or want to talk about it, you can join our [Discord](https://discord.gg/MZ5MHqDnGW) community. We're here to chat and help you out!


### Local Development
[See how to contribute](./CONTRIBUTING.md)

### Linting and Formatting for developers
We chose to use [Ruff](https://docs.astral.sh/ruff/) to automatically lint and format the code. `Run pip install -r requirements_dev.txt` to install Ruff and other relevant dependencies.

> [!IMPORTANT]
> **Before you open a Pull Request, please run this bash commands to format your code properly and doesn't upset our linter:**
>
> 
> ```sh
> ruff format . && ruff check --include I --fix . # this formats code and sort imports
> ruff check . # run linting and perform fixes
> mypy main.py
> ```
>
> **If you use powershell, run these commands:**
>
> ```powershell
> ruff format .;
> ruff check --include I --fix .;
> ruff check .;
> mypy main.py
> ```

## License

This project is licensed under the terms of the **[AGPL-3.0 License](/LICENSE)**.

### Why we chose AGPL

We aim to create a game that is not only fun but also like we mentioned before open source and community-driven. Here's why we chose the **AGPL-3.0 License** for our project:

1. **Focus on Local Gameplay First**
   Our primary goal is to create a fully functional local game that anyone can play. This our starting point, ensuring a solid foundation before we expand the game further.

2. **Future Multiplayer Features**
   Once the local gameplay is polished, we plan to introduce multiplayer functionality. This will include the ability to host your own game servers, opening up more possibilities for collaborative and competitive gameplay.

3. **Modding Capabilities / Expansions**
   We want PyCeas to be mod-friendly, allowing players and developers to customize and expand the game to suit their preferences. This flexibility ensures that the game evolves trough community contributions.

4. **Why AGPL?**
   - The AGPL ensures that the code remains accessible to everyone, even when the game is modified or hosted on private servers.
   - Any changes made to the game whether as forks or additions must be shared under the same license, making them available to anyone who wants to contribute.
   - By using AGPL, we protect the game's openness and ensure that it stays true to the vision of collaborative, community-driven project.

In short, the AGPL aligns perfectly with our commitments to openness, community collaboration, and the long-term growth of PyCeas as both game and an opensource project.


## Relevant Links
- [Project Task List](https://github.com/orgs/PyCeas/projects/3)
- [GitHub discussions](https://github.com/PyCeas/Pyceas/discussions)
- [PyCeas's Discord Server](https://discord.gg/MZ5MHqDnGW)
- [Pygame's Community Discord](https://discord.gg/pygame)
