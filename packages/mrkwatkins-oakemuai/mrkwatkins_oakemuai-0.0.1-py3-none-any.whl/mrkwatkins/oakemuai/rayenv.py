from collections import deque

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from ray import tune
from ray.rllib.utils.images import resize

from mrkwatkins.oakemuai.oakemuenv import OakEmuEnv

# TODO: Custom metrics for game properties such as score, air_supply, etc. https://docs.ray.io/en/latest/rllib/rllib-advanced-api.html


class FrameStack(gym.Wrapper):
    def __init__(self, env, k):
        """Stack k last frames."""
        gym.Wrapper.__init__(self, env)
        self.k = k
        self.frames = deque([], maxlen=k)
        shp = env.observation_space.shape
        self.observation_space = spaces.Box(
            low=np.repeat(env.observation_space.low, repeats=k, axis=-1),
            high=np.repeat(env.observation_space.high, repeats=k, axis=-1),
            shape=(shp[0], shp[1], shp[2] * k),
            dtype=env.observation_space.dtype,
        )

    def reset(self, *, seed=None, options=None):
        ob, infos = self.env.reset(seed=seed, options=options)
        for _ in range(self.k):
            self.frames.append(ob)
        return self._get_ob(), infos

    def step(self, action):
        ob, reward, terminated, truncated, info = self.env.step(action)
        self.frames.append(ob)
        return self._get_ob(), reward, terminated, truncated, info

    def _get_ob(self):
        assert len(self.frames) == self.k
        return np.concatenate(self.frames, axis=2)


class MaxAndSkipEnv(gym.Wrapper):
    def __init__(self, env, skip=4):
        """Return only every `skip`-th frame"""
        gym.Wrapper.__init__(self, env)
        # most recent raw observations (for max pooling across time steps)
        self._obs_buffer = np.zeros((2,) + env.observation_space.shape, dtype=env.observation_space.dtype)
        self._skip = skip

    def step(self, action):
        """Repeat action, sum reward, and max over last observations."""
        total_reward = 0.0
        terminated = truncated = info = None
        for i in range(self._skip):
            obs, reward, terminated, truncated, info = self.env.step(action)
            if i == self._skip - 2:
                self._obs_buffer[0] = obs
            if i == self._skip - 1:
                self._obs_buffer[1] = obs
            total_reward += reward
            if terminated or truncated:
                break
        # Note that the observation on the terminated|truncated=True frame
        # doesn't matter
        max_frame = self._obs_buffer.max(axis=0)

        return max_frame, total_reward, terminated, truncated, info

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)


class NoopResetEnv(gym.Wrapper):
    def __init__(self, env, noop_max=5):
        """Sample initial states by taking random number of no-ops on reset.
        No-op is assumed to be action 0.
        """
        gym.Wrapper.__init__(self, env)
        self.noop_max = noop_max
        self.override_num_noops = None
        self.noop_action = 0

    def reset(self, **kwargs):
        """Do no-op action for a number of steps in [1, noop_max]."""
        self.env.reset(**kwargs)
        noops = self.override_num_noops if self.override_num_noops is not None else self.unwrapped.np_random.integers(1, self.noop_max + 1)

        assert noops > 0
        obs = None
        for _ in range(noops):
            obs, _, terminated, truncated, info = self.env.step(self.noop_action)
            if terminated or truncated:
                obs, info = self.env.reset(**kwargs)
        return obs, info

    def step(self, ac):
        return self.env.step(ac)


class NormalizedImageEnv(gym.ObservationWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.observation_space = gym.spaces.Box(
            -1.0,
            1.0,
            shape=self.observation_space.shape,
            dtype=np.float32,
        )

    # Divide by scale and center around 0.0, such that observations are in the range
    # of -1.0 and 1.0.
    def observation(self, observation):
        return (observation.astype(np.float32) / 128.0) - 1.0


class WarpFrame(gym.ObservationWrapper):
    def __init__(self, env, width, height):
        """Warp frames to the specified size (dim x dim)."""
        gym.ObservationWrapper.__init__(self, env)
        self.width = width
        self.height = height
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 1), dtype=np.uint8)

    def observation(self, frame):
        # frame = rgb2gray(frame)
        frame = resize(frame, height=self.height, width=self.width)
        return frame[:, :, None]


def _wrap_oak_emu_env(env: OakEmuEnv, dim: int = 64, frameskip: int = 4, framestack: int | None = None) -> gym.Env:
    # width = env.play_area_width
    # height = env.play_area_height

    env = gym.wrappers.TimeLimit(env, max_episode_steps=108000)

    # env = WarpFrame(env, width, height)
    env = WarpFrame(env, dim, dim)

    env = NormalizedImageEnv(env)

    if frameskip > 1:
        assert env.spec is not None
        env = MaxAndSkipEnv(env, skip=frameskip)
    # Send n noop actions into env after reset to increase variance in the
    # "start states" of the trajectories. These dummy steps are NOT included in the
    # sampled data used for learning.
    env = NoopResetEnv(env, noop_max=30)

    # Framestack.
    if framestack:
        env = FrameStack(env, k=framestack)
    return env


def _env_creator(cfg):
    return _wrap_oak_emu_env(
        OakEmuEnv(**cfg),
        # Perform frame-stacking through ConnectorV2 API.
        framestack=None,
        frameskip=1,
    )


def register_env():
    tune.register_env("OakEmu", _env_creator)
