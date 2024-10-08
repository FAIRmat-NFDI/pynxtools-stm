#!/usr/bin/env python3
"""
A formatter that formats the STM (Scanning Tunneling Microscopy) experiment's raw data
to NeXus application definition NXstm.
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

from pynxtools_stm.nxformatters.base_formatter import SPMformatter
from typing import Dict, Optional, Union
from pathlib import Path
import itertools
from dataclasses import dataclass
import re
from pynxtools_stm.configs.nanonis_sxm_generic_stm import _nanonis_stm_sxm_generic_5e
import pynxtools_stm.nxformatters.helpers as fhs
from typing import TYPE_CHECKING
from pynxtools_stm.nxformatters.helpers import (
    _get_data_unit_and_others,
    _scientific_num_pattern,
    to_intended_t,
    get_link_compatible_key,
    replace_variadic_name_part,
)
import numpy as np

if TYPE_CHECKING:
    from pynxtools.dataconverter.template import Template

# TODO: add test to check if user example config file is the same as given default
# config file with this package.
# TODO: Check why link to NXdata does not work
# # Create links for NXdata in entry level
# entry = parent_path.split("/")[1]
# print("##### NXdata]", f"/{entry}/DATA[{field_nm}]")
# self.template[f"/{entry}/{field_nm}"] = {
#     "link": get_link_compatible_key(f"{parent_path}/{group_name}")
# }


class NanonisSxmSTM(SPMformatter):
    _grp_to_func = {
        "SCAN_CONTROL[scan_control]": "_construct_nxscan_controllers",
    }
    _axes = ["x", "y", "z"]

    def __init__(
        self,
        template: "Template",
        raw_file: Union[str, Path],
        eln_dict: Dict,
        config_file: str = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        super().__init__(template, raw_file, eln_dict, config_file, entry)
        # self.config_dict: Dict = self._get_conf_dict(config_file)

    def get_nxformatted_template(self):
        self.work_though_config_nested_dict(self.config_dict, "")

    def _get_conf_dict(self, config_file: str = None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            return _nanonis_stm_sxm_generic_5e

    def construct_scan_pattern_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_mesh",
    ):
        """To construct the scan pattern like scan_mesh, scan_spiral (group) etc."""

        # Scanner speed
        forward_speed_k = "forward_speed_N[forward_speed_n]"
        forward_speed, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=forward_speed_k,
        )
        self.template[
            f"{parent_path}/{group_name}/forward_speed_N[forward_speed_{self.NXScanControl.fast_axis}]"
        ] = to_intended_t(forward_speed)
        self.template[
            f"{parent_path}/{group_name}/forward_speed_N[forward_speed_{self.NXScanControl.fast_axis}]/@units"
        ] = unit
        backward_speed_k = "backward_speed_N[backward_speed_n]"
        backward_speed, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=backward_speed_k,
        )
        self.template[
            f"{parent_path}/{group_name}/backward_speed_N[backward_speed_{self.NXScanControl.fast_axis}]"
        ] = to_intended_t(backward_speed)
        self.template[
            f"{parent_path}/{group_name}/backward_speed_N[backward_speed_{self.NXScanControl.fast_axis}]/@units"
        ] = unit

        # scan_point fields
        scan_point = "scan_points_N[scan_points_n]"

        scan_points, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,  # dict that contains concept field
            concept_field=scan_point,
        )
        gbl_scan_points = re.findall(_scientific_num_pattern, scan_points)
        if gbl_scan_points:
            gbl_scan_points = [float(x) for x in gbl_scan_points]
        for ind, point in enumerate(gbl_scan_points):
            self.template[
                f"{parent_path}/{group_name}/scan_points_N[scan_points_{self._axes[ind]}]"
            ] = point
            if self._axes[ind] == "x":
                self.NXScanControl.x_points = point
            elif self._axes[ind] == "y":
                self.NXScanControl.y_points = point
        # step_size
        if len(gbl_scan_points) == len(gbl_scan_ranges):
            for ind, (rng, pnt) in enumerate(zip(gbl_scan_ranges, gbl_scan_points)):
                stp_s = f"{parent_path}/{group_name}/step_size_N[step_size_{self._axes[ind]}]"
                self.template[stp_s] = rng / pnt
                self.template[stp_s + "/@units"] = unit

        # scan_data group
        scan_data = "SCAN_DATA[scan_data]"
        self.construct_scan_data_grps(
            partial_conf_dict=partial_conf_dict[scan_data],
            parent_path=f"{parent_path}/{group_name}",
            group_name=scan_data,
        )

    def construct_scan_region_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_region",
    ):
        scan_offset = "scan_offset_N[scan_offset_n]"

        scan_offsets, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_offset,
        )
        scan_offsets = to_intended_t(re.findall(_scientific_num_pattern, scan_offsets))
        for ind, offset in enumerate(scan_offsets):
            off_key = f"{parent_path}/{group_name}/scan_offset_N[scan_offset_{self._axes[ind]}]"
            self.template[off_key] = offset
            self.template[f"{off_key}/@units"] = unit
            if self._axes[ind] == "x":
                self.NXScanControl.x_start = offset
                self.NXScanControl.x_start_unit = unit
            elif self._axes[ind] == "y":
                self.NXScanControl.y_start = offset
                self.NXScanControl.y_start_unit = unit

        # Scan Angle
        scan_angle = "scan_angle_N[scan_angle_n]"

        scan_angles, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_angle,
        )
        scan_angles = to_intended_t(re.findall(_scientific_num_pattern, scan_angles))
        for ind, angle in enumerate(scan_angles):
            ang_key = (
                f"{parent_path}/{group_name}/scan_angle_N[scan_angle_{self._axes[ind]}]"
            )
            self.template[ang_key] = angle
            self.template[f"{ang_key}/@units"] = unit

        # scan range
        scan_range = "scan_range_N[scan_range_n]"
        scan_ranges, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_range,
        )
        global gbl_scan_ranges
        gbl_scan_ranges = re.findall(_scientific_num_pattern, scan_ranges)
        if gbl_scan_ranges:
            gbl_scan_ranges = [float(x) for x in gbl_scan_ranges]

        for ind, rng in enumerate(gbl_scan_ranges):
            rng_key = (
                f"{parent_path}/{group_name}/scan_range_N[scan_range_{self._axes[ind]}]"
            )
            self.template[rng_key] = rng
            self.template[f"{rng_key}/@units"] = unit

            if self._axes[ind] == "x" and self.NXScanControl.x_start is not None:
                self.NXScanControl.x_end = rng + self.NXScanControl.x_start
                self.NXScanControl.x_end_unit = unit
            elif self._axes[ind] == "y" and self.NXScanControl.y_start is not None:
                self.NXScanControl.y_end = rng + self.NXScanControl.y_start
                self.NXScanControl.y_end_unit = unit

            self.template[
                f"{parent_path}/{group_name}/scan_range__N[scan_range_{self._axes[ind]}]/@units"
            ] = unit

    def construct_single_scan_data_grp(self, parent_path, plot_data_info, group_name):
        raw_key = plot_data_info["data_path"]
        axes = ["x", "y"]
        field_nm = raw_key[1:].replace("/", "_").lower()
        group_name = group_name.replace("scan_data", field_nm)
        self.template[f"{parent_path}/{group_name}/@signal"] = field_nm
        self.template[f"{parent_path}/{group_name}/@axes"] = axes
        title = raw_key[1:].replace("/", " ").upper()
        self.template[f"{parent_path}/{group_name}/title"] = title

        # data field
        f_data = to_intended_t(self.raw_data[raw_key])
        self.template[f"{parent_path}/{group_name}/{field_nm}"] = (
            self.rearrange_data_according_to_axes(f_data)
        )
        self.template[f"{parent_path}/{group_name}/{field_nm}/@units"] = plot_data_info[
            "units"
        ]
        calibration = to_intended_t(plot_data_info.get("calibration", None))
        self.template[f"{parent_path}/{group_name}/{field_nm}/@calibration"] = (
            calibration
        )
        offset = to_intended_t(plot_data_info.get("offset", None))
        self.template[f"{parent_path}/{group_name}/{field_nm}/@offset"] = offset
        # x and y axis
        self.template[f"{parent_path}/{group_name}/x"] = plot_data_info["x_axis"]
        x_unit = plot_data_info["x_units"]
        self.template[f"{parent_path}/{group_name}/x/@units"] = x_unit
        self.template[f"{parent_path}/{group_name}/x/@long_name"] = f"X ({x_unit})"
        self.template[f"{parent_path}/{group_name}/y"] = plot_data_info["y_axis"]
        y_unit = plot_data_info["y_units"]
        self.template[f"{parent_path}/{group_name}/y/@units"] = y_unit
        self.template[f"{parent_path}/{group_name}/y/@long_name"] = f"Y ({y_unit})"

    def construct_scan_data_grps(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="SCAN_DATA[scan_data]",
    ):
        # create multiple groups for scan_data for multiple scans
        data, _, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            end_dict=partial_conf_dict,
        )
        # Example of data des and info and each column is separated by tab
        # Channel	Name	Unit	Direction	Calibration	Offset
        # 14	Z	m	both	9.000E-9	0.000E+0
        # 0	Current	A	both	1.000E-9	-1.132E-13
        data_headers = [dt.strip().split("\t") for dt in data.split("\n")]

        expected_keys = [
            "Channel",
            "Name",
            "Unit",
            "Direction",
            "Calibration",
            "Offset",
        ]
        plot_data_list = []
        for ind, row in enumerate(data_headers):
            if ind == 0 and expected_keys != row:
                raise ValueError(
                    f"Scan data mismatch: Expected keys {expected_keys} but got {row}"
                )
            if ind > 0 and len(row) == len(expected_keys):
                if row[3] == "both":
                    data_key_f = f"/{row[1]}/forward"
                    data_key_b = f"/{row[1]}/backward"
                    plot_data_list = plot_data_list + (
                        [
                            {
                                "data_path": data_key_f,
                                "units": row[2],
                                "calibration": row[4],
                                "offset": row[5],
                                "x_axis": np.linspace(
                                    self.NXScanControl.x_start,
                                    self.NXScanControl.x_end,
                                    int(self.NXScanControl.x_points),
                                ),
                                "x_units": row[2],
                                "y_axis": np.linspace(
                                    self.NXScanControl.y_start,
                                    self.NXScanControl.y_end,
                                    int(self.NXScanControl.y_points),
                                ),
                                "y_units": row[2],
                            },
                            {
                                "data_path": data_key_b,
                                "units": row[2],
                                "calibration": row[4],
                                "offset": row[5],
                                "x_axis": np.linspace(
                                    self.NXScanControl.x_start,
                                    self.NXScanControl.x_end,
                                    int(self.NXScanControl.x_points),
                                ),
                                "x_units": row[2],
                                "y_axis": np.linspace(
                                    self.NXScanControl.y_start,
                                    self.NXScanControl.y_end,
                                    int(self.NXScanControl.y_points),
                                ),
                                "y_units": row[2],
                            },
                        ]
                    )
                else:
                    data_key = f"/{row[1]}/forward"
                    plot_data_list.append(
                        {
                            "data_path": data_key,
                            "units": row[2],
                            "calibration": row[4],
                            "offset": row[5],
                            "x_axis": np.linspace(
                                self.NXScanControl.x_start,
                                self.NXScanControl.x_end,
                                int(self.NXScanControl.x_points),
                            ),
                            "x_units": row[2],
                            "y_axis": np.linspace(
                                self.NXScanControl.y_start,
                                self.NXScanControl.y_end,
                                int(self.NXScanControl.y_points),
                            ),
                            "y_units": row[2],
                        }
                    )
        for plot_data_info in plot_data_list:
            self.construct_single_scan_data_grp(
                parent_path=parent_path,
                plot_data_info=plot_data_info,
                group_name=group_name,
            )

    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_control",
    ):
        # find independent_scan_axes
        # independent_axes = "/ENTRY[entry]/experiment_instrument/scan_environment/SCAN_CONTROL[scan_control]/independent_scan_axes"
        independent_axes = "independent_scan_axes"
        direction, _, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=independent_axes,
        )
        direction = self._arange_axes(direction.strip())
        self.template[f"{parent_path}/{group_name}/independent_scan_axes"] = str(
            direction
        )
        scan_region_grp = "scan_region"
        scan_region_dict = partial_conf_dict.get(scan_region_grp, None)
        # Intended order: construct_scan_region_grp
        if scan_region_dict is not None:
            self.construct_scan_region_grp(
                partial_conf_dict=scan_region_dict,
                parent_path=f"{parent_path}/{group_name}",
                group_name=scan_region_grp,
            )
        scan_pattern_grp = "mesh_SCAN[mesh_scan]"
        scan_pattern_dict = partial_conf_dict.get(scan_pattern_grp, None)
        if scan_pattern_dict is not None:
            self.construct_scan_pattern_grp(
                partial_conf_dict=scan_pattern_dict,
                parent_path=f"{parent_path}/{group_name}",
                group_name=scan_pattern_grp,
            )
