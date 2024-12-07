from collections.abc import Sequence
from typing import NamedTuple

import gymnasium as gym


class EnvConfig(NamedTuple):
    version: str


def register_envs(games: Sequence[str], configs: Sequence[EnvConfig]):
    for game in games:
        for config in configs:
            gym.register(
                id=f"{game}-{config.version}",
                entry_point="mrkwatkins.oakemuai.oakemuenv:OakEmuEnv",
                kwargs=dict(
                    game_type=game,
                    obs_type="spectrum",
                ),
            )


def register():
    games = ["Deathchase", "ManicMiner"]
    versions = [EnvConfig(version="v0")]

    register_envs(games, versions)


registered = False


def ensure_registered():
    global registered
    if not registered:
        register()
        registered = True
