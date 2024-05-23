import comtypes.client

helper = comtypes.client.CreateObject("SAP2000v1.Helper")
helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)