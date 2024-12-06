import copy
from datetime import datetime
from typing import List

from hydutils.hyd_constants import (
    TIMESERIES,
    PRECIPITATION,
    EVAPOTRANSPIRATION,
    DISCHARGE,
)
import pandas as pd


class Dataset:
    def __init__(
        self,
        time_series: List[datetime],
        precipitation: List[float],
        evapotranspiration: List[float],
        discharge: List[float],
    ):
        self._time_series = time_series
        self._precipitation = precipitation
        self._evapotranspiration = evapotranspiration
        self._discharge = discharge

    def to_dataframe(self):
        dataset_dict = {
            TIMESERIES: self._time_series,
            PRECIPITATION: self._precipitation,
            EVAPOTRANSPIRATION: self._evapotranspiration,
            DISCHARGE: self._discharge,
        }

        df = pd.DataFrame(dataset_dict)
        df[TIMESERIES] = pd.to_datetime(df[TIMESERIES])
        return df

    def copy(self):
        return copy.deepcopy(self)
