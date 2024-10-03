#!/usr/bin/env python3
"""
TODO: Add simple description of the module
"""

# -*- coding: utf-8 -*-
#
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
from abc import ABC, abstractmethod
from typing import Dict, Union, List, Optional
from pathlib import Path
from dataclasses import dataclass
from pynxtools_stm.parsers import SPMParser
from pynxtools.dataconverter.template import Template
from pynxtools_stm.nxformatters.helpers import (
    _get_data_unit_and_others,
    to_intended_t,
    replace_variadic_name_part,
)
import numpy as np

from pynxtools_stm.nxformatters.helpers import replace_variadic_name_part


@dataclass
class NXdata:
    grp_name: Optional[str] = ""
    signal: Optional[str] = None
    auxiliary_signals: Optional[List[str]] = None
    title: Optional[str] = None


class SPMformatter(ABC):
    # Map function to deal specific group. Map key should be the same as it is
    # in config file
    _grp_to_func = {}  # Placeholder
    _axes = []  # Placeholder

    # Class used to colleted data from several subgroups of ScanControl and reuse them
    # in the subgroups
    @dataclass
    class NXScanControl:  # TODO: Rename this class NXimageScanControl and create another class for BiasSpectroscopy
        # Put the class in the base_formatter.py under BaseFormatter class
        x_points = None
        y_points = None
        x_start = None
        x_start_unit = None
        y_start = None
        y_start_unit = None
        x_range = None
        y_range = None
        x_end = None
        x_end_unit = None
        y_end = None
        y_end_unit = None
        fast_axis = None  # lower case x, y
        slow_axis = None  # lower case x, y

    def __init__(
        self,
        template: Template,
        raw_file: Union[str, Path],
        eln_dict: Dict,
        config_file: str = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        self.template: Template = template
        self.raw_file: Union[str, Path] = raw_file
        self.eln: Dict = eln_dict
        self.raw_data: Dict = self.get_raw_data_dict()
        self.entry: str = entry
        self.config_dict = self._get_conf_dict(config_file) or None  # Placeholder

    @abstractmethod
    def _get_conf_dict(self, config_file: str = None): ...

    def work_though_config_nested_dict(self, config_dict: Dict, parent_path: str):
        for key, val in config_dict.items():
            if val is None or val == "":
                continue
            if key in self._grp_to_func:
                # First fill the default values
                self.work_though_config_nested_dict(
                    config_dict=val, parent_path=f"{parent_path}/{key}"
                )
                method = getattr(self, self._grp_to_func[key])
                method(val, parent_path, key)

            # end dict of the definition path that has raw_path key
            elif isinstance(val, dict) and "raw_path" in val:
                if "#note" in val:
                    continue
                data, unit, other_attrs = _get_data_unit_and_others(
                    data_dict=self.raw_data, end_dict=val
                )
                self.template[f"{parent_path}/{key}"] = to_intended_t(data)
                self.template[f"{parent_path}/{key}/@units"] = unit
                if other_attrs:
                    for k, v in other_attrs.items():
                        self.template[f"{parent_path}/{key}/@{k}"] = v
            # variadic fields that would have several values according to the dimentions
            elif isinstance(val, list) and isinstance(val[0], dict):
                for item in val:
                    part_to_embed, path_dict = (
                        item.popitem()
                    )  # Current only one item is valid
                    if "#note" in path_dict:
                        continue
                    data, unit, other_attrs = _get_data_unit_and_others(
                        data_dict=self.raw_data, end_dict=path_dict
                    )
                    temp_key = f"{parent_path}/{replace_variadic_name_part(key, part_to_embed=part_to_embed)}"
                    self.template[temp_key] = to_intended_t(data)
                    self.template[f"{temp_key}/@units"] = unit
                    if other_attrs:
                        for k, v in other_attrs.items():
                            self.template[f"{temp_key}/@{k}"] = v
            else:
                self.work_though_config_nested_dict(val, f"{parent_path}/{key}")

    def rearrange_data_according_to_axes(self, data):
        """Rearrange array data according to the fast and slow axes.

        Parameters
        ----------
        data : np.ndarray
            Two dimensional array data from scan.
        """
        if self.NXScanControl.fast_axis == "x":
            if self.NXScanControl.slow_axis == "-y":
                return np.flipud(data)
            return data
        elif self.NXScanControl.fast_axis == "-x":
            if self.NXScanControl.slow_axis == "y":
                return np.fliplr(data)
            elif self.NXScanControl.slow_axis == "-y":
                np.flip(data)
        elif self.NXScanControl.fast_axis == "-y":
            if self.NXScanControl.slow_axis == "x":
                return np.flipud(data)
            elif self.NXScanControl.slow_axis == "-x":
                return np.flip(data)
        elif self.NXScanControl.fast_axis == "y":
            if self.NXScanControl.slow_axis == "-x":
                return np.fliplr(data)
            return data

    def get_raw_data_dict(self):
        return SPMParser().get_raw_data_dict(self.raw_file, eln_dict=self.eln)

    def _arange_axes(self, direction="down"):
        fast_slow = None
        if direction.lower() == "down":
            fast_slow = ["-Y", "X"]
            self.NXScanControl.fast_axis = fast_slow[0].lower()
            self.NXScanControl.slow_axis = fast_slow[1].lower()
        elif direction.lower() == "up":
            fast_slow = ["Y", "X"]
            self.NXScanControl.fast_axis = fast_slow[0].lower()
            self.NXScanControl.slow_axis = fast_slow[1].lower()
        elif direction.lower() == "right":
            fast_slow = ["X", "Y"]
            self.NXScanControl.fast_axis = fast_slow[0].lower()
            self.NXScanControl.slow_axis = fast_slow[1].lower()
        elif direction.lower() == "left":
            fast_slow = ["-X", "Y"]
            self.NXScanControl.fast_axis = fast_slow[0].lower()
            self.NXScanControl.slow_axis = fast_slow[1].lower()

        return fast_slow

    @abstractmethod
    def get_nxformatted_template(self): ...

    @abstractmethod
    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name: str,
        *arg,
        **kwarg,
    ): ...

    def _NXdata__grp_from_conf_description(
        self, partial_conf_dict, parent_path: str, group_name: str
    ):
        """Example NXdata dict descrioption from config
        {
            "data": {
                "name": "temperature1(filter)",
                "raw_path": "/dat_mat_components/Temperature 1 [filt]/value",
                "@units": "/dat_mat_components/Temperature 1 [filt]/unit",
            },
            "0": {
                "name": "Bias Voltage",
                "raw_path": [
                    "/dat_mat_components/Bias calc/value",
                    "/dat_mat_components/Bias/value",
                ],
                "@units": [
                    "/dat_mat_components/Bias calc/unit",
                    "/dat_mat_components/Bias/unit",
                ],
                "axis_ind": 0,
            },
            "title": "Bias Spectroscopy Temperature1(filter)",
            "grp_name": "temperature1(filter)",
        }

        "data" -> Signal data of "temperature1(filter)" denoted by
                  the name key.
        "0" -> Index of the axis if "axis_ind" is not provided.
                Here both are same. Name of the axis is denotec
                by the name key.
        "title" -> Title of the main plot.
        "grp_name" -> Name of the NXdata group.

        To get the proper relation please visit:
        """
        grp_name_to_embed = partial_conf_dict.get("grp_name", "")
        nxdata_group = replace_variadic_name_part(group_name, grp_name_to_embed)
        data_dict = partial_conf_dict.get("data")
        nxdata_nm = data_dict.pop("name", "").replace(" ", "_")
        nxdata_d_arr, d_unit, d_others = _get_data_unit_and_others(
            self.raw_data, end_dict=data_dict
        )

        nxdata_title = partial_conf_dict.get("title")
        nxdata_axes = []
        nxdata_indices = []
        axdata_unit_other_list = []
        for key, val in partial_conf_dict.items():
            if key == "data":
                continue
            if isinstance(val, dict):
                try:
                    index = int(key)
                except ValueError:
                    continue
                nxdata_axes.append(val.pop("name", "").replace(" ", "_"))
                index = val.pop("axis_ind", index)
                nxdata_indices.append(index)
                axdata_unit_other_list.append(
                    _get_data_unit_and_others(self.raw_data, end_dict=val)
                )

        self.template[f"{parent_path}/{nxdata_group}/@title"] = nxdata_title
        self.template[f"{parent_path}/{nxdata_group}/{nxdata_nm}"] = nxdata_d_arr
        self.template[f"{parent_path}/{nxdata_group}/{nxdata_nm}/@units"] = d_unit
        self.template[f"{parent_path}/{nxdata_group}/{nxdata_nm}/@long_name"] = (
            f"{nxdata_nm} ({d_unit})"
        )
        self.template[f"{parent_path}/{nxdata_group}/@signal"] = nxdata_nm
        if d_others:
            for k, v in d_others.items():
                self.template[f"{parent_path}/{nxdata_group}/{nxdata_nm}/@{k}"] = v
        self.template[f"{parent_path}/{nxdata_group}/@axes"] = nxdata_axes

        for ind, index, axis in enumerate(zip(nxdata_indices, nxdata_axes)):
            self.template[f"{parent_path}/{nxdata_group}/@{axis}_indices"] = index
            self.template[f"{parent_path}/{nxdata_group}/{axis}"] = (
                axdata_unit_other_list[ind][0]
            )
            unit = axdata_unit_other_list[ind][1]
            self.template[f"{parent_path}/{nxdata_group}/{axis}/@units"] = unit
            self.template[f"{parent_path}/{nxdata_group}/{axis}/@long_name"] = (
                f"{axis} ({unit})"
            )
            if axdata_unit_other_list[ind][2]:
                for k, v in axdata_unit_other_list[ind][2].items():
                    self.template[f"{parent_path}/{nxdata_group}/{axis}/@{k}"] = v
