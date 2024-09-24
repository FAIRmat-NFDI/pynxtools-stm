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
#

from typing import Dict, Union, Callable, Optional, Iterable, Any
from pynxtools_stm.parsers.nanonis_sxm import SXMGenericNanonis
import pynxtools_stm.parsers.helpers as phs
from pathlib import Path, PosixPath
import os


class SPMParser:
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
        "sxm": {
            "nanonis": {
                "Generic 5e": SXMGenericNanonis,
                "Generic 4.5": SXMGenericNanonis,
            }
        },
        "dat": {
            "nanonis": {
                "Generic 5e": "StsNanonisGeneric",
                "Generic 4.5": "StsNanonisGeneric",
            }
        },
    }

    def __get_appropriate_parser(
        self,
        file: Union[str, Path],
        eln_dict: Dict = {},
        file_ext: Optional[str] = None,
    ) -> Iterable[Callable]:
        """Search for appropriate prser and pass it the reader.

        Parameters
        ----------
        eln_dict : Dict
            User provided eln file (yaml) that must contain all the info about
            experiment, vendor's name and version of the vendor's software.

        Returns
        -------
            Return callable function that has capability to run the correponding parser.
        """
        if file_ext is None:
            if file is None:
                raise ValueError("No file has been provided to parse.")
            else:
                if isinstance(file, PosixPath) and Path.exists(file):
                    file_ext = str(file.absolute()).rsplit(".", 1)[-1]
                elif isinstance(file, str) and os.path.exists(file):
                    file_ext = file.rsplit(".", 1)[-1]
        print(f" ##### File extension: {file_ext}")
        parser: Optional[Callable] = None
        # experiment_t_key: str = "/ENTRY[entry]/experiment_type"
        # experiment_t: str = eln_dict[experiment_t_key]
        try:
            experiment_dict: SPMParser.par_nav_t = self.__parser_navigation[file_ext]
        except KeyError as exc:
            raise KeyError(
                f"Add correct experiment type in ELN file "
                f" from {list(self.__parser_navigation.keys())}."
            ) from exc

        vendor_key: str = "/ENTRY[entry]/INSTRUMENT[instrument]/software/vendor"
        vendor_n: str = eln_dict.get(vendor_key, None)
        try:
            vendor_dict: SPMParser.par_nav_t = experiment_dict.get(vendor_n, {})  # type: ignore[assignment]
        except (KeyError, ValueError):
            pass

        software_v_key: str = (
            "/ENTRY[entry]/INSTRUMENT[instrument]/software/model/@version"
        )
        software_v: str = eln_dict.get(software_v_key, None)
        try:
            parser_cls: Callable = vendor_dict.get(software_v, None)  # type: ignore[assignment]
            if isinstance(parser_cls, Callable):
                parser = parser_cls()
        except (ValueError, KeyError):
            pass

        # collect all parsers
        if parser is None:
            flat_dict = {}
            phs.nested_path_to_slash_separated_path(experiment_dict, flat_dict)

            return flat_dict.values()

        # Return callable function
        return iter([parser])

    def get_raw_data_dict(
        self,
        file: Union[str, Path],
        eln_dict: Dict = None,
        file_ext: Optional[str] = None,
    ):
        """Get the raw data from the file."""
        parsers: Iterable[callable] = self.__get_appropriate_parser(
            file=file, eln_dict=eln_dict or {}, file_ext=file_ext
        )
        raw_data_dict: Optional[Dict[str, Any]] = None
        for parser in parsers:
            try:
                raw_data_dict = parser(file).parse()
            except Exception:
                pass
            if raw_data_dict is not None:
                return raw_data_dict

    def parse(self, file):
        return self.get_raw_data_dict(file)


def get_nanonis_sxm_parsed_data(file_path: str):
    """This function is intended to parse the Nanonis SXM file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the Nanonis SXM file.

    Returns
    -------
    Dict
        The parsed data from the Nanonis SXM file.
    """
    # from pynxtools_stm.parsers.nanonis_sxm import SXMGenericNanonis
    #
    # nanonis_sxm = SXMGenericNanonis(file_path)
    # return nanonis_sxm.get_parsed_data()
    return SPMParser().get_raw_data_dict(file_path)


def get_nanonis_dat_parsed_data(file_path: str):
    """This function is intended to parse the Nanonis DAT file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the Nanonis DAT file.

    Returns
    -------
    Dict
        The parsed data from the Nanonis DAT file.
    """
    # from pynxtools_stm.parsers.nanonis_dat import DATGenericNanonis
    #
    # nanonis_dat = DATGenericNanonis(file_path)
    # return nanonis_dat.get_parsed_data()
    raise NotImplementedError("This function is not implemented yet.")


def get_bruker_spm_parsed_data(file_path: str):
    """This function is intended to parse the Bruker SPM file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the Bruker SPM file.

    Returns
    -------
    Dict
        The parsed data from the Bruker SPM file.
    """
    # from pynxtools_stm.parsers.bruker_spm import BrukerSPM
    #
    # bruker_spm = BrukerSPM(file_path)
    # return bruker_spm.get_parsed_data()
    raise NotImplementedError("This function is not implemented yet.")


def get_spm_parsed_data(file_path: str):
    """This function is intended to parse the SPM file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the SPM file.

    Returns
    -------
    Dict
        The parsed data from the SPM file.
    """
    # from pynxtools_stm.parsers.spm import SPM
    #
    # spm = SPM(file_path)
    # return spm.get_parsed_data()
    raise NotImplementedError("This function is not implemented yet.")
