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
from collections.abc import Callable
from typing import Dict, Union, Tuple, Any, Optional
import yaml
import re
import copy

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.readers.utils import FlattenSettings, flatten_and_replace
from pynxtools.dataconverter.template import Template
from pynxtools import get_nexus_version

from pynxtools_stm.stm_file_parser import STM_Nanonis
from pynxtools_stm.sts_file_parser import from_dat_file_into_template

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


# pylint: disable=too-few-public-methods
class StmNanonisGeneric:
    """Class to handle 'stm' experiment of software version 'Generic 5e' from 'nanonis'
    vendor.
    """

    __version__ = ["Generic 5e", "Generic 4.5"]

    def __call__(
        self, template: Dict, data_file: str, config_dict: str, eln_dict: Dict
    ) -> None:
        """Convert class instace as a callable function.

        Parameters
        ----------
        template : Dict
            Template that will be filled.
        data_file : str
            The file from experiment
        config_dict : str
            Config file to map application definition to the raw file
        eln_dict : Dict
            user provided dict
        """

        STM_Nanonis(file_name=data_file).from_sxm_file_into_template(
            template, config_dict, eln_dict
        )


# pylint: disable=too-few-public-methods
class StsNanonisGeneric:
    """Class to handle 'sts' experiment of software version 'Generic 5e' from 'nanonis'
    vendor.
    """

    __version__ = ["Generic 5e", "Generic 4.5"]

    def __call__(
        self, template: Dict, data_file: str, config_dict: Dict, eln_dict: Dict
    ) -> None:
        """Convert class instace as callable a function.

        Parameters
        ----------
        template : Dict
            Template that will be filled.
        data_file : str
            The file from experiment
        config_dict : str
            Config file to map application definition to the raw file
        eln_dict : Dict
            user provided dict
        """
        from_dat_file_into_template(template, data_file, config_dict, eln_dict)


# pylint: disable=too-few-public-methods
class Spm:
    """This class is intended for taking care of vendor's name,
    experiment (stm, sts, afm) and software versions.

    Raises
    ------
    ValueError
        If experiment is not in ['sts', 'stm', 'afm']
    ValueError
        if vendor's name is not in ['nanonis']
    ValueError
        if software version is not in ['Generic 5e', 'Generic 4.5']
    """

    # parser navigate type
    par_nav_t = Dict[str, Union["par_nav_t", Callable]]
    __parser_navigation: Dict[str, par_nav_t] = {
        "stm": {
            "nanonis": {
                "Generic 5e": StmNanonisGeneric,
                "Generic 4.5": StmNanonisGeneric,
            }
        },
        "sts": {
            "nanonis": {
                "Generic 5e": StsNanonisGeneric,
                "Generic 4.5": StsNanonisGeneric,
            }
        },
    }

    def get_appropriate_parser(self, eln_dict: Dict) -> Callable:
        """Search for appropriate prser and pass it the reader.

        Parameters
        ----------
        eln_dict : str
            User provided eln file (yaml) that must contain all the info about
            experiment, vendor's name and version of the vendor's software.

        Returns
        -------
            Return callable function that has capability to run the correponding parser.
        """

        experiment_t_key: str = "/ENTRY[entry]/experiment_type"
        experiment_t: str = eln_dict[experiment_t_key]
        try:
            experiment_dict: Spm.par_nav_t = self.__parser_navigation[experiment_t]
        except KeyError as exc:
            raise KeyError(
                f"Add correct experiment type in ELN file "
                f" from {list(self.__parser_navigation.keys())}."
            ) from exc

        vendor_key: str = "/ENTRY[entry]/INSTRUMENT[instrument]/software/vendor"
        vendor_n: str = eln_dict[vendor_key]
        try:
            vendor_dict: Spm.par_nav_t = experiment_dict[vendor_n]  # type: ignore[assignment]
        except KeyError as exc:
            raise KeyError(
                f"Add correct vendor name in ELN file "
                f" from {list(experiment_dict.keys())}."
            ) from exc

        software_v_key: str = (
            "/ENTRY[entry]/INSTRUMENT[instrument]/software/model/@version"
        )
        software_v: str = eln_dict[software_v_key]
        try:
            parser_cls: Callable = vendor_dict[software_v]  # type: ignore[assignment]
            # cls instance
            parser = parser_cls()
        except KeyError as exc:
            raise KeyError(
                f"Add correct software version in ELN file "
                f" from {list(vendor_dict.keys())}."
            ) from exc

        # Return callable function
        return parser


def set_default_for_each_group(template):
    """Set default attribute for each group of Nexus file.
    Each group will have a /@default attrubute refering the immediate child group or field in a NeXus definition chain.
    e.g. /@default = "entry1"
        /entry1/data/@default = "field1"

    Parameters
    ----------
    template : Template
        Template from filled with datafile and eln.
    """
    # defalut attribute key to the list of immediate child group
    dflt_key_to_grp_li: Optional[dict[str, list]] = {}
    # defalut attribute key to the group set by reader
    dflt_key_to_exist_grp: dict[str, str] = {}

    # "/abc[DATA]/XYe[anything]/mnf[MNYZ]/anything" -> ['DATA', 'anything', 'MNYZ']
    pattern = r"\[(.*?)\]"

    entry_data_rnd = ""
    for template_concept, val in template.items():
        # skip the last part which is field
        groups_list = template_concept.split("/")
        # Cancel out the attribuutes
        if groups_list[-1].startswith("@"):
            continue
        # Cancel out the fields
        groups_list = groups_list[0:-1]
        if not groups_list:
            continue
        last_default_key = ""
        if template_concept.endswith("/@default") and val:
            dflt_key_to_exist_grp[template_concept] = val

        for group in groups_list:
            if not group:
                continue
            modified_name = re.findall(pattern, group)
            if modified_name:
                modified_name = modified_name[0]
            else:
                modified_name = group
            if modified_name.startswith("@"):
                continue
            last_default_atttr = f"{last_default_key}/@default"
            if not dflt_key_to_grp_li.get(last_default_atttr, None):
                dflt_key_to_grp_li[last_default_atttr] = {}
                # Data groups
                dflt_key_to_grp_li[last_default_atttr]["data"] = []
                dflt_key_to_grp_li[last_default_atttr]["entry"] = []
                # Other groupa
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
        # Verify if user added the group here
        if not pre_defalt_grp:
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
class STMReader(BaseReader):
    """Reader for XPS."""

    supported_nxdls = ["NXsts"]

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ):
        """
        General read menthod to prepare the template.
        """
        # has_sxm_file: bool = False
        # sxm_file: str = ""
        # has_dat_file: bool = False
        # dat_file: str = ""
        filled_template: Union[Dict, None] = Template()
        # config_dict: Union[Dict[str, Any], None] = None
        eln_dict: Union[Dict[str, Any], None] = None
        config_dict: Dict = {}

        data_file: str = ""
        for file in file_paths:
            ext = file.rsplit(".", 1)[-1]
            fl_obj: object
            if ext in ["sxm", "dat"]:
                data_file = file
            if ext == "json":
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    config_dict = json.load(fl_obj)
            if ext in ["yaml", "yml"]:
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    eln_dict = flatten_and_replace(
                        FlattenSettings(
                            yaml.safe_load(fl_obj), CONVERT_DICT, REPLACE_NESTED
                        )
                    )
        # Get callable object that has parser inside
        parser = Spm().get_appropriate_parser(eln_dict)
        parser(template, data_file, config_dict, eln_dict)

        # set_default_for_each_group(template)
        manually_filter_data_type(template)
        for key, val in template.items():
            if val is not None:
                filled_template[key] = val
        # Set nexus def version
        filled_template["/ENTRY[entry]/definition/@version"] = get_nexus_version()

        if not filled_template.keys():
            raise ValueError(
                "Reader could not read anything! Check for input files and the"
                " corresponding extention."
            )

        return filled_template


READER = STMReader
