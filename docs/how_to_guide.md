# How-To-Guide
## How-To Run the Reader from CLI
In the command line interface, input files can be passed as positional arguments. Other arguments like the `reader` and the `nxdl` shall be given as keyword arguments.
## Run STS Reader
The following command can be used to run the `STS` reader:
```bash
!dataconverter \
--reader sts \
--nxdl NXsts \
<path-to STS_nanonis_generic_5e_1.dat> \
<path-to config_file_for_dat.json> \
<path-to Nanonis_Eln.yaml> \
--output ./final_sts_dev.nxs
```

## Run STM Reader
Use the following command to run the `STM` reader:
```bash
!dataconverter \
--reader sts \
--nxdl NXsts \
<path-to STM_nanonis_generic_5e.sxm> \
<path-to config_file_for_sxm.json> \
<path-to Nanonis_Eln.yaml> \
--output final_stm_dev_.nxs
```
## Want to Contribute or Extend the Reader Functionality
We appreciate any comments, extentions or improvements on the existing reader from users. Currently the reader supports the versions `4.5`, `5e` from `Generic` model of `Nanonis` vendor. To include the other versions of the `Generic` model, extend the class `StmNanonisGeneric` and `StsNanonisGeneric` by including versions in `__version__` attribute. Also include the model and version of the brand in `Spm` class. 
### How to Contribute or Extend the Reader Functionality
If you want to add the different versions of the `Nanonis Generic` model for `STM` experiment, please check the `STM_Nanonis` class for `STM` experiment, which parses the data into a python dict of slash (`/`) separated key-value pair (see the right part of the config file). The class uses the `nanonispy` sub-package to read the `sxm` type file. That should also be checked and modified (if needed).

If you add different versions of the `Nanonis Generic` model for `STS` experiment, please check the `BiasSpecData_Nanonis` class for `STS` experiment. The class reads the raw data from the raw files into a dict of slash separated key-value pair (see the config file). 

If you go for a completely different model (e.g., from a different brand), please handle it in a new module with different functions and classes. 

Later on, please add the relevant tests in the plugin test.

Done! Great, then please create a pull request.