#!/usr/bin/env python3
"""
A default configuration file for Nanonis STM data from SXM file.
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

_nanonis_afm_sxm_generic_5e = {
    "ENTRY[entry]": {
        "definition": {"@version": None},
        "experiment_instrument": {
            "CANTILEVER_SPM[cantilever_spm]": {
                "cantilever_oscillator": {
                    "reference_amplitude": {
                        "raw_path": "/Oscillation Control/Amplitude Setpoint",
                        "@units": "/Oscillation Control/Amplitude Setpoint/@unit",
                    },
                    "reference_frequency": {
                        "raw_path": "/Oscillation Control/Center Frequency",
                        "@units": "/Oscillation Control/Center Frequency/@unit",
                    },
                    "reference_phase": {
                        "raw_path": "/Oscillation Control/Reference Phase",
                        "@units": "/Oscillation Control/Reference Phase/@unit",
                    },  # TODO: Add it in NXcantilever_spm
                    "frequency_harmonic": {"raw_path": "/Oscillation Control/Harmonic"},
                    "cantilever_phase_positioner": {
                        "actuator": {
                            "feedback": {
                                "K_p_value[k_p_value]": {
                                    "raw_path": "/Oscillation Control/Phase P gain",
                                    "@units": "/Oscillation Control/Phase P gain/@unit",
                                },
                                "K_i_value[k_i_value]": {
                                    "raw_path": "/Oscillation Control/Phase I gain",
                                    "@units": "/Oscillation Control/Phase I gain/@unit",
                                },
                                "K_d_value[k_d_value]": "",
                                "K_t_const[k_t_const]": "",
                            },
                        },
                    },
                    "cantilever_frequency_positioner": {
                        "actuator": {
                            "feedback": {
                                "K_p_value[k_p_value]": "",
                                "K_i_value[k_i_value]": "",
                                "K_d_value[k_d_value]": "",
                                "K_t_const[k_t_const]": "",
                            },
                        },
                    },
                    "cantilever_amplitude_positioner": {  # TODO: Add it in NXcantilever_spm
                        "actuator": {
                            "feedback": {
                                "K_p_value[k_p_value]": {
                                    "raw_path": "/Oscillation Control/Amplitude P gain",
                                    "@units": "/Oscillation Control/Amplitude P gain/@unit",
                                },
                                "K_i_value[k_i_value]": {
                                    "raw_path": "/Oscillation Control/Amplitude I gain",
                                    "@units": "/Oscillation Control/Amplitude I gain/@unit",
                                },
                                "K_d_value[k_d_value]": "",
                                "K_t_const[k_t_const]": "",
                            },
                        },
                    },
                    "phase_lock_loop": "",  # TODO: fix type in NXcantilever
                    "frequency_shift": {
                        "raw_path": "/Oscillation Control/FrequencyShift",
                        "@units": "/Oscillation Control/FrequencyShift/@unit",
                    },
                    "frequency_cutoff": {
                        "raw_path": "/Oscillation Control/Cut off frq",
                        "@units": "/Oscillation Control/Cut off frq/@unit",
                    },
                    "frequency_bandwidth": {
                        "raw_path": "/Oscillation Control/Range",
                        "@units": "/Oscillation Control/Range/@unit",
                    },
                    "target_amplitude": "",
                    "active_frequency": "",
                },
            },
            "LOCKIN[lockin]": {
                "modulation_frequency": None,
                "modulation_signal_type": None,
            },
            "bias_spectroscopy_environment": {
                "BIAS_SPECTROSCOPY[bias_spectroscopy]": {
                    "bias_sweep": {
                        "linear_sweep": {
                            "reset_bias": None,
                            "scan_points_bias": None,
                            "step_size_bias": {"@units": None},
                        },
                        "scan_region": {
                            "scan_end_bias": {"@units": None},
                            "scan_offset_bias": {"@units": None},
                            "scan_range_bias": {"@units": None},
                            "scan_start_bias": {"@units": None},
                        },
                        "settling_time": {"@units": None},
                    }
                },
                "independent_controllers": None,
                "measurement_sensors": None,
            },
            "cryo_shield_temperature": None,
            "cryo_temperature": None,
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
                "tip_temp": {"@units": None},
                "tip_temperature": {
                    "calibration_time": None,
                    "value": {"@units": None},
                },
            },
            "tip_temperature": None,
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
        "scan_mode": None,
    }
}
