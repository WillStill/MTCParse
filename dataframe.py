import os
from saxonche import PySaxonProcessor
from pathlib import Path

import xml.dom.minidom
import h5py
import numpy as np
import pandas as pd
from collections import OrderedDict

def getDictArray(child):

    DIData = {}

    # Data Name
    eleName = child.tagName + child.getAttribute('sequence')
    DIData["eleName"] = eleName

    # Data Value
    eleValue = child.firstChild.nodeValue
    DIData["eleValue"] = eleValue

    # DataSet Attributes Key and Value
    for key in child.attributes.keys():
        value = child.getAttribute(key)
        DIData[key] = value

    #print("DIDATA", DIData)
    return DIData

def dumpXML(node):  # def dumpXML(node, hdf_group):
    with h5py.File("output2.hdf5", "w") as hf:
        #print(node.firstChild.tagName)
        hdf_group = hf.create_group(node.firstChild.tagName)
        node = node.firstChild
        children = node.childNodes  # define children as child nodes of node
        #print("NODE", node.tagName)
        allArrays = []
        for child in children:  # for each child in children
            if child.nodeType == 1:  # if the child is an element type node
                array = getDictArray(child)
                print("dict", array)
                allArrays.append(array)

        #print("allArrays", allArrays)


        # Find all unique keys across all dictionaries
        allKeys = list(OrderedDict.fromkeys(sum((list(array.keys()) for array in allArrays), [])))
        #print("AllKeys",allKeys)

        # Make a datatype format
        df_dt = np.dtype({'names': allKeys, 'formats':['S80'] * len(allKeys)})
        #print("DF_DT", df_dt)



        data_dict = {key: [] for key in allKeys}
        #print("DATA DICT",data_dict)

        # Populate the data array with values from the dictionary
        for array in allArrays:
            for key in allKeys:
                data_dict[key].append(array.get(key, ''))
        #print(data_dict)

        # Convert structured array to a Pandas Dataframe
        df = pd.DataFrame(data_dict)
        # df = df.astype(str)
        #print(df)
        #print(df.dtypes)

        hdf_group.create_dataset("""TheOneAndOnly""", shape=df.shape, dtype="S80", data=df)

        #
        #
        # # use allKeys to define dtype for df
        #df_dt = [(key, 'S80') for key in allKeys]
        # print(df_dt)
        #
        # # Create dataframe
        # df = pd.json_normalize(allArrays)
        # #print(df)
        #
        # dt = df.convert_dtypes().dtypes
        # #print(dt)
        # # print(df.dtypes)
        # # print(df.convert_dtypes())
        # # #print("\n Updated \n", df.dtypes)
        #

        # Currently we are producing a dataframe in Pandas which works pretty well. Next step is to change column names
        # to match the keys in the dictionary. Then we need to fix the datatypes for the HDF5 file.

        #
        # print(dset)

        # https://stackoverflow.com/questions/58999029/how-do-you-name-the-columns-in-a-hdf5-data-set#:~:text=Regarding%20names%20for%20your%20columns,reference%20with%20the%20data%3D%20parameter.





# hf = h5py.File('output.hdf5', 'w')  # make hdf5 file
# g1 = hf.create_group("root") #make the root tag a group
acc_2 = np.random.random(500)  # TEMPORARY DATA

# FINDFILES
with PySaxonProcessor(license=False) as proc:
    print(proc.version)
    xsltproc = proc.new_xslt30_processor()
    source = "data"
    xslt = "DataXSLT.xsl"
    result = "output"
    fileName = str("data/" + next(os.walk("data"))[2][0])

    executable = xsltproc.compile_stylesheet(stylesheet_file=xslt)
    # With compile_stylesheet() we get a PyXSLTExecutable object and can do more with that using advanced Saxon features
    executable.set_initial_match_selection(file_name=fileName)
    # set a dummy file here, but it does have to be a well-formed XML document
    executable.apply_templates_returning_value(base_output_uri=Path('.', result, 'output').absolute().as_uri())
    # See examples at https://www.saxonica.com/saxon-c/documentation12/index.html#!samples/samples_python

    for file in os.listdir(result):
        if file.endswith(".xml"):
            # doc = open(f"{result}/{file}", encoding='utf-8').read()
            doc = xml.dom.minidom.parse("output/" + file)
            dumpXML(doc)


