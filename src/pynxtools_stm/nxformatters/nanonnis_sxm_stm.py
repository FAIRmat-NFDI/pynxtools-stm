from pynxtools_stm.nxformatters.base_formatter import SPMformatter
from typing import Dict, Optional, Union
from pathlib import Path
import re
from pynxtools_stm.configs.nanonis_sxm_generic_stm import __config_stm_generic
import pynxtools_stm.nxformatters.helpers as fhs
from pynxtools.dataconverter.template import Template
from pynxtools_stm.nxformatters.helpers import (
    __get_data_unit_and_others,
    __scientific_num_pattern,
)


class NanonisSXMSTM(SPMformatter):
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
        self.config_dict: Dict = self.__get_conf_dict(config_file)

    def get_nxformatted_template(self):
        parent_path = "/ENTRY[entry]/experiment_instrument/scan_environment"
        scan_control_dict = self.config_dict["ENTRY[entry]"]["experiment_instrument"][
            "scan_environment"
        ]["SCAN_CONTROL[scan_control]"]
        self.construct_scan_control_grp(
            template=self.template,
            partial_conf_dict=scan_control_dict,
            parent_path=parent_path,
            data_dict=self.raw_data,
            group_name="scan_control",
        )

    def __get_conf_dict(self, config_file: str = None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            return __config_stm_generic

    def construct_scan_control_grp(
        self,
        template,
        partial_conf_dict,
        parent_path: str,
        data_dict,
        group_name="scan_control",
    ):
        # Rethink about the global variables
        global gbl_scan_points, gbl_scan_ranges
        axes = ["x", "y", "z"]

        # gbl_scan_ranges = None
        # gbl_scan_points = None
        def construct_scan_region_grp(
            template,
            partial_conf_dict,
            parent_path: str,
            data_dict,
            group_name="scan_region",
        ):
            scan_angle = "scan_offset_N[scan_offset_n]"

            scan_angles, unit, _ = __get_data_unit_and_others(
                data_dict=data_dict,
                partial_conf_dict=partial_conf_dict,
                concept_field=scan_angle,
            )
            scan_angles = re.findall(__scientific_num_pattern, scan_angles)
            for ind, ang in enumerate(scan_angles):
                template[f"{parent_path}/{group_name}/scan_offset_{axes[ind]}"] = ang
                template[
                    f"{parent_path}/{group_name}/scan_offset_{axes[ind]}/@units"
                ] = unit

            # scan range
            scan_range = "scan_range_N[scan_range_n]"
            scan_ranges, unit, _ = __get_data_unit_and_others(
                data_dict=data_dict,
                partial_conf_dict=partial_conf_dict,
                concept_field=scan_range,
            )
            global gbl_scan_ranges
            gbl_scan_ranges = re.findall(__scientific_num_pattern, scan_ranges)
            if gbl_scan_ranges:
                gbl_scan_ranges = [float(x) for x in gbl_scan_ranges]

            for ind, rng in enumerate(gbl_scan_ranges):
                template[f"{parent_path}/{group_name}/scan_range_{axes[ind]}"] = rng
                template[
                    f"{parent_path}/{group_name}/scan_range_{axes[ind]}/@units"
                ] = unit

        def construct_scan_pattern_grp(
            template,
            partial_conf_dict,
            parent_path: str,
            data_dict,
            group_name="scan_mesh",
        ):
            """To construct the scan pattern like scan_mesh, scan_spiral (group) etc."""

            # scan_point fields
            scan_point = "scan_points_N[scan_points_n]"

            scan_points, unit, _ = __get_data_unit_and_others(
                data_dict=data_dict,
                partial_conf_dict=partial_conf_dict,
                concept_field=scan_point,
            )
            # TODO remove the global variables
            global gbl_scan_points, gbl_scan_ranges
            gbl_scan_points = re.findall(__scientific_num_pattern, scan_points)
            if gbl_scan_points:
                gbl_scan_points = [float(x) for x in gbl_scan_points]
            for ind, point in enumerate(gbl_scan_points):
                template[f"{parent_path}/{group_name}/scan_points_{axes[ind]}"] = point
            # step_size
            if len(gbl_scan_points) == len(gbl_scan_ranges):
                for ind, (rng, pnt) in enumerate(zip(gbl_scan_ranges, gbl_scan_points)):
                    template[f"{parent_path}/{group_name}/step_size_{axes[ind]}"] = (
                        rng / pnt
                    )
                    template[
                        f"{parent_path}/{group_name}/step_size_{axes[ind]}/@units"
                    ] = unit

        # find independent_scan_axes
        # independent_axes = "/ENTRY[entry]/experiment_instrument/scan_environment/SCAN_CONTROL[scan_control]/independent_scan_axes"
        independent_axes = "independent_scan_axes"
        direction, _, _ = __get_data_unit_and_others(
            data_dict=data_dict,
            partial_conf_dict=partial_conf_dict,
            concept_field=independent_axes,
        )
        template[f"{parent_path}/{group_name}/independent_scan_axes"] = (
            self.__arange_axes(direction.strip())
        )
        scan_region_grp = "scan_region"
        scan_region_dict = partial_conf_dict.get(scan_region_grp, None)
        if scan_region_dict is not None:
            construct_scan_region_grp(
                template,
                partial_conf_dict=scan_region_dict,
                parent_path=f"{parent_path}/{group_name}",
                data_dict=data_dict,
                group_name=scan_region_grp,
            )
        scan_pattern_grp = "mesh_SCAN[mesh_scan]"
        scan_pattern_dict = partial_conf_dict.get(scan_pattern_grp, None)
        if scan_pattern_dict is not None:
            construct_scan_pattern_grp(
                template,
                partial_conf_dict=scan_pattern_dict,
                parent_path=f"{parent_path}/{group_name}",
                data_dict=data_dict,
                group_name=scan_pattern_grp,
            )

    # def __construct_nxlockin(self):
    #     pass

    # def __construct_nxdata(self):
    #     pass
