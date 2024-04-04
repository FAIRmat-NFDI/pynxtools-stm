"""
Basic example based test for the stm reader
"""
import logging
import os
import pytest
import xml.etree.ElementTree as ET
from glob import glob

from pynxtools.dataconverter.helpers import (
    generate_template_from_nxdl,
    validate_data_dict,
)
from pynxtools.nexus import nexus
from pynxtools.dataconverter.writer import Writer
from pynxtools.dataconverter.template import Template
from pynxtools.nexus.nxdl_utils import get_nexus_definitions_path

from pynxtools_stm.reader import STMReader


class TestSTMReader:
    out: dict = {'data/out_sts_nanonis_5e': None,
                 'data/out_sts_nanonis_4_5': None,
                 'data/out_stm_nanonis_5e': None,
                 }
    # Try with convert()
    @pytest.mark.parametrize(
    "nxdl,example_data",
    [
        ("NXsts", "data/in_sts_nanonis_5e"),
        ("NXsts", "data/in_sts_nanonis_4_5"),
        ("NXsts", "data/in_stm_nanonis_5e"),
    ],
    )
    def test_example_data(self, nxdl, example_data, tmp_path, caplog):
        """
        Test the example data for the stm reader
        """

        tmp_output = f"{tmp_path}/{os.sep}/output.nxs"
        reader = STMReader
        assert callable(reader.read)

        def_dir = get_nexus_definitions_path()

        data_dir = os.path.join(os.path.dirname(__file__), example_data)
        input_files = sorted(glob(os.path.join(data_dir, "*")))
        assert nxdl in reader.supported_nxdls
        nxdl_file = os.path.join(def_dir, "contributed_definitions", f"{nxdl}.nxdl.xml")

        root = ET.parse(nxdl_file).getroot()
        template = Template()
        generate_template_from_nxdl(root, template)

        read_data = reader().read(
            template=Template(template), file_paths=tuple(input_files)
        )

        assert isinstance(read_data, Template)
        # 30 -> WARNING, 40 -> ERROR
        with caplog.at_level('ERROR', 'WARNING'):
            is_success = validate_data_dict(template, read_data, root)
        assert is_success, "Validation failed"
        for record in caplog.records:
            if record.levelname == "WARNING" or record.levelname == "ERROR":
                assert False, record.message
        Writer(read_data, nxdl_file, tmp_output).write()
        TestSTMReader.out[example_data.replace('data/in', 'data/out')] = tmp_output

    @pytest.mark.parametrize(
        "ref_nexus_file",
        [
            ("data/out_sts_nanonis_5e"),
            ("data/out_sts_nanonis_4_5"),
            ("data/out_stm_nanonis_5e"),
        ],
    )
    def test_repoducibility_of_nxs_file(self, ref_nexus_file, tmp_path):
        """Check if mpes example can be reproduced"""
        # dataconverter
        ref_dir = os.path.dirname(__file__)
        ref_file = glob(os.path.join(ref_dir, ref_nexus_file, "*.nxs"))[0]

        gen_file = TestSTMReader.out[ref_nexus_file]

        # check generated nexus file
        def get_log_file(nxs_file, log_file_nm):
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            log_file = os.path.join(tmp_path, log_file_nm)
            handler = logging.FileHandler(log_file, "w")
            formatter = logging.Formatter("%(levelname)s - %(message)s")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            nexus_helper = nexus.HandleNexus(logger, nxs_file, None, None)
            nexus_helper.process_nexus_master_file(None)
            return log_file
        ref_log = get_log_file(ref_file, "ref_nexus.log")
        gen_log = get_log_file(gen_file, "gen_nexus.log")
        with open(gen_log, "r", encoding="utf-8") as gen, open(ref_log, "r", encoding="utf-8") as ref:
            if len(gen) != len(ref):
                assert False, "Log files are different"
            for line, gen_l, ref_l in enumerate(zip(gen, ref)):
                if gen_l != ref_l:
                    assert False, f"Log files are different at line {line}"
