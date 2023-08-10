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


def dataSetCreation(hdf_group, children, dset):
    allArrays = []
    for child in children:  # for each child in children
        if child.nodeType == 1:  # if the child is an element type node
            if child.tagName == "Orientation" or child.tagName == "Position":

                posName = str(child.tagName + child.getAttribute('sequence'))
                print(posName)
                dset = hdf_group.create_dataset(posName, dtype="S80")  # shape=df.shape, dtype="S80", data=df

                # children.pop(0)
                dataSetCreation(hdf_group, children, dset)

                for key in child.attributes.keys():
                    value = child.getAttribute(key)
                    hdf_group[posName].attrs[key] = value

                allArrays = []
            else:

                #Need to rework the dset to function well. Currently it is using pandas for the dataset, but I have to make my own numpy array to be able to add to the data.

                array = getDictArray(child)
                allArrays.append(array)
                print(allArrays)

                # Find all unique keys across all dictionaries
                allKeys = list(OrderedDict.fromkeys(sum((list(array.keys()) for array in allArrays), [])))

                # # Make a datatype format
                # df_dt = np.dtype({'names': allKeys, 'formats': ['S80'] * len(allKeys)})

                # Make Empty Array Shape
                data_dict = {key: [] for key in allKeys}

                # Populate the data array with values from the dictionary
                for array in allArrays:
                    for key in allKeys:
                        data_dict[key].append(array.get(key, ''))
                print(data_dict)

                # Convert structured array to a Pandas Dataframe
                df = pd.DataFrame(data_dict)

                dset.resize(dset.shape[0] + 1, axis=0)
                dset[:] = df
                # hdf_group.create_dataset("""TheOneAndOnly""", shape=df.shape, dtype="S80", data=df)

                # allKeys = list(OrderedDict.fromkeys(sum((list(array.keys()) for array in allArrays), [])))
                # data_dict = {key: [] for key in allKeys}

                #
                # array = getDictArray(child)
                # allArrays.append(array)
                # posName = str(child.tagName + child.getAttribute('sequence'))
                # # hdf_group.create_dataset(posName, shape=df.shape, dtype="S80", data=df)
                #
                #
                #
                # allKeys = list(OrderedDict.fromkeys(sum((list(array.keys()) for array in allArrays), [])))
                # data_dict = {key: [] for key in allKeys}
                #
                # for array in allArrays:
                #     for key in allKeys:
                #         data_dict[key].append(array.get(key, ''))
                #
                #         df = pd.DataFrame(data_dict)
                #         hdf_group.create_dataset(posName, shape=df.shape, dtype="S80", data=df)

        # # Attributes
        # for key in child.attributes.keys():
        #     hdf_group[posName].attrs[key] = value

        # # DataSet
        #             for key in child.attributes.keys():
        #                 value = child.getAttribute(key)
        #                 #print(posName, key, value)
        #
        #                 array = getDictArray(child)
        #                 allArrays.append(array)
        #
        #                 allKeys = list(OrderedDict.fromkeys(sum((list(array.keys()) for array in allArrays), [])))
        #                 data_dict = {key: [] for key in allKeys}
        #                 for array in allArrays:
        #                     for key in allKeys:
        #                         data_dict[key].append(array.get(key, ''))
        #
        #                 df = pd.DataFrame(data_dict)
        #             print(posName, df.shape, df)
        #             hdf_group.create_dataset(posName, shape=df.shape, dtype="S80", data=df)
        #
        #             # # Attributes
        #             # for key in child.attributes.keys():
        #             #     hdf_group[posName].attrs[key] = value

        # node = node.firstChild
        # children = node.childNodes  # define children as child nodes of node
        # # print("NODE", node.tagName)
        # allArrays = []
        # for child in children:  # for each child in children
        #     if child.nodeType == 1:  # if the child is an element type node
        #         array = getDictArray(child)
        #         allArrays.append(array)
        #
        #         allKeys = list(OrderedDict.fromkeys(sum((list(array.keys()) for array in allArrays), [])))
        #         data_dict = {key: [] for key in allKeys}
        #         for array in allArrays:
        #             for key in allKeys:
        #                 data_dict[key].append(array.get(key, ''))
        #
        #         df = pd.DataFrame(data_dict)
        #         hdf_group.create_dataset(posName, shape=df.shape, dtype="S80", data=df)
        #     else:
        #         for key in child.attributes.keys():
        #             value = child.getAttribute(key)
        #             # print(posName, key, value)


def dumpXML(node, hf):  # def dumpXML(node, hdf_group):
    node = node.firstChild
    children = node.childNodes  # define children as child nodes of node
    hdf_group = hf.create_group(node.tagName)

    dataSetCreation(hdf_group, children, "")


    # get all information
    # put all information into a 1 dimension array
    # Add information to dataset

    # elif node.childNodes.length != 0 and child.getAttribute(
    # 		"sequence") == "":  # if node is not a leaf node and child is not a data item
    # 	ctname = child.tagName  # get the child.tagName
    # 	caname = child.getAttribute("name")  # get the child attribute "name"
    # 	path = str(
    # 		ctname + "_" + caname)  # path = str(child.tagName + 'some delimiter that is not valid xml tag name' + child.attribute("name"))
    # 	new_group = hdf_group.create_group(path)  # new_group = hdf_group.createGroup(path)
    # 	dumpXML(child, new_group)  # dumpXML(child, new_group)

hf = h5py.File('output/output.hdf5', 'w')  # make hdf5 file

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
            dumpXML(doc, hf)