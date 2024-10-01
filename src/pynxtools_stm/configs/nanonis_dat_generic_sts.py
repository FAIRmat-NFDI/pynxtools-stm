#!/usr/bin/env python3
"""
A default configuration file for Nanonis STS data from dat file.
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

_nanonis_sts_dat_generic_5e = {
    "ENTRY[entry]": {
        "definition": {"@version": None},
        "experiment_instrument": {
            "LOCKIN[lockin]": {
                "modulation_frequency": None,
                "modulation_signal_type": None,
            },
            "bias_spectroscopy_environment": {
                "BIAS_SPECTROSCOPY[bias_spectroscopy]": None,
                "independent_controllers": None,
                "measurement_sensors": None,
            },
            "cryo_shield_temperature": {"temperature": {"@units": None}},
            "cryo_temperature": {"temperature": {"@units": None}},
            "current_sensor": {
                "AMPLIFIER[amplifier]": {"current_gain": None},
                "current": {"@units": None},
                "current_calibration": {
                    "caliberation_time": {"@units": None},
                    "coefficients": {"@units": None},
                },
                "current_offset": {"@units": None},
            },
            "piazo_sensor": {
                "PIEZO_CONFIG_SPM[piezo_config_spm]": {
                    "2nd_order_corr_N[2nd_order_corr_n]": {"@units": None},
                    "calibration_coeffecient_N[calibration_coeffecient_n]": {
                        "@units": None
                    },
                    "calibration_type": None,
                    "drift_N[drift_n]": None,
                    "drift_correction_status": None,
                    "hv_gain_N[hv_gain_n]": None,
                    "tilt_N[tilt_n]": {"@units": None},
                },
                "POSITIONER_SPM[positioner_spm]": {
                    "z_controller": {
                        "controller_name": None,
                        "controller_status": None,
                        "set_point": {"@units": None},
                        "switch_off_delay": {"@units": None},
                        "tip_lift": {"@units": None},
                        "z": None,
                    }
                },
                "x": {"@units": None},
                "y": {"@units": None},
                "z": {"@units": None},
            },
            "scan_environment": {
                "SCAN_CONTROL[scan_control]": {
                    "mesh_SCAN[mesh_scan]": {
                        "SCAN_DATA[scan_data]": None,
                        "backward_speed_N[backward_speed_n]": {"@units": None},
                        "forward_speed_N[forward_speed_n]": {"@units": None},
                        "scan_speed": {"@units": None},
                        "scan_time": {"@units": None},
                    },
                    "scan_region": {
                        "scan_angle_N[scan_angle_n]": {"@units": None},
                        "scan_offset": {"@units": None},
                        "scan_range": {"@units": None},
                    },
                    "scan_type": None,
                },
                "cryo_bottom_temp": {"@units": None},
                "cryo_shield_temp": {"@units": None},
                "cryo_shield_temperature": {
                    "calibration_time": None,
                    "value": {"@units": None},
                },
                "cryo_temperature": {
                    "calibration_time": None,
                    "value": {"@units": None},
                },
                "stm_head_temp": {"@units": None},
                "tip_temperature": {
                    "calibration_time": None,
                    "value": {"@units": None},
                },
            },
            "tip_temperature": {"temperature": {"@units": None}},
        },
        "reproducibility_indicators": {
            "bias_sweep": None,
            "current": None,
            "current_gain": None,
            "current_offset": None,
            "modulation_frequency": None,
            "modulation_signal_type": None,
        },
        "resolution_indicators": {
            "bias_sweep": None,
            "cryo_bottom_temp": None,
            "cryo_shield_temp": None,
            "modulation_frequency": None,
            "modulation_signal_type": None,
            "stm_head_temp": None,
        },
    }
}
