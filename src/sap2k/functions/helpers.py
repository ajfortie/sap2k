
def result_setup(model, load_cases, Units=4, NLStatic=1, MSStatic=1,
                  MVCombo=1):
    """
    This function takes the specified output parameters and prepares the model
    for data extraction.
    """
    # Set Units
    model.SetPresentUnits(Units)

    # Set Result Options
    model.Results.Setup.SetOptionNLStatic(NLStatic)
    model.Results.Setup.SetOptionMultiStepStatic(MSStatic)
    model.Results.Setup.SetOptionMultiValuedCombo(MVCombo)

    # Set Load Cases For Output
    model.results.Setup.DeselectAllCasesAndCombosForOutput()
    for itm in load_cases:
        ret = model.Results.Setup.setCaseSelectedForOutput(itm)
        if ret != 0:
            ret = model.Results.Setup.setComboSelectedForOutput(itm)
