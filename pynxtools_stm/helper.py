"""
Some generic function and class for on STM reader.
"""
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple, Optional
import copy
import json
import numpy as np
import re
from pynxtools.dataconverter.helpers import convert_data_dict_path_to_hdf5_path


# Here are some data or data type or unit or data to skip:
UNIT_TO_SKIP = ["on/off", "off", "on", "off/on"]


def fill_template_from_eln_data(eln_data_dict, template):
    """Fill out the template from dict that generated from eln yaml file.
    Parameters:
    -----------
    eln_data_dict : dict[str, Any]
        Python dictionary from eln file.
    template : dict[str, Any]
    Return:
    -------
    None
    """

    for e_key, e_val in eln_data_dict.items():
        template[e_key] = to_intended_t(e_val)


def work_out_overwriteable_field(
    template, data_dict, sub_config_dict, nexus_path, dict_orig_key_to_mod_key
):
    """
    Overwrite a field for multiple dimention of the same type of physical quantity.

    Parameters:
    -----------
    template : dict[str, Any]
        Capturing data elements. One to one dictionary for capturing data array, data axes
        and so on from data_dict to be ploted.
    data_dict : dict[str, Union[array, str]]
        Data stored from dat file. Path (str) to data elements which mainly come from
        dat file. Data from this dict will go to template
    data_config_dict : dict[str, list]
        This dictionary is numerical data order to list (list of path to data elements in
        input file). Each order indicates a group of data set.
    field_path : NeXus field full path

    Returns:
    --------
    None
    """
    # Find the overwriteable part
    overwrite_part = ""
    field_to_replace = ""
    # Two possibilities are considered: tilt_N/@units and tilt_N
    if "/@units" in nexus_path:
        field_to_replace = nexus_path.rsplit("/", 2)[-2]
    else:
        field_to_replace = nexus_path.rsplit("/", 1)[-1]
    for char in field_to_replace:
        if char.isupper():
            overwrite_part = overwrite_part + char

    if (
        not overwrite_part
        and not field_to_replace
        and isinstance(sub_config_dict, dict)
    ):
        raise ValueError(
            f"No overwriteable part has been found but data structure "
            f": {sub_config_dict} intended to overeritten."
        )
    # sub_config_dict contains key that repalce the overwritable (upper case part)
    # part from nexus path
    for ch_to_replace, data_path in sub_config_dict.items():
        modified_field = field_to_replace.replace(overwrite_part, ch_to_replace.lower())
        # Considering renamed field
        new_temp_key = nexus_path.replace(
            field_to_replace, f"{field_to_replace}[{modified_field}]"
        )
        value = "value"
        unit = "unit"
        dict_orig_key_to_mod_key[nexus_path] = new_temp_key
        if value in data_path:
            path_to_data = data_path[value]
            template[new_temp_key] = to_intended_t(
                data_dict[path_to_data] if path_to_data in data_dict else None
            )
        if unit in data_path:
            path_to_data = data_path[unit]
            template[new_temp_key + "/@units"] = to_intended_t(
                data_dict[path_to_data] if path_to_data in data_dict else None
            )


def nested_path_to_slash_separated_path(
    nested_dict: dict, flattened_dict: dict, parent_path=""
):
    """Convert nested dict into slash separeted path upto certain level."""
    start = "/"

    for key, val in nested_dict.items():
        path = parent_path + start + key
        if isinstance(val, dict):
            nested_path_to_slash_separated_path(val, flattened_dict, path)
        else:
            flattened_dict[path] = val


def link_seperation(template, link_modified_dict):
    """Rewrite the link compatible with hdf5 full path.
    for e.g. convert /NXentry/NXinstrument/name to
    /entry/instrument/name and rewrite in template.

    Parameters
    ----------
    template : Template (dict)
        To write out the hdf file
    link_modified_dict : dict
        The key corresponds to nxdl def path e.g. /ENTRY[entry]/INSTRUMENT[instrument]/NAME
        and the value is the modified link path e.g.
        /ENTRY[entry]/INSTRUMENT[special_instrument]/given_name where the
        value is according to the implementaion of the NeXus def.
    """
    for _, val in template.items():
        if isinstance(val, dict) and "link" in val:
            orig_link_path = val["link"]
            # Check whether any concept has been rewriten stored in key value
            if orig_link_path in link_modified_dict:
                # modified concepts come in a list together.
                modif_link_hdf_path = convert_data_dict_path_to_hdf5_path(
                    link_modified_dict[orig_link_path]
                )
                val["link"] = modif_link_hdf_path
            else:
                val["link"] = convert_data_dict_path_to_hdf5_path(orig_link_path)


# pylint: disable=line-too-long
def link_seperation_from_hard_code(template, link_modified_dict):
    """This function is intended to handle hard coded link.
    In future, this function can be removed instead the upper function can be used,
    once the application definition will be updated by link element.
    """
    concept_to_data_link: dict = {
        "/ENTRY[entry]/reproducibility_indicators/backward_sweep": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/backward_sweep",
        "/ENTRY[entry]/reproducibility_indicators/bias": "/NXentry/NXinstrument/NXsample_bias/bias",
        "/ENTRY[entry]/reproducibility_indicators/bias_calibration": "/NXentry/NXnstrument/NXsample_bias/bias_calibration",
        "/ENTRY[entry]/reproducibility_indicators/bias_offset": "/NXentry/NXinstrument/NXsample_bias/bias_offset",
        "/ENTRY[entry]/reproducibility_indicators/current": "/NXentry/NXinstrument/NXenvironment/NXcurrent_sensor/current",
        "/ENTRY[entry]/reproducibility_indicators/current_calibration": "/NXentry/NXinstrument/NXenvironment/NXcurrent_sensor/current_calibration",
        "/ENTRY[entry]/reproducibility_indicators/current_gain": "/NXentry/NXinstrument/NXenvironment/NXcurrent_sensor/current_gain",
        "/ENTRY[entry]/reproducibility_indicators/current_offset": "/NXentry/NXinstrument/NXenvironment/NXcurrent_sensor/current_offset",
        "/ENTRY[entry]/reproducibility_indicators/end_settling_time": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/end_settling_time",
        "/ENTRY[entry]/reproducibility_indicators/final_z": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/record_final_z",
        "/ENTRY[entry]/reproducibility_indicators/first_settling_time": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/first_settling_time",
        "/ENTRY[entry]/reproducibility_indicators/max_slew_rate": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/max_slew_rate",
        "/ENTRY[entry]/reproducibility_indicators/settling_time": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/settling_time",
        "/ENTRY[entry]/reproducibility_indicators/y_control_p_gain": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/p_gain",
        "/ENTRY[entry]/reproducibility_indicators/z_control_hold": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/z_ccontroller_hold",
        "/ENTRY[entry]/reproducibility_indicators/z_control_i_gain": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/i_gain",
        "/ENTRY[entry]/reproducibility_indicators/z_control_switchoff_delay": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/switchoff_delay",
        "/ENTRY[entry]/reproducibility_indicators/z_control_time": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/z_control_time",
        "/ENTRY[entry]/reproducibility_indicators/z_control_time_const": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/time_const",
        "/ENTRY[entry]/reproducibility_indicators/z_control_tip_lift": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/tip_lift",
        "/ENTRY[entry]/reproducibility_indicators/z_controller_name": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/controller_name",
        "/ENTRY[entry]/reproducibility_indicators/z_controller_setpoint": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/set_point",
        "/ENTRY[entry]/reproducibility_indicators/z_controller_status": "/NXentry/NXinstrument/NXenvironment/NXposition/NXz_controller/controller_status",
        "/ENTRY[entry]/reproducibility_indicators/z_offset": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/z_offset",
        "/ENTRY[entry]/resolution_indicators/acquisition_period": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXcircuit/acquisition_period",
        "/ENTRY[entry]/resolution_indicators/animations_period": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXcircuit/animations_period",
        "/ENTRY[entry]/resolution_indicators/cryo_bottom_temp": "/NXentry/NXinstrument/cryo_bottom_temp",
        "/ENTRY[entry]/resolution_indicators/cryo_shield_temp": "/NXentry/NXinstrument/temp_cryo_shield",
        "/ENTRY[entry]/resolution_indicators/indicators_period": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXcircuit/indicators_period",
        "/ENTRY[entry]/resolution_indicators/integration_time": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/NXintegration_time",
        "/ENTRY[entry]/resolution_indicators/measurements_period": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXcircuit/measurements_period",
        "/ENTRY[entry]/resolution_indicators/modulation_signal": "/NXentry/NXinstrument/NXlock_in/modulation_signal",
        "/ENTRY[entry]/resolution_indicators/num_pixel": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/num_pixel",
        "/ENTRY[entry]/resolution_indicators/number_of_sweeps": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/number_of_sweeps",
        "/ENTRY[entry]/resolution_indicators/rt_frequency": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXcircuit/rt_frequency",
        "/ENTRY[entry]/resolution_indicators/signals_oversampling": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXcircuit/signals_oversampling",
        "/ENTRY[entry]/resolution_indicators/stm_head_temp": "/NXentry/NXinstrument/stm_head_temp",
        "/ENTRY[entry]/resolution_indicators/sweep_end": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/sweep_end",
        "/ENTRY[entry]/resolution_indicators/sweep_start": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/sweep_start",
        "/ENTRY[entry]/resolution_indicators/z_avg_time": "/NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/z_avg_time",
    }
    # temp_template = copy.deepcopy(template)
    # for key, _ in temp_template.items():
    #     if key in concept_to_data_link:
    #         concept = concept_to_data_link[key]
    #         concept = concept.replace("NX", "")
    #         # check concept already modified before
    #         if concept in link_modified_dict:
    #             concept = link_modified_dict[concept]
    #         template[key] = {"link": concept}

    temp_template = copy.deepcopy(template)
    for key, _ in temp_template.items():
        concept_to_be_linked = concept_to_data_link.get(key, "")
        # e.g. /NXentry/NXinstrument/NXenvironment/NXsweep_control/NXbias_spectroscopy/z_avg_time
        concept_to_be_linked = concept_to_be_linked.replace("NX", "")

        # check concept already modified before
        if concept_to_be_linked:
            rl_concept_in_templt = link_modified_dict.get(concept_to_be_linked, "")
            if rl_concept_in_templt:
                template[key] = {"link": rl_concept_in_templt}


def cal_dx_by_dy(x_val: np.ndarray, y_val: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Calc conductance or gradiant dx/dy for x-variable and y-variable also return the result."""
    dx_ = x_val[0::2] - x_val[1::2]
    dy_ = y_val[0::2] - y_val[1::2]

    dx_by_dy = dx_ / dy_

    return dx_by_dy


def cal_x_multi_x(x_val: np.ndarray, y_val: np.ndarray) -> np.ndarray:
    """Return multiplication of two array"""
    return x_val * y_val


def slice_before_last_element(np_array):
    """Get all the elements before last element."""
    if not isinstance(np_array, np.ndarray) and not len(np.shape(np_array)) == 1:
        raise ValueError("Please provide a numpy array of 1D.")
    return np_array[:-1]


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


def set_default_attr_in_group(template):
    """Set default attribute for each group of Nexus file.
    Each group will have a /@default attrubute refering the immediate child group.
    e.g. /@default = "entry1"
         /entry1/@default = "data_group_1"
        /entry1/instrument/@default = "group1"
    Parameters
    ----------
    template : Template
        Template from filled with datafile and eln.
    """
    # defalut attribute key to the list of immediate child group
    dflt_key_to_grp_li: Optional[dict[str, list]] = {}
    # defalut attribute key to the group set by reader
    dflt_key_to_exist_grp: Optional[dict[str, str]] = {}

    # "/abc[DATA]/XYe[anything]/mnf[MNYZ]/anything" -> ['DATA', 'anything', 'MNYZ']
    pattern = r"\[(.*?)\]"

    entry_data_rnd = ""
    for template_concept, val in template.items():
        # skip the last part which is field
        # Cancel out the fields and end groups without fields
        groups_list = template_concept.split("/")[0:-1]
        if not groups_list:
            continue
        last_default_key = ""
        if template_concept.endswith("/@default") and val:
            dflt_key_to_exist_grp[template_concept] = val
        # Skip the attributes other than default attribute
        elif bool(re.search(r".*/@.*$", template_concept)):
            continue

        for group in groups_list:
            if not group:
                continue
            modified_name = re.findall(pattern, group)
            if modified_name:
                modified_name = modified_name[0]
            else:
                modified_name = group
            # skip sttributes
            if modified_name.startswith("@"):
                continue
            last_default_atttr = f"{last_default_key}/@default"
            if not dflt_key_to_grp_li.get(last_default_atttr, None):
                dflt_key_to_grp_li[last_default_atttr] = {}
                # Data groups
                dflt_key_to_grp_li[last_default_atttr]["data"] = []
                # Entry groups
                dflt_key_to_grp_li[last_default_atttr]["entry"] = []
                # Other groups
                dflt_key_to_grp_li[last_default_atttr]["other"] = []

            if template_concept.endswith("/@default"):
                dflt_key_to_exist_grp[template_concept] = val

            # Entry
            if group.startswith("ENTRY"):
                dflt_key_to_grp_li[last_default_atttr]["entry"].append(modified_name)
            # Data
            elif group.startswith("DATA"):
                dflt_key_to_grp_li[last_default_atttr]["data"].append(modified_name)
                if not entry_data_rnd:
                    entry_data_rnd = modified_name
            else:
                dflt_key_to_grp_li[last_default_atttr]["other"].append(modified_name)

            last_default_key = last_default_key + "/" + group

    for deflt_key, value in dflt_key_to_grp_li.items():
        pre_defalt_grp = dflt_key_to_exist_grp.get(deflt_key, None)
        # Verify if user has added the group in default attribute
        if pre_defalt_grp:
            if (
                pre_defalt_grp in value["entry"]
                or pre_defalt_grp in value["data"]
                or pre_defalt_grp in value["other"]
            ):
                continue

        # Entry default group always a NXdata
        entry_default = "/entry/@default"
        if entry_default == deflt_key:
            template[entry_default] = entry_data_rnd
            continue

        if value["entry"]:
            template[deflt_key] = value["entry"][0]
        # Prioritize data group on other groups
        elif value["data"]:
            template[deflt_key] = value["data"][0]
            # Randomly choose a NXdata group for entry
        elif value["other"]:
            template[deflt_key] = value["other"][0]
        else:
            template[deflt_key] = ""
