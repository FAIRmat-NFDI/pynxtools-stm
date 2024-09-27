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
# TODO: Try to include functionality to collect NXdata description from config file
# for example:
# "/ENTRY[entry]/DATA[data]": {"0": ["/Z/forward",
#    "/Z/backward"],
#  "1": ["/Bias/forward",
#    "/Bias/backward"],
#  "2": ["/Current/forward",
#    "/Current/backward"],
#  "3": ["/LI_Demod_2_X/forward",
#    "/LI_Demod_2_X/backward"],
#  "4": ["/LI_Demod_2_Y/forward",
#    "/LI_Demod_2_Y/backward"],
#  "5": ["/LI_Demod_1_X/forward",
#    "/LI_Demod_1_X/backward"],
#  "6": ["/LI_Demod_1_Y/forward",
#    "/LI_Demod_1_Y/backward"]},
_config_stm_generic = {
    "ENTRY[entry]": {
        # '@defaut': 'name of one of the plots,  TODO
        "INSTRUMENT[instrument]": {
            "tip_temperature": "",
            "cryo_temperature": "",
            "cryo_shield_temperature": "",
            "scan_environment": {
                "stm_head_temp": {
                    "raw_path": "/Temperature 1/Temperature 1",
                    "@units": "@default:K",
                },
                "cryo_bottom_temp": "",
                "cryo_shield_temp": "",
                "SCAN_CONTROL[scan_control]": {
                    "mesh_SCAN[mesh_scan]": {
                        "backward_speed_N[backward_speed_n]": "",
                        "forward_speed_N[forward_speed_n]": "",
                        "scan_speed_N[scan_speed_n]": "",
                        "channel_NAME_N[scan_name_n]": "",
                        "scan_points_N[scan_points_n]": {
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
                    "independent_scan_axes": {"raw_path": "/SCAN/DIR", "@units": ""},
                    "scan_resolution_N": "",
                    "accuracy_N": "",
                    "scan_type": {"raw_path": "@default:mesh", "@units": ""},
                    "scan_control_type": {
                        "raw_path": "@default:continuous",
                        "@units": "",
                    },
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
                "modulation_frequency": {
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
                "low_pass_N": [
                    {
                        "d1": {
                            "raw_path": "/Lock-in/LP Filter Cutoff D1",
                            "@units": "/Lock-in/LP Filter Cutoff D1/@unit",
                        }
                    },
                    {
                        "d2": {
                            "raw_path": "/Lock-in/LP Filter Cutoff D2",
                            "@units": "/Lock-in/LP Filter Cutoff D2/@unit",
                        }
                    },
                ],
                "lp_filter_order_N": [
                    {
                        "d1": {"raw_path": "/Lock-in/LP Filter Order D1"},
                        "d2": {"raw_path": "/Lock-in/LP Filter Order D2"},
                    }
                ],
                "hi_pass_N": [
                    {
                        "d1": {
                            "raw_path": "/Lock-in/HP Filter Cutoff D1",
                            "@units": "/Lock-in/HP Filter Cutoff D1/@unit",
                        }
                    },
                    {
                        "d2": {
                            "raw_path": "/Lock-in/HP Filter Cutoff D2",
                            "@units": "/Lock-in/HP Filter Cutoff D2/@unit",
                        }
                    },
                ],
                "hp_filter_order_N": [
                    {"d1": {"raw_path": "/Lock-in/HP Filter Order D1"}},
                    {"d2": {"raw_path": "/Lock-in/HP Filter Order D2"}},
                ],
                "ref_phase_N[ref_phase_n]": [
                    {
                        "d1": {
                            "raw_path": "/Lock-in/Reference phase D1",
                            "@units": "/Lock-in/Reference phase D1/@unit",
                        }
                    },
                    {
                        "d2": {
                            "raw_path": "/Lock-in/Reference phase D2",
                            "@units": "/Lock-in/Reference phase D1/@unit",
                        }
                    },
                ],
                "harmonic_order_N[harmonic_order_n]": [
                    {"d1": {"raw_path": "/Lock-in/Harmonic D1"}},
                    {"d2": {"raw_path": "/Lock-in/Harmonic D2"}},
                ],
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
                    "2nd_order_corr_N[2nd_order_corr_n]": [
                        {
                            "X": {
                                "raw_path": "/Piezo Configuration/2nd order corr X",
                                "@units": "/Piezo Configuration/2nd order corr X/@unit",
                            }
                        },
                        {
                            "Y": {
                                "raw_path": "/Piezo Configuration/2nd order corr Y",
                                "@units": "/Piezo Configuration/2nd order corr Y/@unit",
                            }
                        },
                        {
                            "Z": {
                                "raw_path": "/Piezo Configuration/2nd order corr Z",
                                "@units": "/Piezo Configuration/2nd order corr Z/@unit",
                            }
                        },
                    ],
                    "calibration_coeffecient_N[calibration_coeffecient_n]": [
                        {
                            "X": {
                                "raw_path": "/Piezo Configuration/Calib. X",
                                "@units": "/Piezo Configuration/Calib. X/@unit",
                            }
                        },
                        {
                            "Y": {
                                "raw_path": "/Piezo Configuration/Calib. Y",
                                "@units": "/Piezo Configuration/Calib. Y/@unit",
                            }
                        },
                        {
                            "Z": {
                                "raw_path": "/Piezo Configuration/Calib. Z",
                                "@units": "/Piezo Configuration/Calib. Z/@unit",
                            },
                        },
                    ],
                    "calibration_type": {
                        "raw_path": "/Piezo Configuration/Active Calib.",
                    },  # TODO handle it in different function
                    "calibration_name": {
                        "raw_path": "/Piezo Configuration/Active Calib."
                    },
                    "drift_N[drift_n]": [
                        {
                            "X": {
                                "raw_path": "/Piezo Configuration/Drift X",
                                "@units": "/Piezo Configuration/Drift X/@unit",
                            }
                        },
                        {
                            "Y": {
                                "raw_path": "/Piezo Configuration/Drift Y",
                                "@units": "/Piezo Configuration/Drift Y/@unit",
                            }
                        },
                        {
                            "Z": {
                                "raw_path": "/Piezo Configuration/Drift Z",
                                "@units": "/Piezo Configuration/Drift Z/@unit",
                            }
                        },
                    ],
                    "drift_correction_status": {
                        "raw_path": "/Piezo Configuration/Drift correction status"
                    },
                    "hv_gain_N[hv_gain_n]": [
                        {"X": {"raw_path": "/Piezo Configuration/HV Gain X"}},
                        {"Y": {"raw_path": "/Piezo Configuration/HV Gain Y"}},
                        {"Z": {"raw_path": "/Piezo Configuration/HV Gain Z"}},
                    ],
                    "tilt_N[tilt_n]": [
                        {
                            "X": {
                                "raw_path": "/Piezo Configuration/Tilt X",
                                "@units": "/Piezo Configuration/Tilt X/@unit",
                            }
                        },
                        {
                            "Y": {
                                "raw_path": "/Piezo Configuration/Tilt Y",
                                "@units": "/Piezo Configuration/Tilt X/@unit",
                            }
                        },
                        {
                            "Z": {
                                "raw_path": "/Piezo Configuration/Tilt Z",
                                "@units": "/Piezo Configuration/Tilt X/@unit",
                            }
                        },
                    ],
                    "piezo_material": {
                        "curvature_radius_N": [
                            {
                                "x": {
                                    "raw_path": "/Piezo Configuration/Curvature radius X",
                                    "@units": "/Piezo Configuration/Curvature radius X/@unit",
                                }
                            },
                            {
                                "y": {
                                    "raw_path": "/Piezo Configuration/Curvature radius Y",
                                    "@units": "/Piezo Configuration/Curvature radius Y/@unit",
                                }
                            },
                            {
                                "z": {
                                    "raw_path": "/Piezo Configuration/Curvature radius Z",
                                    "@units": "/Piezo Configuration/Curvature radius Z/@unit",
                                }
                            },
                        ]
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
                        },  # TODO: add to under stm[spm] definition
                        "z": {
                            "raw_path": "/Z-Controller/Z",
                            "@units": "/Z-Controller/Z/@unit",
                        },  # TODO:add to uder stm[spm] definition
                    },
                    "z_offset": "",
                    "tip_position_z": "",
                    "controller_name": {"raw_path": "/Z-Controller/Controller name"},
                    "controller_status": {
                        "raw_path": "/Z-Controller/Controller status"
                    },  # TODO: add to under stm[spm] definition
                    "switch_off_delay": {
                        "raw_path": "/Z-Controller/Switch off delay",
                        "@units": "/Z-Controller/Switch off delay/@unit",
                    },
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
