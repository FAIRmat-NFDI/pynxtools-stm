from pathlib import PosixPath
from typing import Dict, Optional, Tuple
from pint import UnitRegistry
from typing import Optional, Dict, Tuple
import logging

import json

ureg = UnitRegistry()

#  try to create a common logger for all the modules
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")

__scientific_num_pattern = r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?"


def read_config_file(config_file: str) -> Dict:
    """Read the config file and return the dictionary.

    Parameters
    ----------
    config_file : str
        The path to the config file.

    Returns
    -------
    Dict
        The dictionary from the config file.
    """
    if isinstance(config_file, PosixPath):
        config_file = str(config_file.absulute())

    if config_file.startswith("json"):
        with open(config_file, mode="r", encoding="utf-8") as f_obj:
            config_file = json.load(f_obj)
    else:
        raise ValueError("The config file should be in JSON format.")
    return config_file


def __verify_unit(
    base_key=None, conf_dict=None, data_dict=None, unit=None, concept=None
):
    unit_derived = None
    if unit is not None:
        unit_derived = unit
    elif base_key:
        unit_or_path = conf_dict[f"{base_key}/@units"]
        if unit_or_path.starswith("@default:"):
            unit_derived = unit_or_path.split("@default:")[-1]
        else:
            unit_derived = data_dict.get(unit_or_path, None)
    try:
        return str(ureg(unit_derived).units)
    except Exception as e:
        # TODO: add nomad logger here
        logger.debug(f"Check the unit for nx concept {concept}.\n" f"Error : {e}")
        return None


def __get_data_unit_and_others(
    data_dict=None, partial_conf_dict=None, concept_field=None
) -> Tuple[str, str, Optional[dict]]:
    """Destructure the raw data, units, and other attrs.

    TODO: write doc test for this function

    Parameters:
    -----------
        data_dict : Dict[str, Any]
            The data dict that comes from the raw file. A partial example of data dict

            example:
            data_dict = {
              /SCAN/TIME" :              1.792E-1             1.792E-1
              /SCAN/RANGE :            4.000000E-9           4.000000E-9
              /SCAN/OFFSET :              -2.583985E-7         1.223062E-7
              /SCAN/ANGLE :             0.000E+0
              /SCAN/DIR : down
            }

        partial_conf_dict : Dict[str, Any]
            The dict that maps from nx concept field (or group especially for NXdata) to dict which explains
            raw data path, units, and other attributes (if exists).

            example for grp "scan_region"
            partial_conf_dict ={
                "scan_angle_N[scan_angle_n]": {
                    "raw_path": "/SCAN/ANGLE",
                    "@units": "@default:deg"
                },
                "scan_offset_N[scan_offset_n]": {
                    "raw_path": "/SCAN/OFFSET",
                },
                "scan_range_N[scan_range_n]": {
                    "raw_path": "/SCAN/RANGE",
                    "@units": "/path/to/unit/in/raw/file",
                    "@example_attr": "test_attr",
                }
            },
        concept_field : str
            The name of the concept field which is a key in partial_conf_dict

            example: scan_angle_N[scan_angle_n]

    Returns:
    --------
        tuple :
            The tuple contains components like raw data string, unit string, and dict that
            contains other attributes (if any attributes comes as a part of value dict).
            See the example below.

    """

    val_dict: dict[str:any] = partial_conf_dict[concept_field]

    raw_data = data_dict.get(val_dict.get("raw_path", None), None)
    unit_des = val_dict.get("@units", None)
    try:
        del val_dict["raw_path"]
        del val_dict["@units"]
    except KeyError:
        pass

    if unit_des and unit_des.startswith("@default:"):
        unit = unit_des.split("@default:")[-1]
    else:
        unit = data_dict.get(unit_des, None)
    # TODO: write a function that write other attributes in general and use that func where this function is used
    return raw_data, __verify_unit(unit=unit), val_dict
