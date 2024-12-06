from datetime import datetime
from io import StringIO
from typing import Optional

from hydutils.hyd_constants import (
    TIMESERIES,
    PRECIPITATION,
    EVAPOTRANSPIRATION,
    DISCHARGE,
)
import pandas as pd

from hydtank.basin_def_utils import (
    extract_basin_file_data,
    extract_basin_defs_dict,
    build_basin_defs,
    build_root_node,
)
from hydtank.dataset import Dataset
from hydtank.hydtank import HydTANK


def _build_basin_defs_from_content(basin_content: str):
    data = extract_basin_file_data(basin_content)

    basin_defs_dict = extract_basin_defs_dict(data)

    basin_defs = build_basin_defs(basin_defs_dict)

    return basin_defs


def build_hydtank_from_dataset(
    basin_content: str,
    _dataset: Dataset,
    interval: float = 24.0,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    basin_defs = _build_basin_defs_from_content(basin_content)

    root_node = build_root_node(basin_defs)

    return HydTANK(_dataset, basin_defs, root_node, interval, start, end)


def build_hydtank(
    dataset_content: str,
    basin_content: str,
    interval: float = 24.0,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    timeseries_column_name: str = TIMESERIES,
    precipitations_column_name: str = PRECIPITATION,
    evapotranspirations_column_name: str = EVAPOTRANSPIRATION,
    discharge_column_name: str = DISCHARGE,
):
    df = pd.read_csv(StringIO(dataset_content))

    _dataset = Dataset(
        time_series=df[timeseries_column_name].tolist(),
        precipitation=df[precipitations_column_name].tolist(),
        evapotranspiration=df[evapotranspirations_column_name].tolist(),
        discharge=df[discharge_column_name].tolist(),
    )

    return build_hydtank_from_dataset(basin_content, _dataset, interval, start, end)
