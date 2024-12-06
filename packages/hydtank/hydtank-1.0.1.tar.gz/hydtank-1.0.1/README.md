# HydTANK

![PyPI - Version](https://img.shields.io/pypi/v/hydtank)

Python implementation of the Tank Hydrological model by Sugawara and Funiyuki (1956), based on the original code
from [tank-model](https://github.com/nzahasan/tank-model) by [nzahasan](https://github.com/nzahasan).

## Installation

```bash
pip install hydtank
```

## Getting Started

### 1. Prepare the Dataset

The dataset must include the following columns: Date, Precipitation, Evapotranspiration, and Discharge. Additionally,
ensure that:

- The time intervals between dates are consistent (e.g., 24 hours) for accurate model performance.

Example dataset:

| Date       | Discharge | Precipitation | Evapotranspiration |
|------------|-----------|---------------|--------------------|
| 10/9/2016  | 0.25694   | 0             | 2.79               |
| 10/10/2016 | 0.25812   | 0             | 3.46               |
| 10/11/2016 | 0.30983   | 0             | 3.65               |
| 10/12/2016 | 0.31422   | 0             | 3.46               |
| 10/13/2016 | 0.30866   | 0             | 5.64               |
| 10/14/2016 | 0.30868   | 0             | 3.24               |
| 10/15/2016 | 0.31299   | 0             | 3.41               |
| ...        | ...       | ...           | ...                |

### 2. Prepare the HEC-HMS Basin File

In addition to the dataset, ensure you have the required HEC-HMS basin file. This file contains the hydrological and
geographical configuration needed for the TANK model.

### 3. Initialize the Model

#### 3.1 Directly from a dataset file and a basin file:

```python
from hydtank import build_hydtank

with open('data.csv') as file1, open('NuiLe_GiaUi.basin') as file2:
    tank = build_hydtank(
        dataset_content=file1.read(),
        basin_content=file2.read(),
        interval=24.0,
        start=None,
        end=None
    )
```

#### 3.2 From a `Dataset` and a basin file:

```python
import pandas as pd
from hydtank import build_hydtank_from_dataset, Dataset, TIME_SERIES, PRECIPITATION, EVAPOTRANSPIRATION, DISCHARGE

df = pd.read_csv('data.csv')

_dataset = Dataset(
    time_series=df[TIME_SERIES].tolist(),
    precipitation=df[PRECIPITATION].tolist(),
    evapotranspiration=df[EVAPOTRANSPIRATION].tolist(),
    discharge=df[DISCHARGE].tolist(),
)

tank = build_hydtank_from_dataset(
    basin_content=open('NuiLe_GiaUi.basin').read(),
    _dataset=_dataset,
    interval=24.0,
    start=None,
    end=None
)
```

#### 3.3 From an existing model:

```python
from hydtank import build_hydtank, HydTANK

with open('data.csv') as file1, open('NuiLe_GiaUi.basin') as file2:
    tank = build_hydtank(
        file1.read(),
        file2.read()
    )

    # Avoid using the original model directly!
    # Always make a copy before creating a new model
    tank_copy = tank.copy()

    tank2 = HydTANK(
        tank_copy.dataset,
        tank_copy.basin_defs,
        tank_copy.root_node,
        tank_copy.interval,
        tank_copy.start,
        tank_copy.end
    )
```

### 4. Retrieve `BasinDef` Information by Name

```python
from hydtank.bsd_junction import Junction
from hydtank.bsd_reach import Reach
from hydtank.bsd_sink import Sink
from hydtank.bsd_subbasin import Subbasin

...

try:
    nui_le: Subbasin = tank.get_basin_def_by_name('NuiLe')
    giaui_local: Subbasin = tank.get_basin_def_by_name('GiaUi_Local')
    reach1: Reach = tank.get_basin_def_by_name('Reach1')
    junction1: Junction = tank.get_basin_def_by_name('Junction1')
    sink: Sink = tank.get_basin_def_by_name('Sink1')
except ValueError:
    # BasinDef not found
    pass
```

### 5. Plotting

```python
tank.plot_basin_network().save('GiaUi_NuiLe_Basin_Network.png')
tank.plot_headwater_q().save('GiaUi_NuiLe_Headwater.png')
tank.plot_q().save('GiaUi_NuiLe_Qsim.png')
tank.plot_subbasin(nui_le).save('GiaUi_NuiLe_NuiLe_Subbasin.png')
tank.plot_subbasin(giaui_local).save('GiaUi_NuiLe_GiaUiLocal_Subbasin.png')
```

### 6. Reconfigure Parameters for a `BasinDef`

```python
from hydtank.parameters import SubbasinParameters, ReachParameters

...

params = reach1.parameters.copy()
params.k = 0.9235288521736096
tank.reconfig_parameters(reach1.name, params)
tank.reconfig_parameters(reach1.name, ReachParameters())

tank.reconfig_parameters(nui_le.name, SubbasinParameters())
```

### 7. Auto-Optimize Parameters for `Subbasin` and `Reach`

#### 7.1 Optimize Specific `Subbasin` and `Reach`

```python
tank.optimize([nui_le, reach1, giaui_local])
```

#### 7.2 Optimize All

**Note:** This process can take significant time as it involves optimizing parameters for all `Subbasin` and `Reach`
elements in the model.

```python
tank.optimize_all()
```

### 8. Export Calculation Results as a `pandas.DataFrame`

```python
r_df = tank.to_dataframe()
```

### 9. Set a New `Dataset`

```python
df = pd.read_csv('new_data.csv')

_dataset = Dataset(
    time_series=df[TIME_SERIES].tolist(),
    precipitation=df[PRECIPITATION].tolist(),
    evapotranspiration=df[EVAPOTRANSPIRATION].tolist(),
    discharge=df[DISCHARGE].tolist(),
)

tank.reset_dataset(_dataset, interval=24.0)
```

### 10. Configure Time Range

```python
from datetime import datetime

...

tank.set_timeseries_range(start=datetime(...), end=datetime(...))
```

## License

This library is released under the MIT License.

## Contact

For any questions or issues, please open an issue on [GitHub](https://github.com/duynguyen02/HydTANK/issues) or email us
at [duynguyen02.dev@gmail.com](mailto:duynguyen02.dev@gmail.com).

---