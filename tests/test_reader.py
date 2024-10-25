"""
Basic example based test for the stm reader
"""

import os

import pytest
from pynxtools.testing.nexus_conversion import ReaderTest

module_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "nxdl,reader_name,files_or_dir",
    [
        # ("NXstm", "spm", f"{module_dir}/data/nanonis/stm/version_gen_4_5"),
        (
            "NXspm",
            "spm",
            f"{module_dir}/data/nanonis/sts/version_gen_5e_with_described_nxdata",
        ),
        (
            "NXspm",
            "spm",
            f"{module_dir}/data/nanonis/sts/version_gen_5e_default_config",
        ),
        # ("NXsts", "sts", f"{module_dir}/data/sts_nanonis_4_5"),
    ],
)
def test_sts_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    "Generic test from pynxtools."
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus(caplog_level="ERROR", ignore_undocumented=True)
    test.check_reproducibility_of_nexus()


@pytest.mark.parametrize(
    "nxdl,reader_name,files_or_dir",
    [
        # ("NXstm", "spm", f"{module_dir}/data/nanonis/stm/version_gen_4_5"),
        (
            "NXstm",
            "spm",
            f"{module_dir}/data/nanonis/stm/version_gen_4_5_with_described_nxdata",
        ),
        (
            "NXstm",
            "spm",
            f"{module_dir}/data/nanonis/stm/version_gen_4_5_default_config",
        ),
        # ("NXsts", "sts", f"{module_dir}/data/sts_nanonis_4_5"),
    ],
)
def test_stm_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    "Generic test from pynxtools."
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus(caplog_level="ERROR", ignore_undocumented=True)
    test.check_reproducibility_of_nexus()


@pytest.mark.parametrize(
    "nxdl,reader_name,files_or_dir",
    [
        (
            "NXafm",
            "spm",
            f"{module_dir}/data/nanonis/afm/version_gen_4_with_described_nxdata",
        ),
        (
            "NXafm",
            "spm",
            f"{module_dir}/data/nanonis/afm/version_gen_4_default_config",
        ),
    ],
)
def test_afm_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    "Generic test from pynxtools."
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus(caplog_level="ERROR", ignore_undocumented=True)
    test.check_reproducibility_of_nexus()
