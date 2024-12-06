import dataclasses
import json

import numpy as np


def mse(x: np.ndarray, y: np.ndarray):
    return ((x - y) ** 2).sum() / x.shape[0]


def rmse(x: np.ndarray, y: np.ndarray):
    return np.sqrt(mse(x, y))


def nse(sim: np.ndarray, obs: np.ndarray):
    obs_mean = obs.mean()
    return 1 - (np.square(obs - sim).sum() / np.square(obs - obs_mean).sum())


def r2(x: np.ndarray, y: np.ndarray):
    n = x.shape[0]

    nu = (n * ((x * y).sum()) - (x.sum()) * (y.sum())) ** 2
    de = (n * ((x ** 2).sum()) - (x.sum()) ** 2) * (n * ((y ** 2).sum()) - (y.sum()) ** 2)

    return nu / de


def pbias(obs: np.ndarray, sim: np.ndarray):
    return (obs - sim).sum() * 100 / obs.sum()


@dataclasses.dataclass
class Statistics:
    rmse: float = None
    nse: float = None
    r2: float = None
    pbias: float = None

    def calculate_stats(self, q_obs: np.ndarray, q_sim: np.ndarray):
        self.rmse = rmse(q_obs, q_sim)
        self.nse = nse(q_sim, q_obs)
        self.r2 = r2(q_sim, q_obs)
        self.pbias = pbias(q_sim, q_obs)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
