"""
Basin Processing Module

This module provides functionality for processing basin definition files and constructing
basin hierarchies. It handles parsing of basin configuration files and creates appropriate
basin definition objects with their relationships.
"""

from typing import List, Optional, Dict, Tuple, Any
from hydtank.basin_def import BasinDef
from hydtank.bsd_junction import Junction
from hydtank.bsd_reach import Reach
from hydtank.bsd_sink import Sink
from hydtank.bsd_subbasin import Subbasin
from hydtank.parameters import ReachParameters


def extract_basin_file_data(content: str) -> List[Dict[str, str]]:
    """
    Parse raw basin file content into a list of dictionaries containing section data.

    Args:
        content (str): Raw content of the basin definition file

    Returns:
        List[Dict[str, str]]: List of dictionaries where each dictionary represents
        a section with key-value pairs

    Example:
        >>> content = '''
        ... Subbasin: Sub1
        ... Area: 100
        ... End:
        ... '''
        >>> extract_basin_file_data(content)
        [{'Subbasin': 'Sub1', 'Area': '100'}]
    """
    sections = content.split("End:\n")
    data = []

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split("\n")
        section_data: Dict[str, str] = {}
        current_key = None

        for line in lines:
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                section_data[key] = value
                current_key = key
            elif line.strip() and current_key:
                section_data[current_key] += f" {line.strip()}"

        if section_data:
            data.append(section_data)

    return data


def extract_basin_defs_dict(basin_data: List[Dict[str, str]]) -> Dict[str, Tuple[BasinDef, Optional[str]]]:
    """
    Convert parsed basin data into basin definition objects with their downstream connections.

    Args:
        basin_data (List[Dict[str, str]]): List of dictionaries containing basin section data

    Returns:
        Dict[str, Tuple[BasinDef, Optional[str]]]: Dictionary mapping basin names to tuples
        containing the basin definition object and its downstream connection name

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    basin_defs_dict: Dict[str, Tuple[BasinDef, Optional[str]]] = {}
    basin_types = {'Subbasin', 'Reach', 'Junction', 'Sink'}

    for section in basin_data:
        # Find basin type and name
        basin_def_type = next((k for k in section if k in basin_types), None)
        if not basin_def_type:
            continue

        basin_def_name = section[basin_def_type]
        params = {
            'area': float(section.get('Area', 0.0)),
            'downstream': section.get('Downstream'),
            'mk': float(section.get('Muskingum K', 0.0)),
            'mx': float(section.get('Muskingum x', 0.0))
        }

        # Create appropriate basin definition object
        basin_def = _create_basin_def(basin_def_type, basin_def_name, params)
        if basin_def:
            basin_defs_dict[basin_def.name] = (basin_def, params['downstream'])

    return basin_defs_dict


def _create_basin_def(def_type: str, name: str, params: Dict[str, Any]) -> Optional[BasinDef]:
    """
    Create a specific basin definition object based on type and parameters.

    Args:
        def_type (str): Type of basin definition
        name (str): Name of the basin
        params (Dict[str, Any]): Parameters for basin creation

    Returns:
        Optional[BasinDef]: Created basin definition object or None if type is invalid
    """
    if def_type == 'Subbasin':
        return Subbasin(name, params['area'])
    elif def_type == 'Reach':
        return Reach(name, parameters=ReachParameters(params['mk'], params['mx']))
    elif def_type == 'Junction':
        return Junction(name)
    elif def_type == 'Sink':
        return Sink(name)
    return None


def build_basin_defs(basin_defs_dict: Dict[str, Tuple[BasinDef, Optional[str]]]) -> List[BasinDef]:
    """
    Build connections between basin definitions based on downstream relationships.

    Args:
        basin_defs_dict (Dict[str, Tuple[BasinDef, Optional[str]]]): Dictionary of basin
        definitions and their downstream connections

    Returns:
        List[BasinDef]: List of all basin definition objects with established connections

    Raises:
        KeyError: If a downstream reference points to a non-existent basin
    """
    for basin_def, downstream in basin_defs_dict.values():
        if downstream is not None:
            try:
                basin_def.downstream = basin_defs_dict[downstream][0]
            except KeyError:
                raise KeyError(f"Referenced downstream basin '{downstream}' does not exist")

    return [basin_def for basin_def, _ in basin_defs_dict.values()]


def build_root_node(basin_defs: List[BasinDef]) -> List[BasinDef]:
    """
    Identify root nodes and establish upstream connections in the basin hierarchy.

    Args:
        basin_defs (List[BasinDef]): List of basin definitions to process

    Returns:
        List[BasinDef]: List of root nodes (basins with no downstream connections)

    Example:
        >>> sub1 = Subbasin("Sub1", 100)
        >>> sub2 = Subbasin("Sub2", 200)
        >>> junction = Junction("J1")
        >>> sub1.downstream = junction
        >>> sub2.downstream = junction
        >>> root_nodes = build_root_node([sub1, sub2, junction])
        >>> len(root_nodes)
        1
        >>> root_nodes[0].name
        'J1'
    """
    root_nodes: List[BasinDef] = []

    for basin_def in basin_defs:
        if basin_def.downstream is None:
            root_nodes.append(basin_def)
        else:
            downstream = basin_def.downstream
            if not downstream.upstream:
                downstream.upstream = [basin_def]
            else:
                downstream.upstream.append(basin_def)

    return root_nodes
