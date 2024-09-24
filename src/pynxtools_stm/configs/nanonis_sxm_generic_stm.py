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

# TODO: careate config file and include test with config file and wihout config file
_config_stm_generic = {
    "ENTRY[entry]": {
        "experiment_instrument": {
            "tip_temperature": "",
            "cryo_temperature": "",
            "cryo_shield_temperature": "",
            "scan_environment": {
                "stm_head_temp": "/Temperature 1/Temperature 1",
                "cryo_bottom_temp": "",
                "cryo_shield_temp": "",
                "SCAN_CONTROL[scan_control]": {
                    "mesh_SCAN[mesh_scan]": {
                        "backward_speed_N[backward_speed_n]": "",
                        "forward_speed_N[forward_speed_n]": "",
                        "scan_speed_N[scan_speed_n]": "",
                        "channel_NAME_N[scan_name_n]": "",
                        "scan_points_N[scan_points_n]": {"raw_path": "/SCAN/PIXELS"},
                        "stepping_N[stepping_n]": {"raw_path": "@default:1"},
                        "step_size_N[step_size_n]": {"raw_path": "", "@units": ""},
                        "scan_time": "",
                        "SCAN_DATA[scan_data]": {"raw_path": "/DATA/INFO"},
                    },
                    "scan_region": {
                        "scan_angle_N[scan_angle_n]": {
                            "raw_path": "/SCAN/ANGLE",
                            "@units": "@default:deg",
                        },
                        "scan_offset_N[scan_offset_n]": {
                            "raw_path": "/SCAN/OFFSET",
                            "@units": "",
                        },
                        "scan_range_N[scan_range_n]": {
                            "raw_path": "/SCAN/RANGE",
                            "@units": "",
                        },
                    },
                    "scan_time_start": "",
                    "scan_time_end": "",
                    "independent_scan_axes": {"raw_path": "/SCAN/DIR"},
                    "scan_resolution_N": "",
                    "accuracy_N": "",
                    "scan_type": {"raw_path": "@default:mesh"},
                    "scan_control_type": {"raw_path": "@default:continuous"},
                },
                "SENSOR[sensor]": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
                "independent_controllers": "",
                "measurement_sensors": "",
                "cryo_shield_temperature": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
                "cryo_temperature": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
                "tip_temperature": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
            },
            "LOCKIN[lockin]": {
                "modulation_frequency": "",
                "modulation_signal_type": "",
            },
            "bias_spectroscopy_environment": {
                "SENSOR[sensor]": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
                "independent_controllers": "",
                "measurement_sensors": "",
            },
            "current_sensor": {
                "AMPLIFIER[amplifier]": {"current_gain": ""},
                "current": "",
                "current_calibration": {"caliberation_time": "", "coefficients": ""},
                "current_offset": "",
            },
            "piazo_sensor": {
                "PIEZO_CONFIG_SPM[piezo_config_spm]": {
                    "2nd_order_corr_N[2nd_order_corr_n]": "",
                    "calibration_coeffecient_N[calibration_coeffecient_n]": "",
                    "calibration_type": "",
                    "drift_N[drift_n]": "",
                    "drift_correction_status": "",
                    "hv_gain_N[hv_gain_n]": "",
                    "tilt_N[tilt_n]": "",
                },
                "POSITIONER_SPM[positioner_spm]": {
                    "z_controller": {
                        "controller_name": "",
                        "controller_status": "",
                        "i_gain": "",
                        "p_gain": "",
                        "set_point": "",
                        "switch_off_delay": "",
                        "time_const": "",
                        "tip_lift": "",
                        "z": "",
                    }
                },
                "x": "",
                "y": "",
                "z": "",
            },
        },
        "PROCESS[process]": {"program": ""},
        "SAMPLE[sample]": {"name": ""},
        "USER[user]": {
            "address": "",
            "affiliation": "",
            "email": "",
            "name": "",
            "orcid": "",
            "telephone_number": "",
        },
        "collection_identifier": "",
        "definition": "",
        "end_time": "",
        "entry_identifier": "",
        "experiment_description": "",
        "experiment_identifier": "",
        "experiment_insturment": {
            "scan_environment": {
                "SENSOR[sensor]": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
                "current_sensor": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
                "independent_controllers": "",
                "measurement_sensors": "",
                "piazo_sensor": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
                "volatage_sensor": {
                    "calibration_time": "",
                    "run_control": "",
                    "value": "",
                    "value_timestamp": "",
                },
            },
            "TEMPERATURE[temperature]": {
                "CHANNEL_temp[channel_temp]": "",
                "temperature": "",
                "temperature_calibration": {
                    "caliberation_time": "",
                    "coefficients": "",
                },
            },
            "hardware": {"model": "", "vendor": ""},
            "sample_bias_votage": {
                "bias_calibration": {"caliberation_time": "", "coefficients": ""},
                "bias_offset": "",
                "bias_voltage": "",
            },
            "software": {"model": "", "vendor": ""},
        },
        "reproducibility_indicators": {
            "current": "",
            "current_gain": "",
            "current_offset": "",
            "modulation_frequency": "",
            "modulation_signal_type": "",
        },
        "resolution_indicators": {
            "modulation_frequency": "",
            "modulation_signal_type": "",
        },
        "scan_mode": "",
        "start_time": "",
    }
}
