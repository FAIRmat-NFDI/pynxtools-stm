#!/usr/bin/env python3
"""
A formatter that formats the STS (Scanning Tunneling Spectroscopy) experiment's raw data
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
from pynxtools_stm.configs.nanonis_dat_generic_sts import _nanonis_sts_dat_generic_5e
import pynxtools_stm.nxformatters.helpers as fhs
from pynxtools.dataconverter.template import Template
from pynxtools_stm.nxformatters.helpers import (
    _get_data_unit_and_others,
    _scientific_num_pattern,
    to_intended_t,
    get_link_compatible_key,
    replace_variadic_name_part,
)
import numpy as np


class NanonisDatSTS(SPMformatter):
    _grp_to_func = {
        "scan_region": "construct_scan_region_grp",
        # "TEMPERATURE_DATA[temperature_data]": "construct_temperature_data_grp",
        # "SCAN_DATA[scan_data]": "construct_scan_data_grp",
    }
    _axes = ["x", "y", "z"]

    def __init__(
        self,
        template: Template,
        raw_file: str | Path,
        eln_file: Dict,
        config_file: str = None,
        entry: str | None = None,
    ):
        super().__init__(template, raw_file, eln_file, config_file, entry)

    def _get_conf_dict(self, config_file: str = None):
        if config_file:
            return fhs.read_config_file(config_file)
        return _nanonis_sts_dat_generic_5e

    def _get_eln_dict(self, eln_file: str):
        # TODO: Implement this function
        raise NotImplementedError

    def get_nxformatted_template(self):
        self.work_though_config_nested_dict(self.config_dict, "")

    def construct_scan_region_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_region",
    ):
        # Note: This function is for 'scan_region' under the scan_control
        # and 'scan_region' from 'bias_spec_scan_control'

        # scan range e.g. raw data path "3.11737E-9;29.1583E-9;15E-9;15E-9;0E+0"
        # that consists [offset_x, offset_y, range_x, range_y, angle]
        if parent_path.endswith("bias_spec_scan_control"):
            scan_range = "scan_range_N[scan_range_n]"
            scan_ranges, unit, _ = _get_data_unit_and_others(
                data_dict=self.raw_data,
                partial_conf_dict=partial_conf_dict,
                concept_field=scan_range,
            )
        else:
            return

        gbl_scan_ranges = re.findall(_scientific_num_pattern, scan_ranges)
        gbl_scan_ranges = [float(x) for x in gbl_scan_ranges]
        scan_offset = gbl_scan_ranges[:2]
        scan_ranges = gbl_scan_ranges[2:4]
        scan_angles = gbl_scan_ranges[4:]
        if len(scan_angles) == 1:
            scan_angles = scan_angles * len(scan_ranges)
        # Angles unit
        scan_angle = "scan_angle_N[scan_angle_n]"
        _, ang_unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_angle,
        )
        for ind, off, rng, ang in enumerate(zip(scan_offset, scan_ranges, scan_angles)):
            off_key = f"{parent_path}/{group_name}/scan_offset_N[scan_offset_{self._axes[ind]}]"
            rng_key = (
                f"{parent_path}/{group_name}/scan_range_N[scan_range_{self._axes[ind]}]"
            )
            ang_key = (
                f"{parent_path}/{group_name}/scan_angle_N[scan_angle_{self._axes[ind]}]"
            )
            self.template[rng_key] = rng
            self.template[f"{rng_key}/@units"] = unit
            self.template[off_key] = off
            self.template[f"{off_key}/@units"] = unit
            self.template[ang_key] = ang
            self.template[f"{ang_key}/@units"] = ang_unit

            if self._axes[ind] == "x":
                self.NXScanControl.x_start = off
                self.NXScanControl.x_start_unit = unit
                self.NXScanControl.x_end = rng + off
                self.NXScanControl.x_end_unit = unit
            elif self._axes[ind] == "y":
                self.NXScanControl.y_start = off
                self.NXScanControl.y_start_unit = unit
                self.NXScanControl.y_end = rng + off
                self.NXScanControl.y_end_unit = unit

    def construct_temperature_data_grp(
        self,
        partial_conf_dict,  # TODO rename partial_conf_dict to partial_conf_dict_or_list everywhere
        parent_path: str,
        group_name="TEMPERATURE_DATA[temperature_data]",
    ):
        if isinstance(partial_conf_dict, list):
            for conf_dict in partial_conf_dict:
                self._NXdata__grp_from_conf_description(
                    conf_dict, parent_path, group_name
                )

    def construct_scan_data_grp(self, partial_conf_dict, parent_path: str, group_name):
        if isinstance(partial_conf_dict, list):
            for conf_dict in partial_conf_dict:
                self._NXdata__grp_from_conf_description(
                    conf_dict, parent_path, group_name
                )

    def _construct_nxscan_controllers(self, partial_conf_dict, parent_path, group_name):
        pass
