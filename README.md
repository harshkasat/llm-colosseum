# LLM Colosseum: A Head-to-Head LLM Competition Arena

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)


## 1. Project Overview

LLM Colosseum is a Python-based framework designed to pit two large language models (LLMs) against each other in a competitive environment.  It provides a structured way to evaluate and compare the performance of different LLMs across various tasks.  The framework facilitates the recording and analysis of game results, offering insights into the strengths and weaknesses of each competing model.


## 2. Key Features

* **Head-to-Head Competition:**  Allows two LLMs to compete in a defined game environment.
* **Customizable Game Logic:** The game's rules and objectives can be easily modified.
* **Model Agnostic:** Supports a wide range of LLMs through adaptable interfaces.  Currently supports models accessible via OpenAI, Ollama, Anthropic, and more.
* **Result Recording and Visualization:**  Tracks game progress and outcomes for analysis.  Includes a basic win screen visualization (result.py).
* **Extensible Architecture:** Designed for easy extension and addition of new game types and LLM integrations.


## 3. Table of Contents

* [Project Overview](#1-project-overview)
* [Key Features](#2-key-features)
* [Prerequisites](#4-prerequisites)
* [Installation](#5-installation-guide)
* [Configuration](#6-configuration)
* [Usage Examples](#7-usage-examples)
* [Project Structure](#8-project-architecture)
* [License](#17-license)


## 4. Prerequisites

* Python 3.8 or higher
* The libraries listed in `requirements.txt`.  You can install them using `pip install -r requirements.txt`.


## 5. Installation Guide

1. Clone the repository: `git clone https://github.com/harshkasat/llm-colosseum.git`
2. Navigate to the project directory: `cd llm-colosseum`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up your environment variables (see Configuration section).


## 6. Configuration

The project uses environment variables to configure the LLMs and game settings.  You'll need to create a `.env` file (example shown below) and set the API keys for your chosen LLMs.  The `demo.py`, `local.py`, and `script.py` files demonstrate different configuration examples.

**Example `.env` file:**

```
OPENAI_API_KEY=your_openai_api_key
# ... other API keys ...
```

## 7. Usage Examples

The project includes several example scripts demonstrating how to set up and run a game:

* **`demo.py`:** Runs a game with two "mistral:mistral small latest" models.
* **`local.py`:** Runs a game with two "ollama:qwen:14b chat v1.5 fp16" models.
* **`script.py`:** Runs a game with an "ollama:llama3" model against an "anthropic:claude 3 haiku 20240307" model.

These scripts showcase how to instantiate the `Game`, `Player1`, and `Player2` classes and run the competition.  The `eval/game.py` file contains the core game logic.  The specific game rules and interactions are defined within this file.


**Example Code Snippet (from `demo.py`):**

```python
game = Game(
    render=True,
    save_game=True,
    player_1=Player1(
        nickname="Baby",
        model="mistral:mistral small latest",
    ),
    player_2=Player2(
        nickname="Daddy",
        model="mistral:mistral small latest",
    ),
)
game.run()
```

## 8. Project Structure

The project is structured as follows:

* **`agent`:** Contains the code for interacting with the LLMs.  This includes classes for the LLM agent (`llm.py`), the game observer (`observer.py`), and the robot (agent that interacts with the game environment) (`robot.py`).
* **`eval`:** Contains the core game logic (`game.py`).
* **`requirements.txt`:** Lists project dependencies.
* **`demo.py`, `local.py`, `script.py`:** Example usage scripts.
* **`result.py`:** Simple win screen display using Tkinter and Pillow.


## 17. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


**Note:**  The provided code snippets and descriptions are based on the files available in the repository.  More detailed documentation within the code itself would improve the overall understanding and usability of the project.  The `eval/game.py` file, in particular, would benefit from comprehensive docstrings explaining the game logic and parameters.
