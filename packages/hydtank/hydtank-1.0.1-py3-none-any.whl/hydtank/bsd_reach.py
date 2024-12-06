from typing import Optional, List

import numpy as np

from hydtank.basin_def import BasinDef
from hydtank.parameters import ReachParameters


class Reach(BasinDef):
    def __init__(
            self, name: str,
            downstream: Optional[BasinDef] = None,
            upstream: Optional[List[BasinDef]] = None,
            parameters: ReachParameters = ReachParameters()
    ):
        super().__init__(name, downstream, upstream)
        self._parameters = parameters

    def muskingum(
            self, n_step: int, interval: float
    ):
        logs = []
        sum_node = np.zeros(n_step, dtype=np.float64)
        params = self.parameters

        for us_node in self.upstream:
            inflow = us_node.q_sim
            outflow: np.ndarray = np.zeros(n_step, dtype=np.float64)

            c0: float = (-params.k * params.x + 0.5 * interval) / (
                    params.k * (1 - params.x) + 0.5 * interval)
            c1: float = (params.k * params.x + 0.5 * interval) / (
                    params.k * (1 - params.x) + 0.5 * interval)
            c2: float = (params.k * (1 - params.x) - 0.5 * interval) / (
                    params.k * (1 - params.x) + 0.5 * interval)

            if (c0 + c1 + c2) > 1 or params.x > 0.5 or (interval / params.k + params.x) > 1:
                warning_msg = f"WARNING-MUSKINGUM-01 ({self.name}): violates k, x constraints ({params.k}, {params.x})"
                logs.append(warning_msg)
                print(warning_msg)

            outflow[0] = inflow[0]

            for t in np.arange(1, n_step):
                outflow[t] = c0 * inflow[t] + c1 * inflow[t - 1] + c2 * outflow[t - 1]

            sum_node += outflow

        self._q_sim = sum_node

        return logs
