"""
This module processes and reports on the steel design module in SAP 2000
"""
from ..functions.helpers import result_setup, select_groups

def StartDesign(model):
    #Are Design Results Available?
    design_status = model.DesignSteel.GetResultsAvailable()

    if design_status:
        return
    else:
        model.DesignSteel.StartDesign()
        model.File.Save()


def GetSummaryResults(model, groups=list|None, Units=4):
    
    # The names of each of the SAP2000 Output Parameters
    field_names = ["NumberItems", "FrameName", "Ratio", "RatioType",
                    "Location", "ComboName", "ErrorSummary",
                    "WarningSummary"]
    
    #Prepare the Model for Output
    result_setup(model,Units = Units)

    # Select elements in groups
    select_groups(model, groups)

    output = model.DesignSteel.GetSummaryResults("",ItemType=2)

    # Convert output into a dictionary
    output_dict = {}
    for i, fldnm in enumerate(field_names):
        output_dict[fldnm] = output[i]

    return output_dict
