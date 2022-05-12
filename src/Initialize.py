##SAP2000 Interface module.
import os

import sys

import comtypes.client

def SAPModel(Version, AttachToInstance = False):
    # This function will
    # Define the paths to different versions of SAP2000
    VersionPaths = ["",""]
    VersionPaths[0] = "C:\\Program Files\\Computers and Structures\\SAP2000 21\\SAP2000.exe"
    VersionPaths[1] = "C:\\Program Files\\Computers and Structures\\SAP2000 22\\SAP2000.exe"

    #Process Version Number
    if (Version == "V21") or (Version == "v21"):
        Prog_Path = VersionPaths[0]

    elif (Version =="V22") or (Version == "v22"):
        Prog_Path = VersionPaths[1]

    if AttachToInstance:

        #attach to a running instance of SAP2000

        try:

            #get the active SapObject

            mySapObject = comtypes.client.GetActiveObject("CSI.SAP2000.API.SapObject")

        except (OSError, comtypes.COMError):

            print("No running instance of the program found or failed to attach.")

            sys.exit(-1)

    else:

        #create API helper object

        helper = comtypes.client.CreateObject("SAP2000v1.Helper")

        helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)

        try:

            #'create an instance of the SAPObject from the specified path

            mySapObject = helper.CreateObject(Prog_Path)

        except (OSError, comtypes.COMError):

            print("Cannot start a new instance of the program from " + Prog_Path)

            sys.exit(-1)

        #start SAP2000 application

    return mySapObject

