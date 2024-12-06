import numpy as np

from hydtank.basin_def import BasinDef


class FlowNode(BasinDef):
    def upstream_discharge(self, n_step: int):
        sum_node = np.zeros(n_step, dtype=np.float64)

        for us_node in self._upstream:
            sum_node += us_node.q_sim

        self._q_sim = sum_node
