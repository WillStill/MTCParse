
# ⚠**UNDER DEVELOPMENT**⚠

Development is underway to:

* Connect the groups created in HDF5 by `CreateDataStructure.py` to the datasets created by `CreateDatasets.py` 

# XMLHDF5Parser

This Parser is designed to convert MTConnect XML data into an HDF5 structure, grouped by positional data items. It is not designed for a 1-to-1 converion.

# Requirements

The parser works with these requirements. If more recent versions of Python libraries do not work, try using the specified versions.

* Python 3.11 or 
* Python Libraries
  * [saxonche](https://pypi.org/project/saxonche/) version 12.1 or above (12.3 recommended)
  * [pathlib](https://pypi.org/project/pathlib/) version 1.0.1
  * [h5py](https://pypi.org/project/h5py/) version 3.9
  * [numpy](https://pypi.org/project/numpy/)
  * [pandas](https://pypi.org/project/pandas/)
  
The resulting HDF5 files may be viewed using software such as [HDFView](https://www.hdfgroup.org/downloads/hdfview/), developed by HDFGroup.

# Usage

Place a single or multiple raw MTConnect XML files into the `data` directory. Each raw XML file should have a unique `uuid` attribute values on the `DeviceStream` element.


Upon execution of `CreateDataStructure.py`, an output HDF5 file should appear in the `output` directory as`output.hdf5`.  
