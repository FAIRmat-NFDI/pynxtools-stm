from pynxtools_stm.nxformatters.base_formatter import SPMformatter
from typing import Dict, Optional, Union
from pathlib import Path
import itertools
from dataclasses import dataclass
import re
from pynxtools_stm.configs.nanonis_sxm_generic_stm import _config_stm_generic
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


# TODO: add test to check if user example config file is the same as given default
# config file with this package.
@dataclass
class NXScanControl:
    x_points = None
    y_points = None
    x_start = None
    y_start = None
    x_end = None
    y_end = None


class NanonisSXMSTM(SPMformatter):
    _grp_to_func = {"SCAN_CONTROL[scan_control]": "_construct_nxscan_controllers"}
    _axes = ["x", "y", "z"]

    def __init__(
        self,
        # TODO: fix the type of template
        template: Template,
        raw_file: Union[str, Path],
        eln_dict: Dict,
        config_file: str = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        super().__init__(template, raw_file, eln_dict, config_file, entry)
        self.config_dict: Dict = self._get_conf_dict(config_file)

    def get_nxformatted_template(self):
        # parent_path = "/ENTRY[entry]/experiment_instrument/scan_environment"
        # scan_control_dict = self.config_dict["ENTRY[entry]"]["experiment_instrument"][
        #     "scan_environment"
        # ]["SCAN_CONTROL[scan_control]"]
        # self._construct_nxscan_controlers(
        #     template=self.template,
        #     partial_conf_dict=scan_control_dict,
        #     parent_path=parent_path,
        #     group_name="scan_control",
        # )
        self.work_though_config_nested_dict(self.config_dict, "")

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

    def _get_conf_dict(self, config_file: str = None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            return _config_stm_generic

    def construct_scan_pattern_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_mesh",
    ):
        """To construct the scan pattern like scan_mesh, scan_spiral (group) etc."""

        # scan_point fields
        scan_point = "scan_points_N[scan_points_n]"

        scan_points, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,  # dict that contains concept field
            concept_field=scan_point,
        )
        # TODO remove the global variables
        global gbl_scan_points, gbl_scan_ranges
        gbl_scan_points = re.findall(_scientific_num_pattern, scan_points)
        if gbl_scan_points:
            gbl_scan_points = [float(x) for x in gbl_scan_points]
        for ind, point in enumerate(gbl_scan_points):
            self.template[
                f"{parent_path}/{group_name}/scan_points_N[scan_points_{self._axes[ind]}"
            ] = point
            if self._axes[ind] == "x":
                NXScanControl.x_points = point
            elif self._axes[ind] == "y":
                NXScanControl.y_points = point
        # step_size
        if len(gbl_scan_points) == len(gbl_scan_ranges):
            for ind, (rng, pnt) in enumerate(zip(gbl_scan_ranges, gbl_scan_points)):
                self.template[
                    f"{parent_path}/{group_name}/step_size_N[step_size_{self._axes[ind]}]"
                ] = rng / pnt
                self.template[
                    f"{parent_path}/{group_name}/step_size_N[step_size_{self._axes[ind]}]/@units"
                ] = unit

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
        scan_angle = "scan_offset_N[scan_offset_n]"

        scan_angles, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_angle,
        )
        scan_angles = to_intended_t(re.findall(_scientific_num_pattern, scan_angles))
        for ind, offset in enumerate(scan_angles):
            self.template[
                f"{parent_path}/{group_name}/scan_offset_N[scan_offset_{self._axes[ind]}]"
            ] = offset
            if self._axes[ind] == "x":
                NXScanControl.x_start = offset
            elif self._axes[ind] == "y":
                NXScanControl.y_start = offset
            self.template[
                f"{parent_path}/{group_name}/scan_offset__N[scan_offset_{self._axes[ind]}]/@units"
            ] = unit

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
            self.template[
                f"{parent_path}/{group_name}/scan_range_N[scan_range_{self._axes[ind]}]"
            ] = rng

            if self._axes[ind] == "x" and NXScanControl.x_start is not None:
                NXScanControl.x_end = rng + NXScanControl.x_start
            elif self._axes[ind] == "y" and NXScanControl.y_start is not None:
                NXScanControl.y_end = rng + NXScanControl.y_start

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
        self.template[f"{parent_path}/{group_name}/{field_nm}"] = f_data
        self.template[f"{parent_path}/{group_name}/{field_nm}/@units"] = plot_data_info[
            "units"
        ]
        calibration = to_intended_t(plot_data_info.get("calibration", None))
        self.template[f"{parent_path}/{group_name}/{field_nm}/@calibration"] = (
            calibration
        )
        offset = to_intended_t(plot_data_info.get("offset", None))
        self.template[f"{parent_path}/{group_name}/{field_nm}/@calibration"] = offset
        # x and y axis
        self.template[f"{parent_path}/{group_name}/x"] = plot_data_info["x_axis"]
        x_unit = plot_data_info["x_units"]
        self.template[f"{parent_path}/{group_name}/x/@units"] = x_unit
        self.template[f"{parent_path}/{group_name}/x/@long_name"] = f"X ({x_unit})"
        self.template[f"{parent_path}/{group_name}/y"] = plot_data_info["y_axis"]
        y_unit = plot_data_info["y_units"]
        self.template[f"{parent_path}/{group_name}/y/@units"] = y_unit
        self.template[f"{parent_path}/{group_name}/y/@long_name"] = f"Y ({y_unit})"

        # TODO: Check why NXdata plot does not work
        # # Create links for NXdata in entry level
        # entry = parent_path.split("/")[1]
        # print("##### NXdata]", f"/{entry}/DATA[{field_nm}]")
        # self.template[f"/{entry}/{field_nm}"] = {
        #     "link": get_link_compatible_key(f"{parent_path}/{group_name}")
        # }

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

        print(" #### : ", data_headers)

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
                                    NXScanControl.x_start,
                                    NXScanControl.x_end,
                                    int(NXScanControl.x_points),
                                ),
                                "x_units": row[2],
                                "y_axis": np.linspace(
                                    NXScanControl.y_start,
                                    NXScanControl.y_end,
                                    int(NXScanControl.y_points),
                                ),
                                "y_units": row[2],
                            },
                            {
                                "data_path": data_key_b,
                                "units": row[2],
                                "calibration": row[4],
                                "offset": row[5],
                                "x_axis": np.linspace(
                                    NXScanControl.x_start,
                                    NXScanControl.x_end,
                                    int(NXScanControl.x_points),
                                ),
                                "x_units": row[2],
                                "y_axis": np.linspace(
                                    NXScanControl.y_start,
                                    NXScanControl.y_end,
                                    int(NXScanControl.y_points),
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
                                NXScanControl.x_start,
                                NXScanControl.x_end,
                                int(NXScanControl.x_points),
                            ),
                            "x_units": row[2],
                            "y_axis": np.linspace(
                                NXScanControl.y_start,
                                NXScanControl.y_end,
                                int(NXScanControl.y_points),
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
        # Rethink about the global variables
        global gbl_scan_points, gbl_scan_ranges

        # gbl_scan_ranges = None
        # gbl_scan_points = None

        # find independent_scan_axes
        # independent_axes = "/ENTRY[entry]/experiment_instrument/scan_environment/SCAN_CONTROL[scan_control]/independent_scan_axes"
        independent_axes = "independent_scan_axes"
        direction, _, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=independent_axes,
        )
        self.template[f"{parent_path}/{group_name}/independent_scan_axes"] = (
            self._arange_axes(direction.strip())
        )
        scan_region_grp = "scan_region"
        scan_region_dict = partial_conf_dict.get(scan_region_grp, None)
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

    # def __construct_nxlockin(self):
    #     pass

    # def __construct_nxdata(self):
    #     pass
