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
from pynxtools_stm.nxformatters.base_formatter import (
    SPMformatter,
    PINT_QUANTITY_MAPPING,
)
from typing import Dict
from pathlib import Path
from pint import UnitRegistry
import re
from pynxtools_stm.configs.nanonis_dat_generic_sts import _nanonis_sts_dat_generic_5e
import pynxtools_stm.nxformatters.helpers as fhs
from pynxtools.dataconverter.template import Template
from pynxtools_stm.nxformatters.helpers import (
    _get_data_unit_and_others,
    _scientific_num_pattern,
)
from pynxtools_stm.nxformatters.helpers import cal_dx_by_dy
import numpy as np

ureg = UnitRegistry()


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

    def get_nxformatted_template(self):
        self._format_template_from_eln()
        self.work_though_config_nested_dict(self.config_dict, "")

    def construct_scan_region_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_region",
    ):
        # Note: This function is for 'scan_region' under the scan_control
        # and 'scan_region' from 'bias_spec_scan_control' group

        # scan range e.g. raw data "3.11737E-9;29.1583E-9;15E-9;15E-9;0E+0"
        # that consists [offset_x, offset_y, range_x, range_y, angle]
        # if parent_path.endswith("bias_spec_scan_control"):
        #     scan_range = "scan_range_N[scan_range_n]"
        #     scan_ranges, unit, _ = _get_data_unit_and_others(
        #         data_dict=self.raw_data,
        #         partial_conf_dict=partial_conf_dict,
        #         concept_field=scan_range,
        #     )
        # else:
        #     return

        scan_range = "scan_range_N[scan_range_n]"
        scan_ranges, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_range,
        )
        if not scan_ranges:
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
            for ind, conf_dict in enumerate(partial_conf_dict):
                _ = self._NXdata_grp_from_conf_description(
                    conf_dict, parent_path, group_name, ind
                )

    def construct_scan_data_grp(self, partial_conf_dict, parent_path: str, group_name):
        if isinstance(partial_conf_dict, list):
            for ind, conf_dict in enumerate(partial_conf_dict):
                _ = self._NXdata_grp_from_conf_description(
                    conf_dict, parent_path, group_name, group_index=ind
                )

    def _construct_nxscan_controllers(self, partial_conf_dict, parent_path, group_name):
        pass

    def _construct_dI_dV_grp(self, IV_dict, parent_path, group_name):
        di_by_dv = cal_dx_by_dy(IV_dict["current_fld"], IV_dict["voltage_fld"])
        self.template[f"{parent_path}/{group_name}/dI_by_dV"] = di_by_dv
        self.template[f"{parent_path}/{group_name}/dI_by_dV/@units"] = str(
            ureg(IV_dict["current_unit"] + "/" + IV_dict["voltage_unit"]).units
        )
        self.template[f"{parent_path}/{group_name}/@signal"] = "dI_by_dV"
        axis = IV_dict["voltage_fld_name"]
        self.template[f"{parent_path}/{group_name}/@axes"] = [axis]
        self.template[f"{parent_path}/{group_name}/{axis}"] = IV_dict["voltage_fld"]
        self.template[f"{parent_path}/{group_name}/{axis}/@units"] = IV_dict[
            "voltage_unit"
        ]
        self.template[f"{parent_path}/{group_name}/@title"] = "dI by dV (Conductance)"

    def _NXdata_grp_from_conf_description(
        self, partial_conf_dict, parent_path, group_name, group_index=0
    ):
        group_name = super()._NXdata_grp_from_conf_description(
            partial_conf_dict, parent_path, group_name, group_index
        )

        if group_name is None:
            return
        current_group = {
            "current_fld": "",
            "current_unit": "",
            "current_fld_name": "",
            "voltage_fld": "",
            "voltage_unit": "",
            "voltage_fld_name": "",
        }
        current = False
        voltage = False
        # check if group is current group
        for key, val in self.template.items():
            if key.startswith(parent_path + "/" + group_name):
                if key.endswith("@units"):
                    current = (
                        PINT_QUANTITY_MAPPING.get(str(ureg(val).dimensionality))
                        == "current"
                        or current
                    )
                    if current and not current_group["current_unit"]:
                        current_group["current_unit"] = val
                        current_group["current_fld"] = self.template[key[0:-7]]
                        current_group["current_fld_name"] = key[0:-7].split("/")[-1]

                    voltage = (
                        PINT_QUANTITY_MAPPING.get(str(ureg(val).dimensionality))
                        == "voltage"
                        or voltage
                    )
                    if voltage and not current_group["voltage_unit"]:
                        current_group["voltage_unit"] = val
                        current_group["voltage_fld"] = self.template[key[0:-7]]
                        current_group["voltage_fld_name"] = key[0:-7].split("/")[-1]

                    if current and voltage:
                        group_name_grad = (
                            f"{group_name[0:-1]}_grad]"
                            if group_name[-1] == "]"
                            else f"{group_name}_grad"
                        )
                        self._construct_dI_dV_grp(
                            current_group, parent_path, group_name_grad
                        )

        return group_name
