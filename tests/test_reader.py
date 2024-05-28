"""
Basic example based test for the stm reader
"""

import logging
import os

import pytest
from pynxtools.nexus import nexus
from pynxtools.testing.nexus_conversion import ReaderTest


def get_log_file(nxs_file, log_file, tmp_path):
    """Get log file for the nexus file with read_nexus tools."""
    logger = logging.getLogger(__name__)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(tmp_path, log_file)
    handler = logging.FileHandler(log_file, "w")
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    nexus_helper = nexus.HandleNexus(logger, nxs_file, None, None)
    nexus_helper.process_nexus_master_file(None)
    return log_file


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
    test.convert_to_nexus(ignore_undocumented=True)
    test.check_reproducibility_of_nexus()
