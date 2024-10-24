from pynxtools_stm.reader import SPMReader

from pynxtools.dataconverter.convert import convert
import os

from pynxtools_stm.parsers import write_spm_raw_file_data

cwd = os.getcwd()


def run_converter():
    technique = "sts"
    default_config = False
    is_config_described = True
    data_file = None
    eln_file = None
    reader = None
    output = None
    nxdl = None
    input_files = []
    if technique == "sts":
        nxdl = "NXspm"
        data_file = "/home/rubel/NOMAD-FAIRmat/GH/pynxtools-stm/tests/data/nanonis/sts/version_gen_5e/STS_nanonis_generic_5e_1.dat"
        eln_file = "/home/rubel/NOMAD-FAIRmat/GH/pynxtools-stm/tests/data/nanonis/sts/version_gen_5e/eln_data.yaml"
        reader = "spm"
        output = "sts_5e_default_config.nxs"
        input_files = [data_file, eln_file]
    elif technique == "afm" and default_config:
        nxdl = "NXafm"
        data_file = f"{cwd}/tests/data/nanonis/afm/version_gen_4_default_config/A151216.123306-02602.sxm"
        eln_file = (
            f"{cwd}/tests/data/nanonis/afm/version_gen_4_default_config/eln_data.yaml"
        )

        reader = "spm"
        output = "output_afm_4_with_default_config.nxs"
        input_files = [data_file, eln_file]
    elif technique == "afm" and not default_config and is_config_described:
        nxdl = "NXafm"
        data_file = f"{cwd}/tests/data/nanonis/afm/version_gen_4_with_described_nxdata/A151216.123306-02602.sxm"
        eln_file = f"{cwd}/tests/data/nanonis/afm/version_gen_4_with_described_nxdata/eln_data.yaml"
        config_file = f"{cwd}/tests/data/nanonis/afm/version_gen_4_with_described_nxdata/config.json"
        reader = "spm"
        output = "output_afm_4_with_described_nxdata.nxs"
        input_files = [data_file, eln_file, config_file]

    elif technique == "stm" and default_config:
        nxdl = "NXstm"
        data_file = f"{cwd}/tests/data/nanonis/stm/version_gen_4_5_default_config/STM_nanonis_generic_4_5.sxm"
        eln_file = (
            f"{cwd}/tests/data/nanonis/stm/version_gen_4_5_default_config/eln_data.yaml"
        )
        reader = "spm"
        output = "output_stm_4_5_with_default_config.nxs"
        input_files = [data_file, eln_file]
    # elif technique == "stm" and not default_config and is_config_described:
    #     nxdl = "NXstm"
    #     data_file = f"{cwd}/tests/data/nanonis/stm/version_gen_4_5_with_described_nxdata/STM_nanonis_generic_4_5.sxm"
    #     eln_file = f"{cwd}/tests/data/nanonis/stm/version_gen_4_5_with_described_nxdata/eln_data.yaml"
    #     config_file = f"{cwd}/tests/data/nanonis/stm/version_gen_4_5_with_described_nxdata/config.json"
    #     reader = "spm"
    #     output = "output_stm_4_5_described_nxdata.nxs"
    # elif technique == "stm" and not default_config and not is_config_described:
    #     nxdl = "NXstm"
    #     data_file = (
    #         f"{cwd}/tests/data/nanonis/stm/version_gen_4_5/STM_nanonis_generic_4_5.sxm"
    #     )
    #     eln_file = f"{cwd}/tests/data/nanonis/stm/version_gen_4_5/eln_data.yaml"
    #     config_file = f"{cwd}/tests/data/nanonis/stm/version_gen_4_5/config.json"
    #     reader = "spm"
    #     output = "output_stm_4_5.nxs"
    #     input_files = [data_file, eln_file, config_file]

    convert(input_files, reader, nxdl, output)


if __name__ == "__main__":
    run_converter()

    # from pynxtools_stm.parsers import write_spm_raw_file_data
    # data_file = (
    #     f"{cwd}/tests/data/nanonis/stm/version_gen_4_5/STM_nanonis_generic_4_5.sxm"
    # )

    # write_spm_raw_file_data(
    #     raw_file=data_file,
    #     output_file="/home/rubel/NOMAD-FAIRmat/GH/pynxtools-stm/tests/data/nanonis/afm/version_gen_4/A151216.123306-02602.txt",
    # )
