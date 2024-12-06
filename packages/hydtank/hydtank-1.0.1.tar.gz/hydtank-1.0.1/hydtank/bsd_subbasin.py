from typing import Optional, List

import numpy as np

from hydtank.basin_def import BasinDef
from hydtank.parameters import SubbasinParameters


class Subbasin(BasinDef):
    def __init__(
            self, name: str,
            area: float,
            downstream: Optional[BasinDef] = None,
            upstream: Optional[List[BasinDef]] = None,
            parameters: SubbasinParameters = SubbasinParameters()
    ):
        super().__init__(name, downstream, upstream)

        self._area = area
        self._parameters = parameters

        self._q_tank_0: Optional[np.ndarray] = None
        self._q_tank_1: Optional[np.ndarray] = None
        self._q_tank_2: Optional[np.ndarray] = None
        self._q_tank_3: Optional[np.ndarray] = None

        self._side_outlet_flow_tank_0: Optional[np.ndarray] = None
        self._side_outlet_flow_tank_1: Optional[np.ndarray] = None
        self._side_outlet_flow_tank_2: Optional[np.ndarray] = None
        self._side_outlet_flow_tank_3: Optional[np.ndarray] = None

        self._bottom_outlet_flow_tank_0: Optional[np.ndarray] = None
        self._bottom_outlet_flow_tank_1: Optional[np.ndarray] = None
        self._bottom_outlet_flow_tank_2: Optional[np.ndarray] = None

    @property
    def bottom_outlet_flow_tank_0(self) -> Optional[np.ndarray]:
        return self._bottom_outlet_flow_tank_0

    @property
    def bottom_outlet_flow_tank_1(self) -> Optional[np.ndarray]:
        return self._bottom_outlet_flow_tank_1

    @property
    def bottom_outlet_flow_tank_2(self) -> Optional[np.ndarray]:
        return self._bottom_outlet_flow_tank_2

    @property
    def side_outlet_flow_tank_1(self) -> Optional[np.ndarray]:
        return self._side_outlet_flow_tank_1

    @property
    def side_outlet_flow_tank_2(self) -> Optional[np.ndarray]:
        return self._side_outlet_flow_tank_2

    @property
    def side_outlet_flow_tank_3(self) -> Optional[np.ndarray]:
        return self._side_outlet_flow_tank_3

    @property
    def q_tank_0(self) -> Optional[np.ndarray]:
        return self._q_tank_0

    @property
    def q_tank_1(self) -> Optional[np.ndarray]:
        return self._q_tank_1

    @property
    def q_tank_2(self) -> Optional[np.ndarray]:
        return self._q_tank_2

    @property
    def q_tank_3(self) -> Optional[np.ndarray]:
        return self._q_tank_3

    @property
    def area(self):
        return self._area

    def tank_discharge(self, p: np.ndarray, e: np.ndarray, time_step: int, interval: float) -> List[str]:
        logs = []
        params = self._parameters

        if params.t0_soh_uo < params.t0_soh_lo:
            warnings_msg = f'WARNING-TANK-01 ({self.name}): Invalid parameter upper outlet height is less than lower outlet height (Tank 0)'
            logs.append(warnings_msg)
            print(warnings_msg)

        tank_storage = np.zeros((time_step, 4), dtype=np.float64)
        side_outlet_flow = np.zeros((time_step, 4), dtype=np.float64)
        bottom_outlet_flow = np.zeros((time_step, 3), dtype=np.float64)

        del_rf_et = p - e

        tank_storage[0, 0] = max(params.t0_is, 0)
        tank_storage[0, 1] = max(params.t1_is, 0)
        tank_storage[0, 2] = max(params.t2_is, 0)
        tank_storage[0, 3] = max(params.t3_is, 0)

        for t in np.arange(time_step):
            # TANK 0 : surface runoff
            side_outlet_flow[t, 0] = params.t0_soc_lo * max(tank_storage[t, 0] - params.t0_soh_lo, 0) \
                                     + params.t0_soc_uo * max(tank_storage[t, 0] - params.t0_soh_uo, 0)

            # TANK 1 : intermediate runoff
            side_outlet_flow[t, 1] = params.t1_soc * max(tank_storage[t, 1] - params.t1_soh, 0)
            # TANK 2 : sub-base runoff
            side_outlet_flow[t, 2] = params.t2_soc * max(tank_storage[t, 2] - params.t2_soh, 0)
            # TANK 3 : base-flow | Side outlet height = 0
            side_outlet_flow[t, 3] = params.t3_soc * tank_storage[t, 3]

            bottom_outlet_flow[t, 0] = params.t0_boc * tank_storage[t, 0]
            bottom_outlet_flow[t, 1] = params.t1_boc * tank_storage[t, 1]
            bottom_outlet_flow[t, 2] = params.t2_boc * tank_storage[t, 2]

            if t < (time_step - 1):
                tank_storage[t + 1, 0] = tank_storage[t, 0] + del_rf_et[t + 1] - (
                        side_outlet_flow[t, 0] + bottom_outlet_flow[t, 0])

                tank_storage[t + 1, 1] = tank_storage[t, 1] + bottom_outlet_flow[t, 0] - (
                        side_outlet_flow[t, 1] + bottom_outlet_flow[t, 1])

                tank_storage[t + 1, 2] = tank_storage[t, 2] + bottom_outlet_flow[t, 1] - (
                        side_outlet_flow[t, 2] + bottom_outlet_flow[t, 2])

                tank_storage[t + 1, 3] = tank_storage[t, 3] + bottom_outlet_flow[t, 2] - side_outlet_flow[t, 3]

                tank_storage[t + 1, 0] = max(tank_storage[t + 1, 0], 0)
                tank_storage[t + 1, 1] = max(tank_storage[t + 1, 1], 0)
                tank_storage[t + 1, 2] = max(tank_storage[t + 1, 2], 0)
                tank_storage[t + 1, 3] = max(tank_storage[t + 1, 3], 0)

            for i in range(4):
                total_tank_outflow = bottom_outlet_flow[t, i] + side_outlet_flow[t, i] if i <= 2 else side_outlet_flow[
                    t, i]

                if total_tank_outflow > tank_storage[t, i]:
                    warnings_msg = f'WARNING-TANK-02 ({self.name}): Total outlet flow exceeded tank storage for tank {i} at timestep {t}'
                    logs.append(warnings_msg)
                    print(warnings_msg)

        unit_conv_coeff = (self.area * 1000) / (interval * 3600)
        discharge = unit_conv_coeff * side_outlet_flow.sum(axis=1)

        # Set result
        self._q_tank_0 = tank_storage[:, 0]
        self._q_tank_1 = tank_storage[:, 1]
        self._q_tank_2 = tank_storage[:, 2]
        self._q_tank_3 = tank_storage[:, 3]

        self._side_outlet_flow_tank_0 = side_outlet_flow[:, 0]
        self._side_outlet_flow_tank_1 = side_outlet_flow[:, 1]
        self._side_outlet_flow_tank_2 = side_outlet_flow[:, 2]
        self._side_outlet_flow_tank_3 = side_outlet_flow[:, 3]

        self._bottom_outlet_flow_tank_0 = bottom_outlet_flow[:, 0]
        self._bottom_outlet_flow_tank_1 = bottom_outlet_flow[:, 1]
        self._bottom_outlet_flow_tank_2 = bottom_outlet_flow[:, 2]

        self._q_sim = discharge

        return logs
