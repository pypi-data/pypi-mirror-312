import json
from typing import Optional, List

import numpy as np

from hydtank.parameters import Parameters
from hydtank.statistics import Statistics


class BasinDef:
    def __init__(
            self, name: str,
            downstream: Optional['BasinDef'] = None,
            upstream: Optional[List['BasinDef']] = None,
    ):
        self._name = name
        self._parameters = Parameters()
        self._stats = Statistics()
        self._downstream = downstream
        self._upstream = [] if upstream is None else upstream
        self._q_sim: Optional[np.ndarray] = None

    def calculate_stats(self, q_obs: np.ndarray):
        self._stats.calculate_stats(q_obs, self._q_sim)

    def display(self, visited=None, level=0):
        if visited is None:
            visited = set()
        if self in visited:
            print('  ' * level + f"(Visited) {self._name}")
            return
        visited.add(self)

        print('  ' * level + f"{type(self).__name__}: {self._name}")

        if self._upstream:
            print('  ' * level + "Upstream:")
            for upstream in self._upstream:
                upstream.display(visited, level + 1)

        if self._downstream:
            print('  ' * level + "Downstream:")
            self._downstream.display(visited, level + 1)

    @property
    def name(self) -> str:
        return self._name

    @property
    def downstream(self) -> Optional['BasinDef']:
        return self._downstream

    @downstream.setter
    def downstream(self, value: Optional['BasinDef']):
        self._downstream = value

    @property
    def upstream(self) -> List['BasinDef']:
        return self._upstream

    @upstream.setter
    def upstream(self, value: List['BasinDef']):
        self._upstream = value

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value: Parameters):
        self._parameters = value

    @property
    def q_sim(self):
        return self._q_sim

    @property
    def stats(self):
        return self._stats

    def __str__(self):
        return json.dumps(
            {
                "Name": self.name,
                "Downstream": None if self._downstream is None else self._downstream.name,
                "Upstreams": [basin_def.name for basin_def in self._upstream],
                "Parameters": self._parameters.__dict__
            },
            indent=4
        )
