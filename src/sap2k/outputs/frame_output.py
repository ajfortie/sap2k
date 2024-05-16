## Frame Output Post-Processing Module
# This Module contains functions which extract frame results from a given
# SAP2000 Model

from asyncio.windows_events import NULL
from ..constants import units

import sys

def FrameJtForces(Model=object, LoadCases, Groups, Units=4, NLStatic=1, MSStatic=1, MVCombo=1):
    """This function will extract the Frame Joint Forces for the given load cases,
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

    if isinstance(Units, str):
        Units = units[Units]
    elif isinstance(Units, int):
        Units = Units
    else:
        raise TypeError("Value of Units variable must be string or integer. \
Reference the Units.json file in the constants directory for list \
of valid units.")

    ret=0
    NumberResults = 0
    Obj = []
    Elm = []
    PointElm =[]
    LoadCase = []
    StepType = []
    StepNum = []
    F1 = []
    F2 = []
    F3 = []
    M1 = []
    M2 = []
    M3 = []
    Xcoord = []
    Ycoord = []
    Zcoord = []
    Results = []
    FldNms = ['FieldNames','NumberResults','Obj','Elm','PointElm','LoadCase','StepType','StepNum',
              'F1','F2','F3','M1','M2','M3','Xcoord','Ycoord','Zcoord']

    # Set Units
    Model.SetPresentUnits(Units)

    # Set Result Options
    Model.Results.Setup.SetOptionNLStatic(NLStatic)
    Model.Results.Setup.SetOptionMultiStepStatic(MSStatic)
    Model.Results.Setup.SetOptionMultiValuedCombo(MVCombo)

    # Set Load Cases For Output
    Model.results.Setup.DeselectAllCasesAndCombosForOutput()
    for i, item in enumerate(LoadCases):
        ret = Model.Results.Setup.setCaseSelectedForOutput(item)
        if ret != 0:
            ret = Model.Results.Setup.setComboSelectedForOutput(item)

    # Select all objects in specified groups
    Model.SelectObj.Group("All",True)
    for i, item in enumerate(Groups):
        ret = Model.SelectObj.ClearSelection()
        ret = Model.SelectObj.Group(item)

        # Loop through each selection group

        [NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3,ret] = Model.Results.FrameJointForce("",3)

    for i in range(NumberResults):
        [X,Y,Z,T] = Model.PointElm.GetCoordCartesian(PointElm[i])
        Xcoord.append(X)
        Ycoord.append(Y)
        Zcoord.append(Z)

    return [FldNms,NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3,Xcoord,Ycoord,Zcoord]

def FrameForces(Model, LoadCases, Groups, Units=4, NLStatic=1, MSStatic=1, MVCombo=3):
    # This function will extract the Area Joint Forces for the given load cases,
    # and groups. output is a list of tuples of the resulting forces.

    # Variable Definitions:
    #   Model       = SAP Model object defined initialized using SAP2000v22 (Object)
    #   LoadCases   = List of load cases for inclusion in output (Strings)
    #   Groups      = List of selection groups for inclusion in output (Strings)
    #   Results     = List of result data extracted from the SAP2000 Model
    #       Results[0]  = Field Names
    #       Results[1]  = Number of Results
    #   NLStatic    = Set output type for Nonlinear Static Results:
    #       1   = Envelopes (Default)
    #       2   = Step-by-Step
    #       3   = Last Step
    #   MSStatic    = Set output type for Multi-Step Static Results:
    #       1   = Envelopes (Default)
    #       2   = Step-by-Step
    #       3   = Last Step
    #   MVCombo     = Set output type for Multi-Valued Combonations:
    #       1   = Envelope (Default)
    #       2   = Multiple Values, if possible
    #       3   = Correspondence
    #   Units       = Set output units for results
    #       1   = lb, in, F
    #       2   = lb, ft, F
    #       3   = kip, in, F
    #       4   = kip, ft, F (Default)
    #       5   = kN, mm, C
    #       6   = kN, m, C
    #       7   = kgf, mm, C
    #       8   = kgf, m, C
    #       9   = N, mm, C
    #       10  = N, m, C
    #       11  = Ton, mm, C
    #       12  = Ton, m, C
    #       13  = kN, cm, C
    #       14  = kgf, cm, C
    #       15  = N, cm, C
    #       16  = Ton, cm, C

    ret=0
    NumberResults = 0
    Obj = []
    ObjSta = []
    Elm = []
    ElmSta =[]
    LoadCase = []
    StepType = []
    StepNum = []
    P = []
    V2 = []
    V3 = []
    T = []
    M2 = []
    M3 = []
    Xcoord = []
    Ycoord = []
    Zcoord = []
    Results = []
    FldNms = ['FieldNames','NumberResults','Obj','ObjSta','Elm','ElmSta','LoadCase','StepType','StepNum',
              'P','V2','V3','T','M2','M3','Xcoord','Ycoord','Zcoord']

    # Set Units
    Model.SetPresentUnits(Units)

    # Set Result Options
    Model.Results.Setup.SetOptionNLStatic(NLStatic)
    Model.Results.Setup.SetOptionMultiStepStatic(MSStatic)
    Model.Results.Setup.SetOptionMultiValuedCombo(MVCombo)

    # Set Load Cases For Output
    Model.results.Setup.DeselectAllCasesAndCombosForOutput()
    for i, item in enumerate(LoadCases):
        ret = Model.Results.Setup.setCaseSelectedForOutput(item)
        if ret != 0:
            ret = Model.Results.Setup.setComboSelectedForOutput(item)

    # Select all objects in specified groups
    Model.SelectObj.Group("All",True)
    for i, item in enumerate(Groups):
        ret = Model.SelectObj.ClearSelection()
        ret = Model.SelectObj.Group(item)

        # Loop through each selection group

        [NumberResults,Obj,ObjSta,Elm,ElmSta,LoadCase,StepType,StepNum,P,V2,V3,T,M2,M3,ret] = Model.Results.FrameForce("",3)

    # for i in range(NumberResults):
    #     [X,Y,Z,Temp] = Model.PointElm.GetCoordCartesian(PointElm[i])
    #     Xcoord.append(X)
    #     Ycoord.append(Y)
    #     Zcoord.append(Z)

    return [FldNms,NumberResults,Obj,ObjSta,Elm,ElmSta,LoadCase,StepType,StepNum,P,V2,V3,T,M2,M3]

def FrameElmSort(Model,Groups):
    ret=0
    NumberResults = 0
    Obj = []
    Elm = []
    PointElm =[]
    LoadCase = []
    StepType = []
    StepNum = []
    F1 = []
    F2 = []
    F3 = []
    M1 = []
    M2 = []
    M3 = []
    Xcoord = []
    Ycoord = []
    Zcoord = []
    Results = []
    ElmJtChk = []
    FldNms = ['Obj','Elm','PointElm']
    Result = []


    # Select all objects in specified groups
    for i, item in enumerate(Groups):

        #Loop through each selection group
        [NumberResults,Obj,Elm,PointElm,LoadCase,StepType,StepNum,F1,F2,F3,M1,M2,M3,ret] = Model.Results.FrameJointForce(item,2)

        dElm = {}
        dPointElm = {}

        for i in range(NumberResults):
            dPointElm.setdefault(Elm[i],[]).append(PointElm[i])

        Unique = list(set(Elm))
        ctr = 0

        loc_Result = [[Unique[0],dPointElm[Unique[0]][0],dPointElm[Unique[0]][1]]]
        currkey = Unique[0]
        for j, jkey in enumerate(Unique):
            for k, kkey in enumerate(Unique):
                if (dPointElm[currkey][1] == dPointElm[kkey][0]) and (currkey != kkey):
                    loc_Result.append([kkey,dPointElm[kkey][0],dPointElm[kkey][1]])
                    currkey = kkey

                elif (loc_Result[0][1] == dPointElm[kkey][1]) and (currkey != kkey):
                    loc_Result.insert(0,[kkey,dPointElm[kkey][0],dPointElm[kkey][1]])
                    currkey = kkey


        Result.append(loc_Result)

    return Result

def Frame_Stress_Avg(RawResults):
    # This module will take an array of results and average the forces over
    # common area joints.

    FldNms = ['Joint','OutputCase','StepType','StepNum','Xcoord','Ycoord','Zcoord',
              'F1','F2','F3','M1','M2','M3']

    ret=0
    NumberResults = 0
    JtCaseStep_Chk = []
    Obj = []
    Elm = []
    PointElm =[]
    LoadCase = []
    StepType = []
    StepNum = []
    F1 = []
    F2 = []
    F3 = []
    M1 = []
    M2 = []
    M3 = []
    Xcoord = []
    Ycoord = []
    Zcoord = []

    # Assign Result Indicies
    for i, item in enumerate(RawResults[0]):
        match item:
            case 'NumberResults':
                NumberResults = RawResults[i]
            case 'Obj':
                Obj = list(RawResults[i])
            case 'Elm':
                Elm = list(RawResults[i])
            case 'PointElm':
                PointElm = list(RawResults[i])
            case 'LoadCase':
                LoadCase = list(RawResults[i])
            case 'StepType':
                StepType = list(RawResults[i])
            case 'StepNum':
                StepNum = list(RawResults[i])
            case 'F1':
                F1 = list(RawResults[i])
            case 'F2':
                F2 = list(RawResults[i])
            case 'F3':
                F3 = list(RawResults[i])
            case 'M1':
                M1 = list(RawResults[i])
            case 'M2':
                M2 = list(RawResults[i])
            case 'M3':
                M3 = list(RawResults[i])
            case 'Xcoord':
                Xcoord = list(RawResults[i])
            case 'Ycoord':
                Ycoord = list(RawResults[i])
            case 'Zcoord':
                Zcoord = list(RawResults[i])

    # Create list of unique Joints
    for i in range(NumberResults):
        JtCaseStep_Chk.append(str(PointElm[i])+str(LoadCase[i])+str(StepType[i])+str(StepNum[i]))

    #Define Dictionaries
    print("Assigning result arrays to Dictionaries...")
    dF1 = {}
    dF2 = {}
    dF3 = {}
    dM1 = {}
    dM2 = {}
    dM3 = {}
    dPointElm = dict(zip(JtCaseStep_Chk,PointElm))
    dLoadCase = dict(zip(JtCaseStep_Chk,LoadCase))
    dStepType = dict(zip(JtCaseStep_Chk,StepType))
    dStepNum = dict(zip(JtCaseStep_Chk,StepNum))
    dXcoord = dict(zip(JtCaseStep_Chk,Xcoord))
    dYcoord = dict(zip(JtCaseStep_Chk,Ycoord))
    dZcoord = dict(zip(JtCaseStep_Chk,Zcoord))

    # Assign Dictionaries
    for i in range(NumberResults):

        dF1.setdefault(JtCaseStep_Chk[i],[]).append(F1[i])
        dF2.setdefault(JtCaseStep_Chk[i],[]).append(F2[i])
        dF3.setdefault(JtCaseStep_Chk[i],[]).append(F3[i])
        dM1.setdefault(JtCaseStep_Chk[i],[]).append(M1[i])
        dM2.setdefault(JtCaseStep_Chk[i],[]).append(M2[i])
        dM3.setdefault(JtCaseStep_Chk[i],[]).append(M3[i])

    # Define the Unique Keys
    UniqueSets = list(set(JtCaseStep_Chk))

    R_Joint = []
    R_Case = []
    R_StepType = []
    R_StepNum = []
    R_F1 = []
    R_F2 = []
    R_F3 = []
    R_M1 = []
    R_M2 = []
    R_M3 = []
    R_Xcoord = []
    R_Ycoord = []
    R_Zcoord = []

    Prev_Chk = []

    for i, key in enumerate(UniqueSets):

        R_Joint.append(dPointElm[key])
        R_Case.append(dLoadCase[key])
        R_StepType.append(dStepType[key])
        R_StepNum.append(dStepNum[key])
        R_F1.append(sum(dF1[key])/len(dF1[key]))
        R_F2.append(sum(dF2[key])/len(dF2[key]))
        R_F3.append(sum(dF3[key])/len(dF3[key]))
        R_M1.append(sum(dM1[key])/len(dM1[key]))
        R_M2.append(sum(dM2[key])/len(dM2[key]))
        R_M3.append(sum(dM3[key])/len(dM3[key]))
        R_Xcoord.append(dXcoord[key])
        R_Ycoord.append(dYcoord[key])
        R_Zcoord.append(dZcoord[key])

        sys.stdout.write('\n')
        if i%1000 == 0:
            sys.stdout.write('\r')
            sys.stdout.write('{0} of {1} items processed | {2:.2%} Complete'.format(i,len(UniqueSets),i/len(UniqueSets)))
        elif i == len(UniqueSets)-1:
            sys.stdout.write('\r')
            sys.stdout.write('{0} of {1} items processed | {2:.2%} Complete'.format(i,len(UniqueSets),i/len(UniqueSets)))

    Results = [FldNms, R_Joint, R_Case, R_StepType, R_StepNum, R_Xcoord, R_Ycoord, R_Zcoord, R_F1, R_F2, R_F3, R_M1, R_M2, R_M3]

    return Results
