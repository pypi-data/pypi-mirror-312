import copy
import dataclasses
import json
from abc import ABC

import numpy as np


class Parameters(ABC):
    @staticmethod
    def get_bounds():
        pass

    def to_initial_params(self):
        pass

    def from_params(self, params):
        field_names = [field.name for field in dataclasses.fields(self)]
        bounds = self.get_bounds()

        for i, (name, bound) in enumerate(zip(field_names, bounds)):
            value = params[i]
            if not (bound[0] <= value <= bound[1]):
                raise ValueError(f"Value {value} for '{name}' is out of bounds {bound}")
            setattr(self, name, value)

        self.validate()

    def validate(self):
        params = self.to_initial_params()
        field_names = [field.name for field in dataclasses.fields(self)]

        for i, (param, bound) in enumerate(zip(params, self.get_bounds())):
            if not (bound[0] <= param <= bound[1]):
                raise ValueError(f"Attribute '{field_names[i]}' with value {param} is out of bounds {bound}")

    def copy(self):
        return copy.deepcopy(self)

    def __post_init__(self):
        self.validate()

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)


@dataclasses.dataclass
class SubbasinParameters(Parameters):
    t0_is: float = 0.01
    t0_boc: float = 0.1
    t0_soc_uo: float = 0.1
    t0_soc_lo: float = 0.1
    t0_soh_uo: float = 75.0
    t0_soh_lo: float = 0.0
    t1_is: float = 0.01
    t1_boc: float = 0.01
    t1_soc: float = 0.01
    t1_soh: float = 0.0
    t2_is: float = 0.01
    t2_boc: float = 0.01
    t2_soc: float = 0.01
    t2_soh: float = 0.0
    t3_is: float = 0.01
    t3_soc: float = 0.01

    @staticmethod
    def get_bounds():
        bounds = (
            (0.01, 100),  # t0_is
            (0.01, 0.5),  # t0_boc
            (0.01, 0.5),  # t0_soc_uo
            (0.01, 0.5),  # t0_soc_lo
            (0, 100),  # t0_soh_uo
            (0, 50),  # t0_soh_lo
            (0.01, 100),  # t1_is
            (0.01, 0.5),  # t1_boc
            (0.01, 0.5),  # t1_soc
            (0, 100),  # t1_soh
            (0.01, 100),  # t2_is
            (0.01, 0.5),  # t2_boc
            (0.01, 0.5),  # t2_soc
            (0, 100),  # t2_soh
            (0.01, 100),  # t3_is
            (0.01, 0.5),  # t3_soc
        )
        return bounds

    def to_initial_params(self):
        return np.array([
            self.t0_is,
            self.t0_boc,
            self.t0_soc_uo,
            self.t0_soc_lo,
            self.t0_soh_uo,
            self.t0_soh_lo,
            self.t1_is,
            self.t1_boc,
            self.t1_soc,
            self.t1_soh,
            self.t2_is,
            self.t2_boc,
            self.t2_soc,
            self.t2_soh,
            self.t3_is,
            self.t3_soc,
        ])


@dataclasses.dataclass
class JunctionParameters(Parameters):

    @staticmethod
    def get_bounds():
        return ()

    def to_initial_params(self):
        return np.array([])


@dataclasses.dataclass
class SinkParameters(Parameters):

    @staticmethod
    def get_bounds():
        return ()

    def to_initial_params(self):
        return np.array([])


@dataclasses.dataclass
class ReachParameters(Parameters):
    k: float = 0.01
    x: float = 0.01

    @staticmethod
    def get_bounds():
        bounds = (
            (0.01, 5.0),  # k
            (0.01, 0.5)  # x
        )
        return bounds

    def to_initial_params(self):
        return np.array([
            self.k,
            self.x,
        ])
