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
from pynxtools.dataconverter.writer import Writer
from pynxtools.dataconverter.template import Template

from pynxtools.definitions.dev_tools.utils.nxdl_utils import get_nexus_definitions_path
from pynxtools_stm.reader import STMReader

@pytest.mark.parametrize("nxdl,example_data", 
                         [('NXsts', 'data/sts_nanonis_5e'),
                          ('NXsts', 'data/sts_nanonis_4_5'),
                          ('NXsts', 'data/stm_nanonis_5e'),])
class TestSTMReader:

    # Try with convert()
    def test_example_data(self, nxdl, example_data, tmp_path):

        """
        Test the example data for the stm reader
        """

        tmp_output = f"{tmp_path}/{os.sep}/output"
        reader = STMReader
        assert callable(reader.read)

        def_dir = get_nexus_definitions_path()

        data_dir = os.path.join(os.path.dirname(__file__), example_data)
        input_files = sorted(glob(os.path.join(data_dir, "*")))
        assert nxdl in reader.supported_nxdls
        nxdl_file = os.path.join(
            def_dir, "contributed_definitions", f"{nxdl}.nxdl.xml"
        )

        root = ET.parse(nxdl_file).getroot()
        template = Template()
        generate_template_from_nxdl(root, template)

        read_data = reader().read(
            template=Template(template), file_paths=tuple(input_files)
        )

        assert isinstance(read_data, Template)
        assert validate_data_dict(template, read_data, root)
        Writer(read_data, nxdl_file, tmp_output).write()
