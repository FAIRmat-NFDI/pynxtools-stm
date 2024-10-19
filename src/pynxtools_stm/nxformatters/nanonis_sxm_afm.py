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
from typing import Dict, Optional, Union, TYPE_CHECKING
from pathlib import Path
import itertools
from pynxtools_stm.nxformatters.nanonis_sxm_stm import NanonisSxmSTM
from dataclasses import dataclass
import re
from pynxtools_stm.configs.nanonis_sxm_generic_afm import _nanonis_afm_sxm_generic_5e
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

if TYPE_CHECKING:
    from pynxtools.dataconverter.template import Template


# TODO: Try to replace the upper version group, field and attributes
# with search method from regrex (e.g. SCAN_DATA[...]). This will help
# to search the group and field of overwritten name.

# TODO: add test to check if user example config file is the same as given default
# config file with this package.
# TODO: Check why link to NXdata does not work
# # Create links for NXdata in entry level
# entry = parent_path.split("/")[1]
# print("##### NXdata]", f"/{entry}/DATA[{field_nm}]")
# self.template[f"/{entry}/{field_nm}"] = {
#     "link": get_link_compatible_key(f"{parent_path}/{group_name}")
# }


class NanonisSxmAFM(NanonisSxmSTM, SPMformatter):
    _grp_to_func = {
        "SCAN_CONTROL[scan_control]": "_construct_nxscan_controllers",
    }
    _axes = ["x", "y", "z"]

    def __init__(
        self,
        # TODO: fix the type of template
        template: "Template",
        raw_file: Union[str, Path],
        eln_file: Dict,
        config_file: str = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        super().__init__(template, raw_file, eln_file, config_file, entry)
        # # self.config_dict: Dict = self._get_conf_dict(config_file)
        # self.nanonis_sxm_stm = NanonisSxmSTM(self.template, self.raw_file, eln_file)
        # # Use AFM specific config file and the resulting dict
        # self.nanonis_sxm_stm.config_dict = self.config_dict

    def get_nxformatted_template(self):
        self.work_though_config_nested_dict(self.config_dict, "")
        self._format_template_from_eln()

    def _get_conf_dict(self, config_file: str = None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            return _nanonis_afm_sxm_generic_5e

    def construct_scan_pattern_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_mesh",
    ):
        """To construct the scan pattern like scan_mesh, scan_spiral (group) etc."""
        # The config file for afm is exactly the same as for stm
        super().construct_scan_pattern_grp(
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )
        # self.nanonis_sxm_stm.construct_scan_pattern_grp(
        #     partial_conf_dict=partial_conf_dict,
        #     parent_path=parent_path,
        #     group_name=group_name,
        # )

    def construct_scan_region_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_region",
    ):
        """To construct the scan region like scan_region."""
        # The config file for afm is exactly the same as for stm
        super().construct_scan_region_grp(
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )
        # # The config file for afm is exactly the same as for stm
        # self.nanonis_sxm_stm.construct_scan_region_grp(
        #     partial_conf_dict=partial_conf_dict,
        #     parent_path=parent_path,
        #     group_name=group_name,
        # )

    def construct_single_scan_data_grp(self, parent_path, plot_data_info, group_name):
        """To construct the scan data like scan_data."""
        # The config file for afm is exactly the same as for stm
        super().construct_single_scan_data_grp(
            parent_path=parent_path,
            plot_data_info=plot_data_info,
            group_name=group_name,
        )
        # self.nanonis_sxm_stm.construct_single_scan_data_grp(
        #     parent_path=parent_path,
        #     plot_data_info=plot_data_info,
        #     group_name=group_name,
        # )

    def construct_scan_data_grps(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="SCAN_DATA[scan_data]",
    ):
        """To construct the scan data like scan_data."""

        # The config file for afm is exactly the same as for stm
        super().construct_scan_data_grps(
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )

        # self.nanonis_sxm_stm.construct_scan_data_grps(
        #     partial_conf_dict=partial_conf_dict,
        #     parent_path=parent_path,
        #     group_name=group_name,
        # )

    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_control",
    ):
        """To construct the scan control like scan_control."""
        # The config file for afm is exactly the same as for stm
        super()._construct_nxscan_controllers(
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )

        # self.nanonis_sxm_stm._construct_nxscan_controllers(
        #     partial_conf_dict=partial_conf_dict,
        #     parent_path=parent_path,
        #     group_name=group_name,
        # )
