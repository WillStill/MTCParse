import os
from saxonche import *
import numpy as np
import h5py

hf = h5py.File('output/output2.hdf5', 'w')

#Import XML as Text SaxonC can utilize

with PySaxonProcessor(license=False) as proc:
    print("Test SaxonC on Python")
    print(proc.version)

    xpathProc = proc.new_xpath_processor()

    #Find Files
    xmlFileList = []


    for file in os.listdir("data"):
        if file.endswith(".xml"):
            xmlFileList.append(f"data/{file}")
            # doc = open(f"data/{file}", encoding='utf-8').read()




    #Name spaces must be defined properly for xpath use
    # xpathProc.declare_namespace("","urn:mtconnect.org:MTConnectStreams:2.0")
    processDict = {}
    for xmlFileName in xmlFileList:
        print(xmlFileName)

        xdm_node = proc.parse_xml(xml_file_name=xmlFileName)
        xpathProc.set_context(xdm_item=xdm_node)
        xpathProc.declare_namespace('', xpathProc.evaluate_single('namespace-uri(/*)').string_value)

        # xpathProc.set_context(file_name=xmlFileName)


        #XPATH Queries


        deviceName = xpathProc.evaluate("//DeviceStream[not(@name = 'Agent')]/@name ! string()").__str__()
        hf_group = hf.create_group(deviceName)

        subArr = []

        for i in range(int(xpathProc.evaluate("(count(//Samples/*) + count(//Events/*))").__str__())):
            i += 1
            attributeDict = {}
            # print("I", i)

            #Elements
            processName = xpathProc.evaluate("(//Samples/* | //Events/*)[" + str(i) + "]/name()")  # (//Samples/* ! name())[i]
            processSequence = xpathProc.evaluate("(//Samples/*/@sequence | //Events/*/@sequence)[" + str(i) +"] ! string()")  # (//Samples/*/@sequence ! string())[i]
            processNameSeq = str(processName) + str(processSequence)

            attributeDict["Sequence"] = str(processSequence)
            attributeDict["Process"] = str(processName)

            # processText = xpathProc.evaluate("(//Samples/*/text())[1]") #(//Samples/*/text())[i]

            #Attributes
            processComponent = xpathProc.evaluate("(//Samples/* | //Events/*)[" + str(i) + "]/ancestor::ComponentStream/@component ! string()") #(//Samples/ancestor::ComponentStream/@component ! string())[i]
            attributeDict["Component"] = str(processComponent)
            processComponentName = xpathProc.evaluate("(//Samples/* | //Events/*)[" + str(i) + "]/ancestor::ComponentStream/@name  ! string()") #(//Samples/ancestor::ComponentStream/@name ! string())[i]
            attributeDict["ComponentName"] = str(processComponentName)
            #processCompName = str(processAttributeComponent) + str(processAttributeComponentName)

            processList = [processName, processSequence, processComponent, processComponentName]

            for x in range(int(xpathProc.evaluate("((//Samples/* | //Events/*)[" + str(i) + "]/@*[not(name() = 'sequence' )] => count())").__str__())):
                x += 1
                # print("X", x)

                AttributeName = xpathProc.evaluate("((//Samples/* | //Events/*)[" + str(i) + "]/@*[not(name() = 'sequence' )] ! name())[" + str(x) + "]") #(//Samples/*/@*[not(name() = 'sequence' )] ! name())[i]
                AttributeValue = xpathProc.evaluate("((//Samples/* | //Events/*)[" + str(i) + "]/@*[not(name() = 'sequence' )] ! string())[" + str(x) + "]") #(//Samples/*/@*[not(name() = 'sequence' )] ! string())[i]
                attributeDict[AttributeName] = str(AttributeValue)

                # processList.append(AttributeValue)
                # Get the AttributeName for the datasets HERE
                # print(processList)

            processText = xpathProc.evaluate("(//Samples/* | //Events/*)[" + str(i) + "]/text()")  # (//Samples/*/text())[i]
            attributeDict["Text"] = processText

            processDict[processNameSeq] = attributeDict

            # Append process information to the subArr list before it is made into a 2d array
            subArr.append(processList)

        # Make the subArr list 2 dimensional array
        print(subArr)
        arr2d = np.array([subArr])
        # print(arr2d)

        #Sort
        # Radix Sort might be a good addition for the future? That or Quicksort me thinks
        # Python sort() is using Timsort
        sorted_processDict = {k: processDict[k] for k in sorted(processDict, key=lambda k: int(processDict[k]['Sequence']))}
        # print(sorted_processDict)

        # for key in sorted_processDict:
        #     print(sorted_processDict[key]["Sequence"])
        # print(sorted_processDict, len(processDict))

        #HDF5

        #     hf = h5py.File('output/output2.hdf5', 'w')

# Get the quantity of process elements to record and attribute values
# Record the last dataset active
# Record the last 2d array

# A full data array is wanted for a dataset

# Check the name of each process.
# For each process that is found
# If the process matches what is wanted

# Create a dataset using the last 2d array of information
# Clear the 2d array of information

# Create an array using the shape of all processes.
# Find a method to assign values to processes. If no values are found then assign a NULL value.
# Record this array to be appended to the 2d array.

# If the process does not match what is wanted create an array using the shape of all processes
# Find a method to assign values to processes. If no values are found then assign a NULL value.
# With the 1 dimensional array created, pull the last array and append to it.

        for key in sorted_processDict:
            if sorted_processDict[key]["Process"] in ["Orientation", "Position"]:
                #print(key)
                obj = hf_group.create_dataset(key, shape=100, dtype=None, data=None)

            else:
                pass
                # obj.create_dataset(key)

# with h5py.File("output/output2.hdf5", "r") as h5file:
#     # Print all root level object names (aka keys)
#     # these can be group or dataset names
#     print("Keys: %s" % h5file.keys())
#     # get first object name/key; may or may NOT be a group
#     a_group_key = list(h5file[].keys())[0]
#
#     # get the object type for a_group_key: usually group or dataset
#     print(type(h5file[a_group_key]))
#
#     # If a_group_key is a group name,
#     # this gets the object names in the group and returns as a list
#     data = list(h5file[a_group_key])
#
#     # If a_group_key is a dataset name,
#     # this gets the dataset values and returns as a list
#     data = list(h5file[a_group_key])
#     # preferred methods to get dataset values:
#     # ds_obj = f[a_group_key]  # returns as a h5py dataset object
#     # ds_arr = f[a_group_key][()]  # returns as a numpy array

