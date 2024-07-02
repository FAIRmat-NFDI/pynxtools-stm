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
        ("NXsts", "sts", f"{module_dir}/data/stm_nanonis_5e"),
        ("NXsts", "sts", f"{module_dir}/data/sts_nanonis_5e"),
        ("NXsts", "sts", f"{module_dir}/data/stm_nanonis_4_5"),
        ("NXsts", "sts", f"{module_dir}/data/sts_nanonis_4_5"),
    ],
)
def test_stm_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    "Generic test from pynxtools."
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus(caplog_level="ERROR", ignore_undocumented=True)
    test.check_reproducibility_of_nexus()
