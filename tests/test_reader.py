"""
Basic example based test for the stm reader
"""
# import logging
# import os
# import pytest
# import xml.etree.ElementTree as ET
# from glob import glob

# from pynxtools.dataconverter.helpers import (
#     generate_template_from_nxdl,
#     validate_data_dict,
# )
# from pynxtools.nexus import nexus
# from pynxtools.dataconverter.writer import Writer
# from pynxtools.dataconverter.template import Template
# from pynxtools.nexus.nxdl_utils import get_nexus_definitions_path

# from pynxtools_stm.reader import STMReader


# def get_log_file(nxs_file, log_file_nm, tmp_path):
#     logger = logging.getLogger(__name__)
#     logger.handlers.clear()
#     logger.setLevel(logging.DEBUG)
#     log_file = os.path.join(tmp_path, log_file_nm)
#     handler = logging.FileHandler(log_file, "w")
#     formatter = logging.Formatter("%(levelname)s - %(message)s")
#     handler.setLevel(logging.DEBUG)
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     nexus_helper = nexus.HandleNexus(logger, nxs_file, None, None)
#     nexus_helper.process_nexus_master_file(None)
#     return log_file


# class TestSTMReader:
#     # Try with convert()
#     @pytest.mark.parametrize(
#         "nxdl,example_data,ref_nexus_file",
#         [
#             (
#                 "NXsts",
#                 "data/in_sts_nanonis_5e",
#                 "data/out_sts_nanonis_5e/sts_nanonis_5e.nxs",
#             ),
#             (
#                 "NXsts",
#                 "data/in_sts_nanonis_4_5",
#                 "data/out_sts_nanonis_4_5/sts_nanonis_4_5.nxs",
#             ),
#             (
#                 "NXsts",
#                 "data/in_stm_nanonis_5e",
#                 "data/out_stm_nanonis_5e/stm_nanonis_5e.nxs",
#             ),
#         ],
#     )
#     def test_example_data(self, nxdl, example_data, ref_nexus_file, tmp_path, caplog):
#         """
#         Test the example data for the stm reader
#         """

#         tmp_output = f"{tmp_path}/{os.sep}/output.nxs"
#         reader = STMReader
#         assert callable(reader.read)

#         def_dir = get_nexus_definitions_path()

#         data_dir = os.path.join(os.path.dirname(__file__), example_data)
#         ref_nexus_file = os.path.join(os.path.dirname(__file__), ref_nexus_file)
#         input_files = sorted(glob(os.path.join(data_dir, "*")))
#         assert nxdl in reader.supported_nxdls
#         nxdl_file = os.path.join(def_dir, "contributed_definitions", f"{nxdl}.nxdl.xml")

#         root = ET.parse(nxdl_file).getroot()
#         template = Template()
#         generate_template_from_nxdl(root, template)

#         read_data = reader().read(
#             template=Template(template), file_paths=tuple(input_files)
#         )

#         assert isinstance(read_data, Template)
#         with caplog.at_level("ERROR", "WARNING"):
#             is_success = validate_data_dict(template, read_data, root)
#         assert is_success, "Validation failed"
#         for record in caplog.records:
#             if record.levelname == "WARNING" or record.levelname == "ERROR":
#                 assert False, record.message
#         Writer(read_data, nxdl_file, tmp_output).write()

#         ref_log = get_log_file(ref_nexus_file, "ref_nexus.log", tmp_path)
#         gen_log = get_log_file(tmp_output, "gen_nexus.log", tmp_path)
#         with open(gen_log, "r", encoding="utf-8") as gen:
#             gen_lines = gen.readlines()
#         with open(ref_log, "r", encoding="utf-8") as ref:
#             ref_lines = ref.readlines()
#         if len(gen_lines) != len(ref_lines):
#             assert False, "Log files are different"
#         for ind, (gen_l, ref_l) in enumerate(zip(gen_lines, ref_lines)):
#             if gen_l != ref_l:
#                 # skip version conflicts
#                 if gen_l.startswith("DEBUG - value: v") and ref_l.startswith(
#                     "DEBUG - value: v"
#                 ):
#                     continue
#                 assert False, (
#                     f"Log files are different at line {ind}"
#                     f" generated: {gen_l} \n referenced : {ref_l}"
#                 )


import os
from pynxtools_stm.reader import STMReader
import pytest
from pynxtools.dataconverter.test_suite.reader_plugin import ReaderTest

module_dir = os.path.dirname(os.path.abspath(__file__))
@pytest.mark.parametrize(
    "nxdl,reader, example_data,ref_nexus_file",
    [
        (
            "NXsts",
            STMReader,
            f"{module_dir}/data/in_sts_nanonis_5e",
            f"{module_dir}/data/out_sts_nanonis_5e/sts_nanonis_5e.nxs",
        ),
        (
            "NXsts",
            STMReader,
            f"{module_dir}/data/in_sts_nanonis_4_5",
            f"{module_dir}/data/out_sts_nanonis_4_5/sts_nanonis_4_5.nxs",
        ),
        (
            "NXsts",
            STMReader,
            f"{module_dir}/data/in_stm_nanonis_5e",
            f"{module_dir}/data/out_stm_nanonis_5e/stm_nanonis_5e.nxs",
        ),
    ],
)
def test_stm_reader(nxdl, reader, example_data, ref_nexus_file, tmp_path, caplog):
    # test plugin reader
    test = ReaderTest(nxdl, reader, example_data, ref_nexus_file, tmp_path, caplog)
    test.convert_to_nexus()
    test.check_reproducibility_of_nexus()
