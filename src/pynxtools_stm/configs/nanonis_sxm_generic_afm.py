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
        "@defaut": {
            "raw_path": "@default:/entry/experiment_instrument/scan_environment/scan_control/mesh_scan/amplitude_backward/amplitude_backward",
        },
        "definition": {"@version": None},
        "collection_identifier": "",
        "end_time": "",
        "entry_identifier": "",
        "start_time": "",
        "scan_mode": "",
        "scan_type": "",
        "experiment_identifier": {"identifier": ""},
        "experiment_description": {"raw_path": "/COMMENT"},
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
                    },
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
                    "cantilever_amplitude_positioner": {
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
                            "raw_path": "/Oscillation Control/PLL-Setup Demod. Bandwidth Amp",
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
            "tip_temperature": None,
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
                    "2nd_order_corr_N[2nd_order_corr_n]": [
                        {
                            "X": {
                                "raw_path": "/Piezo Calibration/2nd order corr X",
                                "@units": "/Piezo Calibration/2nd order corr X/@unit",
                            }
                        },
                        {
                            "Y": {
                                "raw_path": "/Piezo Calibration/2nd order corr Y",
                                "@units": "/Piezo Calibration/2nd order corr Y/@unit",
                            }
                        },
                        {
                            "Z": {
                                "raw_path": "/Piezo Calibration/2nd order corr Z",
                                "@units": "/Piezo Calibration/2nd order corr Z/@unit",
                            }
                        },
                    ],
                    "calibration_name": {
                        "raw_path": "/Piezo Calibration/Active Calib."
                    },
                    "drift_N[drift_n]": [
                        {
                            "X": {
                                "raw_path": "/Piezo Calibration/Drift X",
                                "@units": "/Piezo Calibration/Drift X/@unit",
                            }
                        },
                        {
                            "Y": {
                                "raw_path": "/Piezo Calibration/Drift Y",
                                "@units": "/Piezo Calibration/Drift Y/@unit",
                            }
                        },
                        {
                            "Z": {
                                "raw_path": "/Piezo Calibration/Drift Z",
                                "@units": "/Piezo Calibration/Drift Z/@unit",
                            }
                        },
                    ],
                    "drift_correction_status": {
                        "raw_path": [
                            "/Piezo Configuration/Drift correction status",
                            "/Piezo Calibration/Drift correction status",
                        ]
                    },
                    "hv_gain_N[hv_gain_n]": [
                        {"X": {"raw_path": "/Piezo Calibration/HV Gain X"}},
                        {"Y": {"raw_path": "/Piezo Calibration/HV Gain Y"}},
                        {"Z": {"raw_path": "/Piezo Calibration/HV Gain Z"}},
                    ],
                    "tilt_N[tilt_n]": [
                        {
                            "X": {
                                "raw_path": "/Piezo Calibration/Tilt X",
                                "@units": "/Piezo Calibration/Tilt X/@unit",
                            }
                        },
                        {
                            "Y": {
                                "raw_path": "/Piezo Calibration/Tilt Y",
                                "@units": "/Piezo Calibration/Tilt X/@unit",
                            }
                        },
                    ],
                    "piezo_material": {
                        "curvature_radius_N": [
                            {
                                "x": {
                                    "raw_path": "/Piezo Calibration/Curvature radius X",
                                    "@units": "/Piezo Calibration/Curvature radius X/@unit",
                                }
                            },
                            {
                                "y": {
                                    "raw_path": "/Piezo Calibration/Curvature radius Y",
                                    "@units": "/Piezo Calibration/Curvature radius Y/@unit",
                                }
                            },
                        ]
                    },
                    "calibration": {
                        "calibration_type": {
                            "raw_path": "@default:active",
                        },
                        "calibration_coeffecient_N[calibration_coeffecient_n]": [
                            {
                                "X": {
                                    "raw_path": "/Piezo Calibration/Calib. X",
                                    "@units": "/Piezo Calibration/Calib. X/@unit",
                                }
                            },
                            {
                                "Y": {
                                    "raw_path": "/Piezo Calibration/Calib. Y",
                                    "@units": "/Piezo Calibration/Calib. Y/@unit",
                                }
                            },
                            {
                                "Z": {
                                    "raw_path": "/Piezo Calibration/Calib. Z",
                                    "@units": "/Piezo Calibration/Calib. Z/@unit",
                                },
                            },
                        ],
                    },
                },
                "POSITIONER_SPM[positioner_spm]": {
                    "z_controller": {
                        "K_i_value[k_i_value]": {"raw_path": "/Z-Controller/P gain"},
                        "K_p_value[k_p_value]": {"raw_path": "/Z-Controller/I gain"},
                        "setpoint": {
                            "raw_path": "/Z-Controller/Setpoint",
                            "@units": "/Z-Controller/Setpoint unit",
                        },
                        "switch_off_delay": "",
                        "K_t_const[k_t_const]": {
                            "raw_path": "/Z-Controller/Time const",
                            "@units": "/Z-Controller/Time const/@unit",
                        },
                        "tip_lift": {
                            "raw_path": "/Z-Controller/TipLift",
                            "@units": "/Z-Controller/TipLift/@unit",
                        },
                        "z": {
                            "raw_path": "/Z-Controller/Z",
                            "@units": "/Z-Controller/Z/@unit",
                        },
                    },
                    "z_offset": "",
                    "tip_position_z": "",
                    "controller_name": {"raw_path": "/Z-Controller/Controller name"},
                    "controller_status": {
                        "raw_path": "/Z-Controller/Controller status"
                    },
                    "switch_off_delay": {
                        "raw_path": "/Z-Controller/Switch off delay",
                        "@units": "/Z-Controller/Switch off delay/@unit",
                    },
                },
                "x": {"@units": None},
                "y": {"@units": None},
                "z": {"@units": None},
            },
            "scan_environment": {
                "cryo_bottom_temp": {"@units": None},
                "cryo_shield_temp": {"@units": None},
                "tip_temp": {"@units": None},
                "scan_name": {"raw_path": "/Scan/series name"},
                "SCAN_CONTROL[scan_control]": {
                    "scan_name": {"raw_path": "/Scan/series name"},
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
                        "SCAN_DATA[scan_data]": [
                            {
                                "data": {
                                    "name": "imput_4",
                                    "raw_path": "/Input_4/forward",
                                    "@units": "/DATA/INFO/Input_4/Unit",
                                },
                                "@title": "Input-4 Plot of AFM Experiment (Forward Direction)",
                                "grp_name": "input_4_forward",
                            },
                            {
                                "data": {
                                    "name": "imput_4",
                                    "raw_path": "/Input_4/backward",
                                    "@units": "/DATA/INFO/Input_4/Unit",
                                },
                                "@title": "Input-4 Plot of AFM Experiment (Backward Direction)",
                                "grp_name": "input_4_backward",
                            },
                            {
                                "data": {
                                    "name": "lix_1_omega",
                                    "raw_path": "/LIX_1_omega/foward",
                                    "@units": "/DATA/INFO/LIX_1_omega/Unit",
                                },
                                "@title": "Lockin X-1 Plot of AFM Experiment (Forward Direction)",
                                "grp_name": "lix_1_omega_forward",
                            },
                            {
                                "data": {
                                    "name": "lix_1_omega",
                                    "raw_path": "/LIX_1_omega/backward",
                                    "@units": "/DATA/INFO/LIX_1_omega/Unit",
                                },
                                "@title": "Lockin X-1 Plot of AFM Experiment (Backward Direction)",
                                "grp_name": "lix_1_omega_backward",
                            },
                            {
                                "data": {
                                    "name": "liy_1_omega",
                                    "raw_path": "/LIY_1_omega/foward",
                                    "@units": "/DATA/INFO/LIY_1_omega/Unit",
                                },
                                "@title": "Lockin Y-1 Plot of AFM Experiment (Forward Direction)",
                                "grp_name": "liy_1_omega_forward",
                            },
                            {
                                "data": {
                                    "name": "liy_1_omega",
                                    "raw_path": "/LIY_1_omega/backward",
                                    "@units": "/DATA/INFO/LIY_1_omega/Unit",
                                },
                                "@title": "Lockin Y-1 Plot of AFM Experiment (Backward Direction)",
                                "grp_name": "lixy_1_omega_backward",
                            },
                            {
                                "data": {
                                    "name": "frequency_shift",
                                    "raw_path": "/Frequency_Shift/forward",
                                    "@units": "/DATA/INFO/Frequency_Shift/Unit",
                                },
                                "@title": "Frequency Shift Plot of AFM Experiment (Forward Direction)",
                                "grp_name": "frequency_shift_forward",
                            },
                            {
                                "data": {
                                    "name": "frequency_shift",
                                    "raw_path": "/Frequency_Shift/backward",
                                    "@units": "/DATA/INFO/Frequency_Shift/Unit",
                                },
                                "@title": "Frequency Shift Plot of AFM Experiment (Backward Direction)",
                                "grp_name": "frequency_shift_backward",
                            },
                        ],
                    },
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
            },
            "real_time_controller": {
                "rcs_frequency": {
                    "raw_path": "/NanonisMain/RT Frequency",
                    "@units": "/NanonisMain/RT Frequency/@unit",
                },
                "rcs_model": {
                    "raw_path": "/NanonisMain/RT Release",
                },
                "acquisition_time": {
                    "raw_path": "/NanonisMain/Acquisition Period",
                    "@units": "/NanonisMain/Acquisition Period/@unit",
                },
                "animation_time": {
                    "raw_path": "/NanonisMain/Animations Period",
                    "@units": "/NanonisMain/Animations Period/@unit",
                },
                "measurement_time": {
                    "raw_path": "/NanonisMain/Measurements Period",
                    "@units": "/NanonisMain/Measurements Period/@unit",
                },
                "indicators_period": {
                    "raw_path": "/NanonisMain/Indicators Period",
                    "@units": "/NanonisMain/Indicators Period/@unit",
                },
            },
            "sample_bias_votage": {
                "bias_voltage": {
                    "raw_path": "/Bias/Bias",
                    "@units": "/Bias/Bias/@unit",
                },
                "bias_offset": {
                    "raw_path": "/Bias/Offset",
                    "@units": "/Bias/Offset/@unit",
                },
                "bias_calibration": {
                    "coefficients": {
                        "raw_path": "/Bias/Calibration",
                        "@units": "/Bias/Calibration/@unit",
                    },
                    "calibration_time": "",
                },
            },
        },
        "DATA[data]": [
            {
                "data": {
                    "name": "z",
                    "raw_path": "/Z/forward",
                    "@units": "/DATA/INFO/Z/Unit",
                },
                # "0": {
                #     "name": "Bias Voltage",
                #     "raw_path": [
                #         "/Excitation/forward",
                #         "/dat_mat_components/Bias/value",
                #     ],
                #     "@units": [
                #         "/dat_mat_components/Bias calc/unit",
                #         "/dat_mat_components/Bias/unit",
                #     ],
                #     # "@long_name": "Bias Voltage",
                # },
                "@title": "Height Plot of AFM Experiment (Foward Direction)",
                "grp_name": "z_forward",
            },
            {
                "data": {
                    "name": "z",
                    "raw_path": "/Z/backward",
                    "@units": "/DATA/INFO/Z/Unit",
                },
                "@title": "Height Plot of AFM Experiment (Backward Direction)",
                "grp_name": "z_backward",
            },
            {
                "data": {
                    "name": "excitation",
                    "raw_path": "/Excitation/forward",
                    "@units": "/DATA/INFO/Excitation/Unit",
                },
                "@title": "Excitation Plot of AFM Experiment (Forward Direction)",
                "grp_name": "excitation_forward",
            },
            {
                "data": {
                    "name": "excitation",
                    "raw_path": "/Excitation/backward",
                    "@units": "/DATA/INFO/Excitation/Unit",
                },
                "@title": "Excitation Plot of AFM Experiment (Backward Direction)",
                "grp_name": "excitation _backward",
            },
            {
                "data": {
                    "name": "phase",
                    "raw_path": "/Phase/Foward",
                    "@units": "/DATA/INFO/Phase/Unit",
                },
                "@title": "Phase Plot of AFM Experiment (Forward Direction)",
                "grp_name": "phase_forward",
            },
            {
                "data": {
                    "name": "phase",
                    "raw_path": "/Phase/Backward",
                    "@units": "/DATA/INFO/Phase/Unit",
                },
                "@title": "Phase Plot of AFM Experiment (Backward Direction)",
                "grp_name": "phase_backward",
            },
            {
                "data": {
                    "name": "current",
                    "raw_path": "/Current/forward",
                    "@units": "/DATA/INFO/Current/Unit",
                },
                "@title": "Current Plot of AFM Experiment (Forward Direction)",
                "grp_name": "current_forward",
            },
            {
                "data": {
                    "name": "current",
                    "raw_path": "/Current/backward",
                    "@units": "/DATA/INFO/Current/Unit",
                },
                "@title": "Current Plot of AFM Experiment (Backward Direction)",
                "grp_name": "current_backward",
            },
        ],
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
    }
}
