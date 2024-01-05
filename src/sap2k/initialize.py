##SAP2000 Interface module.
import os
import sys

import comtypes.client




def SAPModel(Version, AttachToInstance=False, Visible=True, Path=""):
    # This function will Find the installed versions of SAP
    installed_versions = {}
    for items in os.listdir("C:\\Program Files\\Computers and Structures\\"):
        if items.find("SAP2000") != -1:
            key = items.removeprefix("SAP2000 ")
            installed_versions[key] = items

    #Process Version Number
    if Version in installed_versions:
        Prog_Path = "C:\\Program Files\\Computers and Structures\\" + installed_versions[Version] + "\\SAP2000.exe"

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

            # Start Sap2000 Application
            mySapObject.applicationstart(Visible=Visible,FileName=Path)

        except (OSError, comtypes.COMError):

            print("Cannot start a new instance of the program from " + Prog_Path)

            sys.exit(-1)

        #start SAP2000 application


    return mySapObject

