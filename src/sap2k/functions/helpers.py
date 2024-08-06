from ..constants import units

def result_setup(model, load_cases=None, Units=4, NLStatic=1, MSStatic=1,
                  MVCombo=1):
    """
    This function takes the specified output parameters and prepares the model
    for data extraction.
    """
    # Set Units
    if isinstance(Units, str):
        Units = units[Units]
    elif isinstance(Units, int):
        Units = Units
    else:
        raise TypeError("Value of Units variable must be string or integer. \
Reference the Units.json file in the constants directory for list \
of valid units.")
    
    model.SetPresentUnits(Units)

    # Set Result Options
    model.Results.Setup.SetOptionNLStatic(NLStatic)
    model.Results.Setup.SetOptionMultiStepStatic(MSStatic)
    model.Results.Setup.SetOptionMultiValuedCombo(MVCombo)

    # Set Load Cases For Output
    if load_cases != None:
        ret=model.Results.Setup.DeselectAllCasesAndCombosForOutput()
        print("Flag for Case claring is {}".format(ret))
        for itm in load_cases:
            ret = model.Results.Setup.SetCaseSelectedForOutput(itm)
            if ret != 0:
                ret = model.Results.Setup.SetComboSelectedForOutput(itm)
    return ret

def select_groups(model,groups=list):

    ret = model.SelectObj.ClearSelection()
    for grp in groups:
        ret = model.SelectObj.Group(grp)
    
    return ret