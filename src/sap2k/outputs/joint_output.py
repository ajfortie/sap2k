## Frame Output Post-Processing Module
# This Module contains functions which extract joint results from a given
# SAP2000 Model

from asyncio.windows_events import NULL
from ..constants import units
from ..functions.helpers import result_setup

import pandas as pd
import sys

def JointReact(Model, LoadCases, Groups, Units=4, NLStatic=1, MSStatic=1, MVCombo=1):
    """This function will extract the Joint Reactions for the given load cases,
    and groups.

    Variable Definitions:
      Model       = SAP Model object defined initialized using SAP2000v22 (Object)
      LoadCases   = List of load cases for inclusion in output (Strings)
      Groups      = List of selection groups for inclusion in output (Strings)
      Results     = List of result data extracted from the SAP2000 Model
          Results[0]  = Field Names
          Results[1]  = Number of Results
      NLStatic    = Set output type for Nonlinear Static Results:
          1   = Envelopes (Default)
          2   = Step-by-Step
          3   = Last Step
      MSStatic    = Set output type for Multi-Step Static Results:
          1   = Envelopes (Default)
          2   = Step-by-Step
          3   = Last Step
      MVCombo     = Set output type for Multi-Valued Combonations:
          1   = Envelope (Default)
          2   = Correspondence
          3   = Multiple Values, if possible
      Units       = Set output units for results
          1   = lb, in, F
          2   = lb, ft, F
          3   = kip, in, F
          4   = kip, ft, F (Default)
          5   = kN, mm, C
          6   = kN, m, C
          7   = kgf, mm, C
          8   = kgf, m, C
          9   = N, mm, C
          10  = N, m, C
          11  = Ton, mm, C
          12  = Ton, m, C
          13  = kN, cm, C
          14  = kgf, cm, C
          15  = N, cm, C
          16  = Ton, cm, C """

    FldNms = ['NumberResults','Obj', 'Elm', 'LoadCase','StepType','StepNum', 'F1','F2','F3',
              'M1','M2','M3']
    
    if isinstance(Units, str):
        Units = units[Units]
    elif isinstance(Units, int):
        Units = Units
    else:
        raise TypeError("Value of Units variable must be string or integer. \
Reference the Units.json file in the constants directory for list \
of valid units.")
    
    result_setup(Model, LoadCases, Units, NLStatic, MSStatic, MVCombo)

    ret = Model.SelectObj.ClearSelection()
    for grp in Groups:
        ret = Model.SelectObj.Group(grp)
    
    output = Model.Results.JointReact("",3)
    output_dict = {}

    for i, fldnm in enumerate(FldNms):
        output_dict[fldnm] = output[i]

    return output_dict