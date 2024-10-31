!#/local/bin/bash

find tests/data/sts_nanonis_4_5/ -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXsts --reader sts --output sts_nanonis_generic_4_5.nxs
find tests/data/sts_nanonis_4_5/ -type f -name '*.nxs' | xargs mv sts_nanonis_generic_4_5.nxs    

find tests/data/sts_nanonis_5e/ -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXsts --reader sts --output sts_nanonis_generic_5e.nxs
find tests/data/sts_nanonis_5e/ -type f -name '*.nxs' | xargs mv sts_nanonis_generic_5e.nxs    

find tests/data/stm_nanonis_4_5/ -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXsts --reader sts --output stm_nanonis_generic_4_5.nxs
find tests/data/stm_nanonis_4_5/ -type f -name '*.nxs' | xargs mv stm_nanonis_generic_4_5.nxs    


find tests/data/stm_nanonis_5e/ -type f ! -name '*.nxs' | xargs dataconverter --nxdl NXsts --reader sts --output stm_nanonis_generic_5e.nxs
find tests/data/stm_nanonis_5e/ -type f -name '*.nxs' | xargs mv stm_nanonis_generic_5e.nxs    