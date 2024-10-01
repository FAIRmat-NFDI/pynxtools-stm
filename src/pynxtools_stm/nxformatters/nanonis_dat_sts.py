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
    _grp_to_func = {}
    _axes = ["x", "y", "z"]

    def __init__(
        self,
        template: Template,
        raw_file: str | Path,
        eln_dict: Dict,
        config_file: str = None,
        entry: str | None = None,
    ):
        super().__init__(template, raw_file, eln_dict, config_file, entry)

    def _get_conf_dict(self, config_file: str = None):
        if config_file:
            return fhs.read_config_file(config_file)
        return _nanonis_sts_dat_generic_5e

    def get_nxformatted_template(self):
        self.work_though_config_nested_dict(self.config_dict, "")
    
    def 
