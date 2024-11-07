!#/local/bin/bash

# STS Nanonis
echo " !!! Converting Nanonis STS data !!! "
find tests/data/nanonis/sts/version_gen_5e_default_config -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXspm --reader spm --output sts_5e_default_config.nxs
find tests/data/nanonis/sts/version_gen_5e_default_config -type f -name '*.nxs' | xargs mv sts_5e_default_config.nxs

find tests/data/nanonis/sts/version_gen_5e_with_described_nxdata -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXspm --reader spm --output sts_5e_with_described_nxdata.nxs
find tests/data/nanonis/sts/version_gen_5e_with_described_nxdata -type f -name '*.nxs' | xargs mv sts_5e_with_described_nxdata.nxs

# AFM Nanonis
echo " !!! Converting Nanonis AFM data !!! "
find tests/data/nanonis/afm/version_gen_4_default_config -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXafm --reader spm --output afm_4_with_default_config.nxs
find tests/data/nanonis/afm/version_gen_4_default_config -type f -name '*.nxs' | xargs mv afm_4_with_default_config.nxs

find tests/data/nanonis/afm/version_gen_4_with_described_nxdata -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXafm --reader spm --output afm_4_with_described_nxdata.nxs
find tests/data/nanonis/afm/version_gen_4_with_described_nxdata -type f -name '*.nxs' | xargs mv afm_4_with_described_nxdata.nxs

# STM Nanonis
echo " !!! Converting Nanonis STM data !!! "
find tests/data/nanonis/stm/version_gen_4_5_default_config -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXstm --reader spm --output stm_4_5_default_config.nxs
find tests/data/nanonis/stm/version_gen_4_5_default_config -type f -name '*.nxs' | xargs mv stm_4_5_default_config.nxs

find tests/data/nanonis/stm/version_gen_4_5_with_described_nxdata -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXstm --reader spm --output stm_4_5_with_described_nxdata.nxs
find tests/data/nanonis/stm/version_gen_4_5_with_described_nxdata -type f -name '*.nxs' | xargs mv stm_4_5_with_described_nxdata.nxs

