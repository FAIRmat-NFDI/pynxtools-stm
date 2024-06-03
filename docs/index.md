# STS reader
***Note: Though the reader name is STS reader, it also supports STM experiment species. This is the first version of the reader according to the NeXus application definition [NXsts](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXsts.nxdl.xml) which is a generic template of concept definitions for STS and STM experiments. Later on, the application definitions and readers specific to STM, STS and AFM will be available. To stay up-to-date, keep visiting this page from time to time. From now onwards, when we mention STS, we are referring to both STM and STS techniques.***

The prime purpose of the reader is to transform data from measurement files into community-defined concepts constructed by the SPM community which allows experimentalists to store, organize, search, analyze, and share experimental data (only within the [NOMAD](https://nomad-lab.eu/nomad-lab/) platform) among the scientific communities. To utilize the reader one needs:  

1. A data file from the experiment
2. An ELN (Electronic Lab Notebook) file (to add user-provided data that does not come along with the experimental data file)
3. A config file that maps the raw data coming from both the experimental data file and the ELN to the corresponding NeXus concepts.

**TODO: Here discuss about NXsts NeXus application definition**

## Reader Notes:
- Reader builds on [NXsts](https://github.com/FAIRmat-NFDI/nexus_definitions/blob/fairmat/contributed_definitions/NXsts.nxdl.xml) application definition
- Needs an experimental file, a config file and a eln file
- Can parse Scanning Tunneling Spectroscopy (STS) from
    - Nanonis: Generic 5e, Generic 4.5
- Can parse Scanning Tunneling Microscopy (STM) from
    - Nanonis: Generic 5e, Generic 4.5


## Useful Functions:
There are a few functions that you can utilize to make this reader compatible with your data:

- **Function get_stm_raw_file_info()**: For `STM` experiment the function can return you the slash separated dict in a text file. This dict helps to write or modify the config file according to your raw data file. 

  ```python
  from pynxtools_stm import get_stm_raw_file_info

  # for stm (.sxm) file
  get_stm_raw_file_info('STM_nanonis_generic_5e.sxm')
  ```

- **get_sts_raw_file_info**: For `STS` experiment to get the slash separated dict from the `STS` raw file one can use this function. It will write a txt file in the working directory.

  ```python
  from pynxtools_stm import get_sts_raw_file_info

  # for sts (.dat) file
  get_sts_raw_file_info('STS_nanonis_generic_5e_1.dat')
  ```


## Contact Person in FAIRmat for this Reader
**Rubel Mozumder (mozumder@physik.hu-berlin.de)**
