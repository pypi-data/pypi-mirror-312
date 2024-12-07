from typing import Any, Literal, NotRequired, TypedDict, cast

import gymnasium as gym
import numpy as np
import pygame
from gymnasium import error, spaces

from mrkwatkins.oakemu.zxspectrum import Deathchase, Game, GameResult, ManicMiner


def get_game(env: gym.Env) -> Game:
    if not isinstance(env.unwrapped, OakEmuEnv):
        raise ValueError("env.unwrapped is not an OakEmuEnv.")

    return cast(OakEmuEnv, env.unwrapped).game


class OakEmuEnvStepMetadata(TypedDict):
    frame_number: int
    seeds: NotRequired[tuple[int, int]]


class OakEmuEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    # TODO: Add frameskip, repeat_action_probability, in common with the Atari envs.
    # TODO: Increase variance as per https://github.com/ray-project/ray/blob/41be27c417480ebe7d457d219b79f53d957f1989/rllib/env/wrappers/atari_wrappers.py#L364
    def __init__(
        self,
        game_type: Literal["Deathchase", "ManicMiner"],
        obs_type: Literal["ram", "rgb", "spectrum"] = "spectrum",
        render_mode: Literal["human", "rgb_array"] | None = None,
    ):
        if game_type == "Deathchase":
            self.game = Deathchase()
        elif game_type == "ManicMiner":
            self.game = ManicMiner()
        else:
            raise error.Error(f"Invalid game_type: {game_type}. Expecting: Deathchase, ManicMiner.")

        if obs_type not in {"ram", "rgb", "spectrum"}:
            raise error.Error(f"Invalid obs_type: {obs_type}. Expecting: ram, rgb, spectrum.")

        if render_mode is not None and render_mode not in self.metadata["render_modes"]:
            raise error.Error(f"Invalid render_mode: {render_mode}. Expecting: human, rgb_array.")

        self._obs_type = obs_type
        self.render_mode = render_mode
        self._actions = list(self.game.actions)
        self.action_space = spaces.Discrete(len(self._actions))
        self.play_area_width = self.game.play_area.width
        self.play_area_height = self.game.play_area.height

        if obs_type == "ram":
            self.observation_space = spaces.Box(low=0, high=255, dtype=np.uint8, shape=(6912,))
        else:  # rgb or spectrum
            image_shape = (
                self.play_area_height,
                self.play_area_width,
            )
            if obs_type == "rgb":
                image_shape += (3,)
            self.observation_space = spaces.Box(low=0, high=255, dtype=np.uint8, shape=image_shape)

        if render_mode == "human":
            pygame.init()
            pygame.display.init()
            self._screen = pygame.display.set_mode((256, 192))
            self._clock = pygame.time.Clock()
        else:
            self._screen = None
            self._clock = None

        self._frame_number: int = 0

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, OakEmuEnvStepMetadata]:
        super().reset(seed=seed, options=options)

        self.game.start_episode()

        obs = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return obs, info

    def step(
        self,
        action: int | np.ndarray,
    ) -> tuple[np.ndarray, float, bool, bool, OakEmuEnvStepMetadata]:
        action_name = self._actions[action]

        step_result = self.game.execute_step(action_name)

        reward = step_result.score_increase
        is_terminal = step_result.result != GameResult.NONE
        is_truncated = False

        self._frame_number += 1

        if self.render_mode == "human":
            self.render()

        return self._get_obs(), reward, is_terminal, is_truncated, self._get_info()

    def _get_obs(self) -> np.ndarray:
        if self._obs_type == "spectrum":
            return self.game.get_play_area_pixel_colour_screenshot()
        elif self._obs_type == "rgb":
            return self.game.get_play_area_rgb_screenshot()
        else:
            return self.game.spectrum.get_screen()

    def _get_info(self) -> OakEmuEnvStepMetadata:
        return {
            "frame_number": self._frame_number,
        }

    def render(self) -> np.ndarray | None:
        screenshot = self.game.spectrum.get_rgb_screenshot()

        if self.render_mode == "rgb_array":
            return screenshot
        else:
            screenshot = np.rot90(screenshot)
            screenshot = np.flip(screenshot, axis=0)
            pygame.surfarray.blit_array(self._screen, screenshot)

            pygame.event.pump()
            self._clock.tick(50)
            pygame.display.flip()
            return

    def close(self):
        if self._screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()
