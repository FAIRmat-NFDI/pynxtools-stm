import os
from pynxtools.testing.nexus_conversion import ReaderTest
import logging

logger = logging.getLogger(__file__)
module_dir = os.path.dirname(os.path.abspath(__file__))


list_example = [
    (
        "NXsts",
        "sts",
        f"{module_dir}/data/stm_nanonis_5e",
        f"{module_dir}/data/",
        logger,
    ),
    (
        "NXsts",
        "sts",
        f"{module_dir}/data/sts_nanonis_5e",
        f"{module_dir}/data/",
        logger,
    ),
    (
        "NXsts",
        "sts",
        f"{module_dir}/data/stm_nanonis_4_5",
        f"{module_dir}/data/",
        logger,
    ),
    (
        "NXsts",
        "sts",
        f"{module_dir}/data/sts_nanonis_4_5",
        f"{module_dir}/data/",
        logger,
    ),
]


def test_stm_reader(nxdl, reader_name, files_or_dir, tmp_path, caplog):
    "Generic test from pynxtools."
    # test plugin reader
    test = ReaderTest(nxdl, reader_name, files_or_dir, tmp_path, caplog)
    test.convert_to_nexus(caplog_level="ERROR", ignore_undocumented=True)
    test.check_reproducibility_of_nexus()


for x in list_example:
    test_stm_reader(*x)
