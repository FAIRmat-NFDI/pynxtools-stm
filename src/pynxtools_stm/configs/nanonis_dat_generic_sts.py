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
                "modulation_status": {
                    "raw_path": "/Lock-in/Lock-in status/value",
                },
                "reference_frequency": {
                    "raw_path": "/Lock-in/Frequency/value",
                    "@units": "/Lock-in/Frequency/unit",
                },
                "modulation_signal_type": {
                    "raw_path": "@default:Voltage",
                },
                "demodulated_signal": {
                    "raw_path": "@default:Current",
                    "@units": "/Lock-in/Demodulated signal/Current/unit",
                },
                "reference_amplitude": {  # TODO: Modify amplitude unit to ANY in NXlockin
                    "raw_path": "/Lock-in/Amplitude/value",
                    "@units": "/Lock-in/Modulated signal/Bias/unit",
                },
                "low_pass_N": [
                    {
                        "d1": {
                            "raw_path": "/Lock-in/LP Filter Cutoff D1/value",
                            "@units": "/Lock-in/LP Filter Cutoff D1/unit",
                        }
                    },
                    {
                        "d2": {
                            "raw_path": "/Lock-in/LP Filter Cutoff D2/value",
                            "@units": "/Lock-in/LP Filter Cutoff D2/unit",
                        }
                    },
                ],
                "lp_filter_order_N": [
                    {
                        "d1": {"raw_path": "/Lock-in/LP Filter Order D1/value"},
                        "d2": {"raw_path": "/Lock-in/LP Filter Order D2/value"},
                    }
                ],
                "hi_pass_N": [
                    {
                        "d1": {
                            "raw_path": "/Lock-in/HP Filter Cutoff D1/value",
                            "@units": "/Lock-in/HP Filter Cutoff D1/unit",
                        }
                    },
                    {
                        "d2": {
                            "raw_path": "/Lock-in/HP Filter Cutoff D2/value",
                            "@units": "/Lock-in/HP Filter Cutoff D2/unit",
                        }
                    },
                ],
                "hp_filter_order_N": [
                    {"d1": {"raw_path": "/Lock-in/HP Filter Order D1/value"}},
                    {"d2": {"raw_path": "/Lock-in/HP Filter Order D2/value"}},
                ],
                "ref_phase_N[ref_phase_n]": [
                    {
                        "d1": {
                            "raw_path": "/Lock-in/Reference phase D1/value",
                            "@units": "/Lock-in/Reference phase D1/unit",
                        }
                    },
                    {
                        "d2": {
                            "raw_path": "/Lock-in/Reference phase D2/value",
                            "@units": "/Lock-in/Reference phase D2/unit",
                        }
                    },
                ],
                "harmonic_order_N[harmonic_order_n]": [
                    {"d1": {"raw_path": "/Lock-in/Harmonic D1/value"}},
                    {"d2": {"raw_path": "/Lock-in/Harmonic D2/value"}},
                ],
            },
            "real_time_controller": {  # TODO: Extend RTC in NXspm
                "rcs_frequency": {
                    "raw_path": "/NanonisMain/RT Frequency/value",
                    "@units": "/NanonisMain/RT Frequency/unit",
                },
                "rcs_model": {
                    "raw_path": "/NanonisMain/RT Release/value",
                },
                "acquisition_time": {
                    "raw_path": "/NanonisMain/Acquisition Period/value",
                    "@units": "/NanonisMain/Acquisition Period/unit",
                },
                "animation_time": {
                    "raw_path": "/NanonisMain/Animations Period/value",
                    "@units": "/NanonisMain/Animations Period/unit",
                },
                "measurement_time": {
                    "raw_path": "/NanonisMain/Measurements Period/value",
                    "@units": "/NanonisMain/Measurements Period/unit",
                },
                "indicators_period": {
                    "raw_path": "/NanonisMain/Indicators Period/value",
                    "@units": "/NanonisMain/Indicators Period/unit",
                },
            },
            "bias_spectroscopy_environment": {
                "BIAS_SPECTROSCOPY[bias_spectroscopy]": {
                    "measurement_type": "",
                    "POSITIONER_SPM[positioner_spm]": {
                        "z_controller": {
                            "z_average_time": {
                                "raw_path": "/Bias Spectroscopy/Z Avg time/value",
                                "@units": "/Bias Spectroscopy/Z Avg time/unit",
                            },
                            "z_controller_time": {},
                            "z_controller_hold": {},
                            "record_final_z": {},
                        },
                        "z_offset": {
                            "raw_path": "/Bias Spectroscopy/Z offset/value",
                            "@units": "/Bias Spectroscopy/Z offset/unit",
                        },
                    },
                    "bias_sweep": {  # TODO: Extend in NXspm
                        "scan_type": "",
                        "settling_time": {
                            "raw_path": "/Bias Spectroscopy/Settling time/value",
                            "@units": "/Bias Spectroscopy/Settling time/unit",
                        },
                        "first_settling_time": {
                            "raw_path": "/Bias Spectroscopy/1st Settling time/value",
                            "@units": "/Bias Spectroscopy/1st Settling time/unit",
                        },
                        "end_settling_time": {
                            "raw_path": "/Bias Spectroscopy/End Settling time/value",
                            "@units": "/Bias Spectroscopy/End Settling time/unit",
                        },
                        "max_slew_rate": {
                            "raw_path": "/Bias Spectroscopy/Max Slew rate/value",
                            "@units": "/Bias Spectroscopy/Max Slew rate/unit",
                        },
                        "final_z": "",
                        "total_spectroscopy_time": "",
                        "sweep_number": {
                            "raw_path": "/Bias Spectroscopy/Number of sweeps/value"
                        },
                        "scan_region": {
                            "scan_range_bias": "",
                            "scan_offset_bias": {
                                "raw_path": "/Bias Spectroscopy/Scanfield/value",
                                "@units": "/Bias Spectroscopy/Scanfield/unit",
                            },
                            "scan_angle_N[scan_angle_n]": "",
                            "scan_start_bias": {
                                "raw_path": "/Bias Spectroscopy/Sweep Start/value",
                                "@units": "/Bias Spectroscopy/Sweep Start/unit",
                            },
                            "scan_end_bias": {
                                "raw_path": "/Bias Spectroscopy/Sweep End/value",
                                "@units": "/Bias Spectroscopy/Sweep End/unit",
                            },
                        },
                        "linear_sweep": {
                            "scan_speed": "",
                            "scan_time": "",
                            "forward_speed_bias": "",
                            "backward_speed_bias": "",
                            "scan_points_bias": {
                                "raw_path": "/Bias Spectroscopy/Num Pixel/value"
                            },
                            "step_size_bias": "",
                            "reset_bias": "",
                            "backward_weep": "",
                            "SCAN_DATA[scan_data]": [
                                {
                                    "data": {
                                        "name": "Current",
                                        "raw_path": "/dat_mat_components/Current/value",
                                        "@units": "/dat_mat_components/Current/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": [
                                            "/dat_mat_components/Bias calc/unit",
                                            "/dat_mat_components/Bias/unit",
                                        ],
                                        # "@long_name": "Bias Voltage",
                                    },
                                    "@title": "Bias Spectroscopy",
                                    "grp_name": "current",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 1X",
                                        "raw_path": "/dat_mat_components/LI Demod 1 X/value",
                                        "@units": "/dat_mat_components/LI Demod 1 X/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": [
                                            "/dat_mat_components/Bias calc/unit",
                                            "/dat_mat_components/Bias/unit",
                                        ],
                                    },
                                    "@title": "Lockin Signal 1X",
                                    "grp_name": "Lockin Demod 1X",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 1Y",
                                        "raw_path": "/dat_mat_components/LI Demod 1 Y/value",
                                        "@units": "/dat_mat_components/LI Demod 1 Y/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": [
                                            "/dat_mat_components/Bias calc/unit",
                                            "/dat_mat_components/Bias/unit",
                                        ],
                                    },
                                    "@title": "Lockin Signal 1Y",
                                    "grp_name": "Lockin Demod 1Y",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 2X",
                                        "raw_path": "/dat_mat_components/LI Demod 2 X/value",
                                        "@units": "/dat_mat_components/LI Demod 2 X/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": [
                                            "/dat_mat_components/Bias calc/unit",
                                            "/dat_mat_components/Bias/unit",
                                        ],
                                    },
                                    "@title": "Lockin Signal 2X",
                                    "grp_name": "Lockin Demod 2X",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 2Y",
                                        "raw_path": "/dat_mat_components/LI Demod 2 Y/value",
                                        "@units": "/dat_mat_components/LI Demod 2 Y/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": [
                                            "/dat_mat_components/Bias calc/unit",
                                            "/dat_mat_components/Bias/unit",
                                        ],
                                    },
                                    "@title": "Lockin Signal 2Y",
                                    "grp_name": "Lockin Demod 2Y",
                                },
                                {
                                    "data": {
                                        "name": "Current(filter)",
                                        "raw_path": "/dat_mat_components/Current [filt]/value",
                                        "@units": "/dat_mat_components/Current [filt]/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias [filt]/value",
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": "/dat_mat_components/Bias [filt]/unit",
                                    },
                                    "@title": "Bias Spectroscopy(filter)",
                                    "grp_name": "Current(filter)",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 1X(filter)",
                                        "raw_path": "/dat_mat_components/LI Demod 1 X [filt]/value",
                                        "@units": "/dat_mat_components/LI Demod 1 X [filt]/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias [filt]/value",
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": "/dat_mat_components/Bias [filt]/unit",
                                    },
                                    "@title": "Lockin Demod 1X(filter)",
                                    "grp_name": "Lockin_Demod_1X(filter)",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 1Y(filter)",
                                        "raw_path": "/dat_mat_components/LI Demod 1 Y [filt]/value",
                                        "@units": "/dat_mat_components/LI Demod 1 Y [filt]/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias [filt]/value",
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": "/dat_mat_components/Bias [filt]/unit",
                                    },
                                    "@title": "Lockin Demod 1Y(filter)",
                                    "grp_name": "Lockin_Demod_1Y(filter)",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 2X(filter)",
                                        "raw_path": "/dat_mat_components/LI Demod 2 X [filt]/value",
                                        "@units": "/dat_mat_components/LI Demod 2 X [filt]/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias [filt]/value",
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": "/dat_mat_components/Bias [filt]/unit",
                                    },
                                    "@title": "Lockin Demod 2X(filter)",
                                    "grp_name": "Lockin_Demod_2X(filter)",
                                },
                                {
                                    "data": {
                                        "name": "Lockin Demod 2Y(filter)",
                                        "raw_path": "/dat_mat_components/LI Demod 2 Y [filt]/value",
                                        "@units": "/dat_mat_components/LI Demod 2 Y [filt]/unit",
                                    },
                                    "0": {
                                        "name": "Bias Voltage",
                                        "raw_path": [
                                            "/dat_mat_components/Bias [filt]/value",
                                            "/dat_mat_components/Bias calc/value",
                                            "/dat_mat_components/Bias/value",
                                        ],
                                        "@units": "/dat_mat_components/Bias [filt]/unit",
                                    },
                                    "@title": "Lockin Demod 2Y(filter)",
                                    "grp_name": "Lockin_Demod_2Y(filter)",
                                },
                            ],  # TODO: Plotable data data will come here
                        },
                    },
                    "CIRCUIT[circuit]": "",
                },
                "current_sensor": {  # TODO: Extend in NXspm
                    "AMPLIFIER[amplifier]": {"current_gain": ""},
                    "current": {
                        "raw_path": "/Current/Current/value",
                        "@units": "/Current/Current/unit",
                    },
                    "current_calibration": {
                        "caliberation_time": "",
                        "coefficients": {
                            "raw_path": "/Current/Calibration/value",
                            "@units": "/Current/Calibration/unit",
                        },
                    },
                    "current_offset": {
                        "raw_path": "/Current/Offset/value",
                        "@units": "/Current/Offset/unit",
                    },
                    "current_gain": {"raw_path": "/Current/Gain/value"},
                },
                "independent_controllers": None,
                "measurement_sensors": None,
            },
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
                "piezo_configuration": {
                    "calibration": {
                        "calibration_type": {
                            "raw_path": "@default:active",
                        },
                        "calibration_coeffecient_N[calibration_coeffecient_n]": [
                            {
                                "x": {
                                    "raw_path": "/Piezo Configuration/Calib. X/value",
                                    "@units": "/Piezo Configuration/Calib. X/unit",
                                }
                            },
                            {
                                "y": {
                                    "raw_path": "/Piezo Configuration/Calib. Y/value",
                                    "@units": "/Piezo Configuration/Calib. Y/unit",
                                }
                            },
                            {
                                "z": {
                                    "raw_path": "/Piezo Configuration/Calib. Z/value",
                                    "@units": "/Piezo Configuration/Calib. Z/unit",
                                }
                            },
                        ],
                        "2nd_order_corr_N[2nd_order_corr_n]": [
                            {
                                "x": {
                                    "raw_path": "/Piezo Configuration/2nd order corr X/value",
                                    "@units": "/Piezo Configuration/2nd order corr X/unit",
                                }
                            },
                            {
                                "y": {
                                    "raw_path": "/Piezo Configuration/2nd order corr Y/value",
                                    "@units": "/Piezo Configuration/2nd order corr Y/unit",
                                }
                            },
                        ],
                        "drift_N[drift_n]": [
                            {
                                "x": {
                                    "value": "/Piezo Configuration/Drift X/value",
                                    "unit": "/Piezo Configuration/Drift X/unit",
                                }
                            },
                            {
                                "y": {
                                    "value": "/Piezo Configuration/Drift Y/value",
                                    "unit": "/Piezo Configuration/Drift Y/unit",
                                }
                            },
                            {
                                "z": {
                                    "value": "/Piezo Configuration/Drift Z/value",
                                    "unit": "/Piezo Configuration/Drift Z/unit",
                                }
                            },
                        ],
                        "hv_gain_N[hv_gain_n]": [
                            {"x": {"value": "/Piezo Configuration/HV Gain X/value"}},
                            {"y": {"value": "/Piezo Configuration/HV Gain Y/value"}},
                            {"z": {"value": "/Piezo Configuration/HV Gain Z/value"}},
                        ],
                        "tilt_N[tilt_n]": [
                            {
                                "x": {
                                    "value": "/Piezo Configuration/Tilt X/value",
                                    "@units": "/Piezo Configuration/Tilt X/unit",
                                }
                            },
                            {
                                "y": {
                                    "value": "/Piezo Configuration/Tilt Y/value",
                                    "@units": "/Piezo Configuration/Tilt Y/unit",
                                }
                            },
                            {
                                "z": {
                                    "value": "/Piezo Configuration/Tilt Z/value",
                                    "@units": "/Piezo Configuration/Tilt Z/unit",
                                }
                            },
                        ],
                        "drift_correction_status": {
                            "raw_path": [
                                "/Piezo Configuration/Drift correction status/value",
                                "/Piezo Calibration/Drift correction status/value",
                            ]
                        },
                    },
                    "piezo_material": {
                        "curvature_radius_N": [
                            {
                                "x": {
                                    "raw_path": "/Piezo Configuration/Curvature radius X/value",
                                    "@units": "/Piezo Configuration/Curvature radius X/unit",
                                }
                            },
                            {
                                "y": {
                                    "raw_path": "/Piezo Configuration/Curvature radius Y/value",
                                    "@units": "/Piezo Configuration/Curvature radius Y/unit",
                                }
                            },
                            {
                                "z": {
                                    "raw_path": "/Piezo Configuration/Curvature radius Z/value",
                                    "@units": "/Piezo Configuration/Curvature radius Z/unit",
                                }
                            },
                        ],
                    },
                },
                "POSITIONER_SPM[positioner_spm]": {
                    "z_controller": {
                        "controller_name": {
                            "raw_path": "/Z-Controller/Controller name/value",
                        },
                        "controller_status": {
                            "raw_path": "/Z-Controller/Controller status/value"
                        },
                        "set_point": {
                            "raw_path": "/Z-Controller/Setpoint/value",
                            "@units": "/Z-Controller/Setpoint/unit",
                        },
                        "tip_lift": {
                            "raw_path": "/Z-Controller/TipLift/value",
                            "@units": "/Z-Controller/TipLift/unit",
                        },
                        "z": {
                            "raw_path": "/Z-Controller/Z/value",
                            "@units": "/Z-Controller/Z/unit",
                        },
                        "K_i_value[k_i_value]": {
                            "raw_path": "/Z-Controller/I gain/value"
                        },
                        "K_p_value[k_p_value]": {
                            "raw_path": "/Z-Controller/P gain/value"
                        },
                        "K_t_const[k_t_const]": {
                            "raw_path": "/Z-Controller/Time const/value",
                            "@units": "/Z-Controller/Time const/unit",
                        },
                    },
                },
                "x": {"raw_path": "/X/value", "@units": "/X/unit"},
                "y": {"raw_path": "/Y/value", "@units": "/Y/unit"},
                "z": {"raw_path": "/Z/value", "@units": "/Z/unit"},
            },
            "scan_environment": {
                "scan_name": {
                    "raw_path": "/Scan/series name/value",
                },
                "SCAN_CONTROL[bias_spec_scan_control]": {  # TODO: Rename it bias_spec_scan_control
                    "scan_name": {  # TODO: Extend in NXspm
                        "raw_path": "/Scan/series name/value",
                    },
                    "mesh_SCAN[mesh_scan]": {
                        "forward_speed_N[forward_speed_n]": {
                            "raw_path": "/Scan/speed forw./value",
                            "@units": "/Scan/speed forw./unit",
                        },
                        "backward_speed_N[backward_speed_n]": {
                            "raw_path": "/Scan/speed backw./value",
                            "@units": "/Scan/speed backw./unit",
                        },
                        "scan_speed": {"@units": None},
                        "scan_time": {"@units": None},
                        "SCAN_DATA[scan_data]": None,
                    },
                    "scan_region": {
                        "scan_angle_N[scan_angle_n]": {
                            "raw_path": "",
                            "#note": "Handled in construct_scan_region_grp",
                            "@units": "@default:deg",
                        },
                        "scan_offset_N[scan_offset_n]": {
                            "#note": "Handled in construct_scan_region_grp",
                            "raw_path": "/Scan/Scanfield/value",
                        },
                        "scan_range_N[scan_range_n]": {
                            "#note": "Handled in construct_scan_region_grp",
                            "raw_path": "/Scan/Scanfield/value",
                            "@units": [
                                "/Scan/Scanfield/unit",
                                "/X/unit",
                                "/Y/unit",
                                "/Z/unit",
                            ],
                        },
                    },
                    "scan_type": None,  # Check it it is optional
                },
                "cryo_bottom_temp": {"@units": None},
                "cryo_shield_temp": {"@units": None},
                "tip_temp": {
                    "raw_path": "/Temperature 1/Temperature 1/value",
                    "@units": "/Temperature 1/Temperature 1/unit",
                },
                "cryo_shield_temperature": "",
                "cryo_temperature": "",
                "tip_temperature": "",
                "sample_bias_votage": {
                    "bias_voltage": {
                        "raw_path": "/Bias/Bias/value",
                        "@units": "/Bias/Bias/unit",
                    },
                    "bias_calibration": {
                        "coefficients": {
                            "raw_path": "/Bias/Calibration/value",
                            "@units": "/Bias/Calibration/unit",
                        },
                    },
                },
            },
            "TEMPERATURE[cryo_shield_temperature]": {
                "CHANNEL_temp[channel_temp]": "",
                "temperature_calibration": {"coefficients": ""},
                "TEMPERATURE_DATA[temperature_data]": "",
            },
            "TEMPERATURE[cryo_temperature]": {
                "CHANNEL_temp[channel_temp]": "",
                "temperature_calibration": {"coefficients": ""},
                "TEMPERATURE_DATA[temperature_data]": "",
            },
            "TEMPERATURE[tip_temperature]": {
                "CHANNEL_temp[channel_temp]": "",
                "temperature_calibration": {"coefficients": ""},
                "TEMPERATURE_DATA[temperature_data]": [
                    {
                        "data": {
                            "name": "temperature1",
                            "raw_path": "/dat_mat_components/Temperature 1/value",
                            "@units": "/dat_mat_components/Temperature 1/unit",
                        },
                        "0": {  # axis index
                            "name": "Bias Voltage",
                            "raw_path": [
                                "/dat_mat_components/Bias calc/value",
                                "/dat_mat_components/Bias/value",
                            ],
                            "@units": [
                                "/dat_mat_components/Bias calc/unit",
                                "/dat_mat_components/Bias/unit",
                            ],
                            "axis_ind": 0,
                        },
                        "@title": "Bias Spectroscopy Temperature1",
                        "grp_name": "temperature1",
                    },
                    {
                        "data": {
                            "name": "temperature1(filter)",
                            "raw_path": "/dat_mat_components/Temperature 1 [filt]/value",
                            "@units": "/dat_mat_components/Temperature 1 [filt]/unit",
                        },
                        "0": {
                            "name": "Bias Voltage",
                            "raw_path": [
                                "/dat_mat_components/Bias calc/value",
                                "/dat_mat_components/Bias/value",
                            ],
                            "@units": [
                                "/dat_mat_components/Bias calc/unit",
                                "/dat_mat_components/Bias/unit",
                            ],
                            "axis_ind": 0,
                        },
                        "@title": "Bias Spectroscopy Temperature1(filter)",
                        "grp_name": "temperature1(filter)",
                    },
                ],
            },
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
    }
}
