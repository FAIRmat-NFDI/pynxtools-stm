# Python packages
## Some possible python packages that help to read Matrix from scienta omicron files
1.   https://pypi.org/project/access2theMatrix/ (not tested yet)
2. https://github.com/KoenImdea/Matrix-Image-Analysis/tree/main (not tested yet)
   This lib may help to understand what type of data is rendered by python package 1.

3. Got some endocing that have been tested out to the file `sm4` file
       encodings[] = {
        "UTF-16", "CP1252", "CP1251", "CP1250", "CP1253", "CP1254", "CP1255", "CP1256", "CP1257", "CP1258",
    };
   in line : 622 in file anfatec from the Gwyddion package. Seems `cp1255` works though not all the data.
   a. The following link may help to understand how to read the sm5 file.
      https://github.com/rescipy-project/spym/blob/master/spym/io/rhksm4/_sm4.py#L43
      