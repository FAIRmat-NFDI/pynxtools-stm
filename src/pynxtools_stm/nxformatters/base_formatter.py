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
import pynxtools_stm.nxformatters.helpers as fhs
from pynxtools_stm.configs.nanonis_sxm_generic_stm import __config_stm_generic


@dataclass
class NXdata:
    grp_name: Optional[str] = ""
    signal: Optional[str] = None
    auxiliary_signals: Optional[List[str]] = None
    title: Optional[str] = None


# # Delte the NXscan_control class is not needed
# @dataclass
# class NXscan_control:
#     # TODO construct is later


class SPMformatter(ABC):
    def __init__(
        self,
        raw_file: Union[str, Path],
        eln_dict: Dict,
        config_file: str = None,  # Incase it is not provided by users
        # data_dict: Optional[Dict] = None,
        entry: Optional[str] = None,
    ):
        self.raw_file: Union[str, Path] = raw_file
        self.eln: Dict = eln_dict
        self.conf: Dict = self.__get_conf_dict(config_file)
        self.raw_data: Dict = self.get_raw_data_dict()
        self.entry: str = entry

    # def __anylize_raw_file(self):
    #     instrument_name: Optional[str] = None
    #     file_ext: Optional[str] = None
    #     vendor: Optional[str] = None
    #     vendor_software_version: Optional[str] = None

    #     return instrument_name, file_ext, vendor, vendor_software_version

    def __get_conf_dict(self, config_file: str = None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            return __config_stm_generic

    def get_raw_data_dict(self):
        SPMParser().get_raw_data_dict(self.raw_file, eln_dict=self.eln)

    def __arange_axes(self, direction="down"):
        if direction.lower() == "down":
            return ["-Y", "X"]
        elif direction.lower() == "up":
            return ["Y", "X"]
        elif direction.lower() == "right":
            return ["X", "Y"]
        elif direction.lower() == "left":
            return ["-X", "Y"]

    @abstractmethod
    def __construct_nxscan_controlers(self):
        ...
        # TODO: if NXscan_control is implementd please try to construct
        # scan_controller here

    # @abstractmethod
    # def __construct_nxlockin(self): ...
    # @abstractmethod
    # def __construct_nxdata(self):
    #     ...
    #     # TODO construct code here
