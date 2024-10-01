from pathlib import PosixPath
from typing import Dict, Optional, Tuple
from pint import UnitRegistry
from typing import Optional, Dict, Tuple
import logging
from copy import deepcopy
import numpy as np
import re
import json

ureg = UnitRegistry()

#  try to create a common logger for all the modules
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")

_scientific_num_pattern = r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?"


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


def _verify_unit(
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
            unit_derived = (
                data_dict.get(unit_or_path, None)
                if isinstance(data_dict, dict)
                else None
            )
    try:
        unit_derived = str(ureg(unit_derived).units)
        return unit_derived
        # return "" if unit_derived == "dimensionless" else unit_derived
    except Exception as e:
        # TODO: add nomad logger here
        logger.debug(f"Check the unit for nx concept {concept}.\n" f"Error : {e}")
        return None


def _get_data_unit_and_others(
    data_dict, partial_conf_dict=None, concept_field=None, end_dict=None
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

    if end_dict is None:
        end_dict: dict[str:any] = partial_conf_dict[concept_field]

    # # Skip the non-general data
    # if "#note" in end_dict:
    #     return None, None, {}

    raw_path = end_dict.get("raw_path", "")

    # if raw_path have multiple possibel path to the raw data
    if isinstance(raw_path, list):
        for path in raw_path:
            raw_data = data_dict.get(path, "")
            if raw_data != "":
                break
    elif raw_path.startswith("@default:"):
        raw_data = raw_path.split("@default:")[-1]
    else:
        raw_data = data_dict.get(raw_path)
    unit_des = end_dict.get("@units", None)

    try:
        val_copy = deepcopy(end_dict)
        del val_copy["raw_path"]
        del val_copy["@units"]
    except KeyError:
        pass

    if unit_des and unit_des.startswith("@default:"):
        unit = unit_des.split("@default:")[-1]
    else:
        unit = data_dict.get(unit_des, None)
    # TODO: write a function that write other attributes in general and use that func where this function is used
    return raw_data, _verify_unit(unit=unit), val_copy


# pylint: disable=too-many-return-statements
def to_intended_t(str_value):
    """
        Transform string to the intended data type, if not then return str_value.
    e.g '2.5E-2' will be transfor into 2.5E-2
    tested with: '2.4E-23', '28', '45.98', 'test', ['59', '3.00005', '498E-34'], None
    with result: 2.4e-23, 28, 45.98, test, [5.90000e+01 3.00005e+00 4.98000e-32], None

    Parameters
    ----------
    str_value : _type_
        _description_

    Returns
    -------
    Union[str, int, float, np.ndarray]
        Converted data type
    """
    symbol_list_for_data_seperation = [";"]
    transformed = ""
    if str_value is None:
        return str_value

    if isinstance(str_value, list):
        str_value = list(str_value)
        try:
            transformed = np.array(str_value, dtype=np.float64)
            return transformed
        except ValueError:
            pass

    if isinstance(str_value, np.ndarray):
        return str_value

    if isinstance(str_value, str):
        if str_value in (
            "infinitiy",
            "-infinity",
            "Infinity",
            "-Infinity",
            "INFINITY",
            "-INFINITY",
            "inf",
            "-inf",
            "Inf",
            "-Inf",
            "INF",
            "-INF",
            "NaN",
            "nan",
        ):
            return None
        try:
            transformed = int(str_value)
            return transformed
        except ValueError:
            try:
                transformed = float(str_value)
                return transformed
            except ValueError:
                if "[" in str_value and "]" in str_value:
                    transformed = json.loads(str_value)
                    return transformed

        for sym in symbol_list_for_data_seperation:
            if sym in str_value:
                parts = str_value.split(sym)
                modified_parts = []
                for part in parts:
                    modified_parts.append(to_intended_t(part))
                return modified_parts

    return str_value


def get_link_compatible_key(key):
    """A unction to convert the key to compatible hdf5 link."""
    # TODO use regrex pattern to match the key
    # # DO not know why this pattern does not work
    # pattern = r"\[([^\]]+)\]"
    # Convert the key to compatible key for template
    compatible_key = key.replace("NX", "")
    key_parts = compatible_key.split("/")
    new_parts = []
    for part in key_parts:
        ind_f = part.find("[")
        ind_e = part.find("]")
        if ind_f > 0 and ind_e > 0:
            new_parts.append(part[ind_f + 1 : ind_e])

    compatible_key = "/" + "/".join(new_parts)
    print("  #### compatible_key: ", compatible_key)
    return compatible_key


def replace_variadic_name_part(name, part_to_embed):
    """Replace the variadic part of the name with the part_to_embed.
    e.g. name = "scan_angle_N_X[scan_angle_n_x]", part_to_embed = "xy"
    then the output will be "scan_angle_xy"

    # TODO: write test for this function with the following test_dict
    and try to replace this with regex pattern
    test_dict = {('yy_NM[yy_nm]', 'x'): 'yy_NM[yy_x]',
                 ('yy_M_N[yy_m_n]', 'x') : 'yy_M_N[yy_x]',
                 ('Myy[myy]', 'x') : 'Myy[xyy]',
                 ('y_M_yy[y_m_yy]', 'x') : 'y_M_yy[y_x_yy]',
                 ('y_M_N_yy[y_x_yy]', 'x') : 'y_M_N_yy[y_x_yy]',}
    """
    f_part, _ = name.split("[") if "[" in name else (name, "")
    ind_start = None
    ind_end = None
    for ind, chr in enumerate(f_part):
        if chr.isupper():
            if ind_start is None:
                ind_start = ind
        if ind_start is not None and chr.islower():
            ind_end = ind
            break
    if ind_end is None and ind_start is not None:
        f_part_mod = f_part.replace(f_part[ind_start:], part_to_embed)
        return "[".join([f_part, f_part_mod]) + "]"
    elif ind_end is not None and ind_start is not None:
        replacement_p = f_part[ind_start:ind_end]
        # if replacement_p end with '_'
        if replacement_p.endwith("_"):
            replacement_p = replacement_p[:-1]
        f_part_mod = f_part.replace(replacement_p, part_to_embed)
        return "[".join([f_part, f_part_mod]) + "]"
    else:
        return name


def transfer_plain_template_to_nested_dict(template, nested_dict):
    """TODO: Write a doc compatibel with doc test write test in pytest."""

    def split_each_key(key, final_val, nested_dict):
        parts = key.split("/", 1)
        if len(parts) < 2:
            parts.append("")
        k1, rest = parts
        k1_val = nested_dict.get(k1, None)
        if k1_val is None and rest != "":
            nested_dict[k1] = dict()
            split_each_key(rest, final_val, nested_dict[k1])
        elif rest == "":
            nested_dict[k1] = final_val
        elif isinstance(k1_val, dict):
            split_each_key(rest, final_val, k1_val)

    for key, value in template.items():
        _, rest = key.split("/", 1)
        split_each_key(key=rest, final_val=value, nested_dict=nested_dict)
