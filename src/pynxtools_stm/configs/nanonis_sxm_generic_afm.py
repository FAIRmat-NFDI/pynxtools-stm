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
                    "frequency_bandwidth": {
                        "raw_path": "/Oscillation Control/Range",
                        "@units": "/Oscillation Control/Range/@unit",
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
                    "oscillator_excitation": {
                        "raw_path": "//Oscillation Control/Excitation",
                        "@units": "/Oscillation Control/Excitation/@unit",
                    },
                    "phase_lock_loop": {
                        "sensitivity_factor": {
                            "raw_path": "/Oscillation Control/PLL-Setup Q-Factor",
                            "@units": "/Oscillation Control/Sensitivity/@unit",
                        },
                        "frequency_demodulation_bandwidth": "",
                        "amplitude_demodulation_bandwidth": {
                            "raw_data": "/Oscillation Control/PLL-Setup Demod. Bandwidth Amp",
                            "@units": "/Oscillation Control/PLL-Setup Demod. Bandwidth Amp/@unit",
                        },
                        "phase_demodulation_bandwidth": {
                            "raw_path": "/Oscillation Control/PLL-Setup Demod. Bandwidth Pha",
                            "@units": "/Oscillation Control/PLL-Setup Demod. Bandwidth Pha/@unit",
                        },
                        "demodulated_signal": "",
                        "amplitude_excitation": {
                            "raw_path": "/Oscillation Control/PLL-Setup amplitude/excitation",
                            "@units": "/Oscillation Control/PLL-Setup amplitude/excitation/@unit",
                        },
                    },
                    "frequency_shift": {
                        "raw_path": "/Oscillation Control/FrequencyShift",
                        "@units": "/Oscillation Control/FrequencyShift/@unit",
                    },
                    "frequency_cutoff": {
                        "raw_path": "/Oscillation Control/Cut off frq",
                        "@units": "/Oscillation Control/Cut off frq/@unit",
                    },
                    "target_amplitude": "",
                    "active_frequency": "",
                },
            },
            "LOCKIN[lockin]": {
                "reference_frequency": {
                    "raw_path": "/Lock-in/Frequency",
                    "@units": "@default:Hz",
                },
                "modulation_signal_type": {
                    "raw_path": "/Lock-in/Modulated signal",
                    "@units": "/Lock-in/Modulated signal/@unit",
                },
                "demodulated_signal": {
                    "raw_path": "/Lock-in/Demodulated signal",
                    "@units": "/Lock-in/Demodulated signal/@unit",
                },
                "modulation_status": {"raw_path": "/Lock-in/Lock-in status"},
                "demodulated_frequency": "",
                "demodulated_amplitude": "",
                "demodulator_channels": "",
                "recorded_channels": "",
                "ref_phase_N[ref_phase_n]": {
                    "raw_path": "/Lock-in/Reference phase",
                    "@units": "/Lock-in/Reference phase/@unit",
                },
                "harmonic_order_N[harmonic_order_n]": {"raw_path": "/Lock-in/Harmonic"},
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
                "scan_name": {"raw_path": "/Scan/series name"},
                "SCAN_CONTROL[scan_control]": {
                    "scan_name": {  # TODO check it is in appdef
                        "raw_path": "/Scan/series name"
                    },
                    # TODO: include the functino from
                    # nanosnis stm_template.py, This part is
                    # copied from stm.
                    "mesh_SCAN[mesh_scan]": {
                        "backward_speed_N[backward_speed_n]": {
                            "#note": "Derived in construct_scan_pattern_grp",
                            "raw_path": "/Scan/speed backw.",
                            "@units": "/Scan/speed backw./@unit",
                        },
                        "forward_speed_N[forward_speed_n]": {
                            "#note": "Derived in construct_scan_pattern_grp",
                            "raw_path": "/Scan/speed forw.",
                            "@units": "/Scan/speed forw./@unit",
                        },
                        "scan_speed_N[scan_speed_n]": "",
                        "channel_NAME_N[scan_name_n]": "",
                        "scan_points_N[scan_points_n]": {
                            "#note": "Derived in construct_scan_pattern_grp",
                            "raw_path": "/SCAN/PIXELS",
                            "@units": "",
                        },
                        "stepping_N[stepping_n]": {
                            "raw_path": "@default:1",
                            "@units": "",
                        },
                        "step_size_N[step_size_n]": {"raw_path": "", "@units": ""},
                        "scan_time": "",
                        "SCAN_DATA[scan_data]": {
                            "raw_path": "/DATA/INFO",
                            "@units": "",
                        },
                    },
                    # TODO: include the functino from
                    # nanosnis stm_template.py, This part is
                    # copied from stm.
                    "scan_region": {
                        "scan_angle_N[scan_angle_n]": {
                            "raw_path": "/SCAN/ANGLE",
                            "@units": "@default:deg",
                        },
                        "scan_offset_N[scan_offset_n]": {
                            "#note": "Derived in function 'construct_scan_region_grp'.",
                            "raw_path": "/SCAN/OFFSET",
                            "@units": "/Z-Controller/Z/@unit",
                        },
                        "scan_range_N[scan_range_n]": {
                            "#note": "Derived in function 'construct_scan_region_grp'.",
                            "raw_path": "/SCAN/RANGE",
                            "@units": "/Z-Controller/Z/@unit",
                        },
                    },
                    "independent_scan_axes": {"raw_path": "/SCAN/DIR", "@units": ""},
                    "scan_resolution_N": "",
                    "accuracy_N": "",
                    "scan_type": {"raw_path": "@default:mesh", "@units": ""},
                    "scan_control_type": {
                        "raw_path": "@default:continuous",
                        "@units": "",
                    },
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
            "reference_frequency": None,
            "modulation_signal_type": None,
        },
        "resolution_indicators": {
            "bias_sweep": None,
            "cryo_bottom_temp": None,
            "cryo_shield_temp": None,
            "reference_frequency": None,
            "modulation_signal_type": None,
            "stm_head_temp": None,
        },
        "scan_mode": None,
    }
}
