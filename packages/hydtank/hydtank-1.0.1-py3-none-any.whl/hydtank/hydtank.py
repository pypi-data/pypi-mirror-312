import copy
import io
from datetime import datetime
from queue import Queue
from typing import Optional, List, Literal, Union

from hydutils.df_validation import (
    validate_columns_for_nulls,
    validate_interval,
    filter_timeseries,
)
from hydutils.hyd_constants import (
    TIMESERIES,
    INTERVAL,
    PRECIPITATION,
    EVAPOTRANSPIRATION,
    DISCHARGE,
)
import networkx as nx
import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from scipy.optimize import minimize

from hydtank.basin_def import BasinDef
from hydtank.bsd_junction import Junction
from hydtank.bsd_reach import Reach
from hydtank.bsd_sink import Sink
from hydtank.bsd_subbasin import Subbasin
from hydtank.dataset import Dataset
from hydtank.parameters import Parameters, SubbasinParameters, ReachParameters


class HydTANK:
    def __init__(
        self,
        dataset: Dataset,
        basin_defs: List[BasinDef],
        root_node: List[BasinDef],
        interval: float = 24.0,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ):
        self._dataset = dataset
        self._basin_defs = basin_defs
        self._root_node = root_node

        self._interval = interval
        self._start = start
        self._end = end

        self._timeseries: Optional[np.ndarray] = None
        self._P: Optional[np.ndarray] = None
        self._E: Optional[np.ndarray] = None
        self._q_obs: Optional[np.ndarray] = None

        self._logs: List[str] = []

        self._run()

    @property
    def dataset(self):
        return self._dataset

    @property
    def basin_defs(self):
        return self._basin_defs

    @property
    def root_node(self):
        return self._root_node

    @property
    def interval(self):
        return self._interval

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def logs(self):
        return self._logs

    def copy(self):
        return copy.deepcopy(self)

    def _validate_dataset_n_provide_dataframe(self):
        df = self._dataset.to_dataframe()
        df = validate_columns_for_nulls(df)
        df = validate_interval(df, self._interval)
        return df

    def _init_input(self, df: pd.DataFrame):
        self._timeseries = df[TIMESERIES].reset_index(drop=True).to_numpy()
        self._P = df[PRECIPITATION].reset_index(drop=True).to_numpy()
        self._E = df[EVAPOTRANSPIRATION].reset_index(drop=True).to_numpy()
        self._q_obs = df[DISCHARGE].reset_index(drop=True).to_numpy()

    def _build_computation_stack(self):
        computation_stack = []
        node_queue: Queue[BasinDef] = Queue()
        for root_node in self._root_node:
            node_queue.put(root_node)

        while not node_queue.empty():
            node = node_queue.get()
            node.parameters.validate()

            computation_stack.append(node)

            if node.upstream:
                for child_node in node.upstream:
                    node_queue.put(child_node)

        return computation_stack

    def _compute(self):
        computation_stack = self._build_computation_stack()

        n_step = len(self._P)

        while len(computation_stack) > 0:
            current_node = computation_stack.pop()

            if isinstance(current_node, Subbasin):
                self._logs += current_node.tank_discharge(
                    self._P, self._E, n_step, self._interval
                )

            elif isinstance(current_node, Sink) or isinstance(current_node, Junction):
                current_node.upstream_discharge(n_step)

            elif isinstance(current_node, Reach):
                self._logs += current_node.muskingum(n_step, self._interval)

            current_node.calculate_stats(self._q_obs)

    def _run(self):
        self._logs = []
        df = self._validate_dataset_n_provide_dataframe()
        df = filter_timeseries(df, self._start, self._end)
        self._init_input(df)
        self._compute()

    def reload(self):
        self._run()

    def _reconfig_by_stacked_parameters(
        self, basin_defs: List[Union[Subbasin, Reach]], stacked_parameters: List[float]
    ):
        subbasin_steps = len(SubbasinParameters().to_initial_params())
        reach_steps = len(ReachParameters().to_initial_params())
        _from = 0
        for basin_def in basin_defs:
            if isinstance(basin_def, Subbasin):
                steps = _from + subbasin_steps
                basin_def.parameters = SubbasinParameters(
                    *stacked_parameters[_from:steps]
                )
                _from = steps
            if isinstance(basin_def, Reach):
                steps = _from + reach_steps
                basin_def.parameters = ReachParameters(*stacked_parameters[_from:steps])
                _from = steps

        self._run()

    def _optimize_operator(
        self, stacked_parameters: List[float], basin_defs: List[Union[Subbasin, Reach]]
    ):
        self._reconfig_by_stacked_parameters(basin_defs, stacked_parameters)
        _nse = 0
        for basin_def in self._root_node:
            _nse += basin_def.stats.nse
        _nse = _nse / len(self._root_node)
        return 1 - _nse

    def optimize(self, basin_defs: List[Union[Subbasin, Reach]], eps: float = 0.01):
        stacked_parameters = []
        lower_bound_stacked = []
        upper_bound_stacked = []

        for basin_def in basin_defs:
            stacked_parameters.extend(basin_def.parameters.to_initial_params())
            for min_bound, max_bound in basin_def.parameters.get_bounds():
                lower_bound_stacked.append(min_bound)
                upper_bound_stacked.append(max_bound)

        initial_guess = np.array(stacked_parameters)
        param_bounds = np.column_stack((lower_bound_stacked, upper_bound_stacked))

        optimizer = minimize(
            fun=self._optimize_operator,
            x0=initial_guess,
            args=basin_defs,
            method="L-BFGS-B",
            bounds=param_bounds,
            options={"eps": eps},
        )

        self._reconfig_by_stacked_parameters(basin_defs, optimizer.x)

    def optimize_all(self, eps: float = 0.01):
        self.optimize(
            [
                basin_def
                for basin_def in self.basin_defs
                if isinstance(basin_def, (Reach, Subbasin))
            ],
            eps,
        )

    def reset_dataset(self, dataset: Dataset, interval: Optional[float]):
        self._dataset = dataset
        self._interval = interval if interval is not None else self._interval
        self._run()

    def set_timeseries_range(self, start: Optional[datetime], end: Optional[datetime]):
        self._start = start
        self._end = end
        self._run()

    def get_basin_def_by_name(self, name: str) -> Optional[BasinDef]:
        for basin_def in self._basin_defs:
            if basin_def.name == name:
                return basin_def

        raise ValueError(f"The BasinDef {name} does not exist.")

    def reconfig_parameters(self, name: str, parameters: Parameters):
        basin_def = self.get_basin_def_by_name(name)

        if (
            isinstance(basin_def, Subbasin)
            and isinstance(parameters, SubbasinParameters)
        ) or (isinstance(basin_def, Reach) and isinstance(parameters, ReachParameters)):
            basin_def.parameters = parameters

        else:
            raise ValueError(
                f"{type(parameters).__name__} cannot be configured for {type(basin_def).__name__}."
            )

        self._run()

    def _generate_plot(
        self, plot_data, xlabel="Timeseries", ylabel="Flow", figsize=(12, 6), title=None
    ):
        plt.figure(figsize=figsize)

        for label, data in plot_data:
            plt.plot(self._timeseries, data, label=label)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        if title:
            plt.title(title)

        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="PNG", bbox_inches="tight")
        buf.seek(0)
        image = Image.open(buf)
        plt.close()

        return image

    def plot_subbasin(self, subbasin: Subbasin, figsize=(12, 6)):
        if subbasin not in self._basin_defs:
            raise ValueError(f"The subbasin does not exist in the basin.")

        flow_data = [
            ("TANK 0", subbasin.q_tank_0),
            ("TANK 1", subbasin.q_tank_1),
            ("TANK 2", subbasin.q_tank_2),
            ("TANK 3", subbasin.q_tank_3),
            ("Bottom outlet flow TANK 0", subbasin.bottom_outlet_flow_tank_0),
            ("Bottom outlet flow TANK 1", subbasin.bottom_outlet_flow_tank_1),
            ("Bottom outlet flow TANK 2", subbasin.bottom_outlet_flow_tank_2),
            ("Side outlet flow TANK 1", subbasin.side_outlet_flow_tank_1),
            ("Side outlet flow TANK 2", subbasin.side_outlet_flow_tank_2),
            ("Side outlet flow TANK 3", subbasin.side_outlet_flow_tank_3),
        ]

        return self._generate_plot(
            flow_data,
            figsize=figsize,
            title=f"Subbasin {subbasin.name} Flow Characteristics",
        )

    def _plot_basin_q(self, include_all=True):
        plot_data = [("Q_obs", self._q_obs)]

        basin_defs = (
            self._root_node
            if include_all
            else [b for b in self._basin_defs if not b.upstream]
        )

        plot_data.extend(
            [(basin_def.name, basin_def.q_sim) for basin_def in basin_defs]
        )

        title = (
            "Basin Discharge (All Basins)"
            if include_all
            else "Headwater Basin Discharge"
        )
        return self._generate_plot(plot_data, ylabel="Q", title=title)

    def plot_q(self):
        return self._plot_basin_q(include_all=True)

    def plot_headwater_q(self):
        return self._plot_basin_q(include_all=False)

    def plot_basin_network(
        self,
        layout_type: Literal[
            "hierarchical", "circular", "spring", "kamada-kawai", "multipartite"
        ] = "hierarchical",
        figsize=(15, 10),
        node_spacing=1.0,
    ):
        color_map = {
            "Subbasin": "#7FB3D5",
            "Junction": "#F4D03F",
            "Reach": "#2ECC71",
            "Sink": "#E74C3C",
        }
        shape_map = {"Subbasin": "s", "Junction": "o", "Reach": "^", "Sink": "v"}

        graph = nx.DiGraph()

        def build_network(_basin_def: BasinDef):
            for us_basin_def in _basin_def.upstream:
                build_network(us_basin_def)
                graph.add_edge(us_basin_def.name, _basin_def.name)
            graph.add_node(_basin_def.name, component_type=type(_basin_def).__name__)

        for basin_def in self._root_node:
            build_network(basin_def)

        plt.figure(figsize=figsize)

        pos = None
        if layout_type == "hierarchical":
            pos = nx.spring_layout(graph, k=node_spacing)
            root_nodes = [n for n in graph.nodes() if graph.in_degree(n) == 0]
            for node in nx.descendants(graph, root_nodes[0]):
                level = nx.shortest_path_length(graph, root_nodes[0], node)
                pos[node] = (pos[node][0], 1 - level * 0.2)

        elif layout_type == "circular":
            pos = nx.circular_layout(graph)

        elif layout_type == "spring":
            pos = nx.spring_layout(graph, k=node_spacing, iterations=50)

        elif layout_type == "kamada-kawai":
            pos = nx.kamada_kawai_layout(graph)

        elif layout_type == "multipartite":
            layers = {}
            for node in graph.nodes():
                if graph.in_degree(node) == 0:
                    layers[node] = 0
                elif graph.out_degree(node) == 0:
                    layers[node] = 2
                else:
                    layers[node] = 1
            nx.set_node_attributes(graph, layers, "layer")
            pos = nx.multipartite_layout(graph, subset_key="layer")

        for component_type in ["Subbasin", "Junction", "Reach", "Sink"]:
            nodes = [
                node
                for node, attr in graph.nodes(data=True)
                if attr.get("component_type") == component_type
            ]

            if nodes:
                nx.draw_networkx_nodes(
                    graph,
                    pos,
                    nodelist=nodes,
                    node_color=color_map[component_type],
                    node_shape=shape_map[component_type],
                    node_size=1000,
                    label=component_type,
                )

        nx.draw_networkx_edges(
            graph,
            pos,
            edge_color="gray",
            arrows=True,
            arrowsize=20,
            edge_cmap=plt.cm.Blues,
            width=2,
            connectionstyle="arc3,rad=0.2",
        )

        labels = nx.draw_networkx_labels(graph, pos)
        for label in labels.values():
            label.set_bbox(dict(facecolor="white", edgecolor="none", alpha=0.7))

        plt.title(
            f"Watershed Network Visualization\n({layout_type.title()} Layout)",
            size=16,
            pad=20,
        )
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.axis("off")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="PNG", bbox_inches="tight")
        buf.seek(0)

        image = Image.open(buf)
        plt.close()

        return image

    def to_dataframe(self):
        data = {"Timeseries": self._timeseries, "Q_obs": self._q_obs}
        data.update({basin_def.name: basin_def.q_sim for basin_def in self._basin_defs})
        return pd.DataFrame(data)
