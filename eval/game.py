from typing import List, Optional, Union
from diambra.arena import (
    SpaceTypes,
    EnvironmentSettingsMultiAgent,
    make,
    RecordingSettings,
)
import os
import datetime

from agent import Robot, KEN_RED, KEN_GREEN


class Player:
    nickname: str
    model: str
    robot: Optional[Robot] = None


class Player1(Player):
    def __init__(self, nickname: str, model: str):
        self.nickname = nickname
        self.model = model
        self.robot = Robot(
            action_space=None,
            character="Ken",
            side=0,
            character_color=KEN_RED,
            ennemy_color=KEN_GREEN,
        )


class Player2(Player):
    def __init__(self, nickname: str, model: str):
        self.nickname = nickname
        self.model = model
        self.robot = Robot(
            action_space=None,
            character="Ken",
            side=1,
            character_color=KEN_GREEN,
            ennemy_color=KEN_RED,
        )


class Game:
    render: Optional[bool] = False
    splash_screen: Optional[bool] = False
    save_game: Optional[bool] = False
    characters: Optional[List[str]] = ["Ken", "Ken"]
    outfits: Optional[List[int]] = [1, 3]
    frame_shape: Optional[List[int]] = [0, 0, 0]
    seed: Optional[int] = 42
    settings: EnvironmentSettingsMultiAgent = None  # Settings of the game
    env = None  # Environment of the game
    player_1: Player1 = None  # First player
    player_2: Player2 = None  # Second player

    def __init__(
        self,
        render: bool = False,
        save_game: bool = False,
        splash_screen: bool = False,
        characters: List[str] = ["Ken", "Ken"],
        outfits: List[int] = [1, 3],
        frame_shape: List[int] = [0, 0, 0],
        seed: int = 42,
        player_1: Player1 = None,
        player_2: Player2 = None,
    ):
        """_summary_

        Args:
            render (bool, optional): Renders the fights. Defaults to False.
            splash_screen (bool, optional): Display the splash screen. Defaults to False.
            characters (List[str], optional): List of the players to have. Defaults to ["Ryu", "Ken"].
            outfits (List[int], optional): Outfits to run. Defaults to [2, 2].
            frame_shape (List[int], optional): Don't know :D . Defaults to [0, 0, 0].
            seed (int, optional): Random seed. Defaults to 42.
        """
        self.render = render
        self.splash_screen = splash_screen
        self.save_game = save_game
        self.characters = characters
        self.outfits = outfits
        self.frame_shape = frame_shape
        self.seed = seed
        self.settings = self._init_settings()
        self.env = self._init_env(self.settings)
        self.observation, self.info = self.env.reset(seed=self.seed)
        self.player_1 = (
            player_1 if player_1 else Player1(nickname="Player 1", model="llm")
        )
        self.player_2 = (
            player_2 if player_2 else Player2(nickname="Player 2", model="llm")
        )

    def _init_settings(self) -> EnvironmentSettingsMultiAgent:
        """
        Initializes the settings for the game.
        """
        settings = EnvironmentSettingsMultiAgent(
            render_mode="rgb_array",
            splash_screen=self.splash_screen,
        )

        settings.action_space = (SpaceTypes.DISCRETE, SpaceTypes.DISCRETE)

        settings.characters = self.characters

        settings.outfits = self.outfits

        settings.frame_shape = self.frame_shape

        return settings

    def _init_recorder(self) -> RecordingSettings:
        """
        Initializes the recorder for the game.
        """
        if not self.save_game:
            return None
        # Recording settings in root directory
        root_dir = os.path.dirname(os.path.abspath(__file__))
        game_id = "sfiii3n"
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        recording_settings = RecordingSettings()
        recording_settings.dataset_path = os.path.join(
            root_dir, "diambra/episode_recording", game_id, "-", timestamp
        )
        recording_settings.username = "llm-colosseum"

        return recording_settings

    def _init_env(self, settings: EnvironmentSettingsMultiAgent):
        """
        Initializes the environment for the game.
        """
        render_mode = "human" if self.render else "rgb_array"
        recorder_settings = self._init_recorder()
        if self.save_game:
            return make(
                "sfiii3n",
                settings,
                render_mode=render_mode,
                episode_recording_settings=recorder_settings,
            )
        return make("sfiii3n", settings, render_mode=render_mode)

    def _save(self):
        """
        Save the game state.
        """
        pass

    def run(self):
        """
        Runs the game with the given settings.
        """

        self.player_1.robot.observe(self.observation, {})
        self.player_2.robot.observe(self.observation, {})

        while True:
            if self.render:
                self.env.render()

            # Plan
            self.player_1.robot.plan()
            self.player_2.robot.plan()

            # Act
            actions = {
                "agent_0": self.player_1.robot.act(),
                "agent_1": self.player_2.robot.act(),
            }
            print("Actions: {}".format(actions))
            # Execute actions in the game
            observation, reward, terminated, truncated, info = self.env.step(actions)

            done = terminated or truncated
            print("Reward: {}".format(reward))
            print("Done: {}".format(done))
            print("Info: {}".format(info))

            if done:
                # Optionally, change episode settings here
                options = {}
                options["characters"] = (None, None)
                options["char_outfits"] = (5, 5)
                observation, info = self.env.reset(options=options)
                break

            # Observe the environment
            self.player_1.robot.observe(observation, actions)
            self.player_2.robot.observe(observation, actions)
        self.env.close()
        return 0
