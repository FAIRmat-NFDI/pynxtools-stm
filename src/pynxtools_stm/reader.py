"""
A short description on STS reader which also suitable for file from STM .
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
#

import json
from typing import Dict, Union, Tuple, Any, Optional
import numpy as np
import yaml
import copy

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.utils import FlattenSettings, flatten_and_replace
from pynxtools.dataconverter.template import Template
from pynxtools import get_nexus_version
# from pynxtools_stm.helper import set_default_attr_in_group


CONVERT_DICT = {
    "Instrument": "INSTRUMENT[instrument]",
    "Environment": "ENVIRONMENT[environment]",
    "Sample_bias": "SAMPLE_BIAS[sample_bias]",
    "unit": "@units",
    "version": "@version",
    "default": "@default",
    "Sample": "SAMPLE[sample]",
    "User": "USER[user]",
    "Data": "DATA[data]",
    "Source": "SOURCE[source]",
}
# For flatened key-value pair from nested dict.
REPLACE_NESTED: Dict[str, str] = {}


def manually_filter_data_type(template):
    """Check for the data with key type and fix it"""
    nexus_key_to_dt = {
        "/ENTRY[entry]/INSTRUMENT[instrument]/ENVIRONMENT[environment]/current_sensor/current_gain": float,
    }
    template_copy = copy.deepcopy(template)
    for key, val in template_copy.items():
        dt = nexus_key_to_dt.get(key, None)
        if dt:
            try:
                template[key] = dt(val)
            except (ValueError, TypeError):
                del template[key]


# pylint: disable=invalid-name, too-few-public-methods
class SPMReader(BaseReader):
    """Reader for XPS."""

    supported_nxdls = ["NXstm"]

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ):
        """
        General read menthod to prepare the template.
        """
        filled_template: Union[Dict, None] = Template()
        eln_dict: Union[Dict[str, Any], None] = None
        config_file: Optional[str] = None
        data_file: Optional[str] = ""
        experirment_type: Optional[str] = None
        raw_file_ext: Optional[str] = None

        for file in file_paths:
            ext = file.rsplit(".", 1)[-1]
            fl_obj: object
            if ext in ["sxm", "dat"]:
                data_file = file
                raw_file_ext = ext
            if ext == "json":
                config_file = file
            if ext in ["yaml", "yml"]:
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    eln_dict = flatten_and_replace(
                        FlattenSettings(
                            yaml.safe_load(fl_obj), CONVERT_DICT, REPLACE_NESTED
                        )
                    )
        # TODO: Get experiment type from eln, so include `experiment_type`
        # in application definition
        experirment_type = "stm"
        # Get callable object that has parser inside
        if experirment_type == "stm" and raw_file_ext == "sxm":
            from pynxtools_stm.nxformatters.nanonnis_sxm_stm import NanonisSXMSTM

            nss = NanonisSXMSTM(
                template=template,
                raw_file=data_file,
                eln_dict=eln_dict,
                config_file=config_file,
            )
            nss.get_nxformatted_template()

        # set_default_attr_in_group(template)

        # manually_filter_data_type(template)
        for key, val in template.items():
            if isinstance(val, np.ndarray):
                filled_template[key] = val
                continue
            elif val in (None, ""):
                continue

            filled_template[key] = val
        # Set nexus def version
        filled_template["/ENTRY[entry]/definition/@version"] = get_nexus_version()

        if not filled_template.keys():
            raise ValueError(
                "Reader could not read anything! Check for input files and the"
                " corresponding extention."
            )

        return filled_template


READER = SPMReader
