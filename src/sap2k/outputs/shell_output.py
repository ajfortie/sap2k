## Processing of Shell Element Output
# This module performs various processing tasks on the output generated by SAP 2000

from ..constants import units, sap_paths
from ..functions.helpers import select_groups, result_setup
from pandas import DataFrame, merge
import math
import sys

def W_A_Eq(M11, M22, M12, alpha=90):
    # This function will combine the reported twisting moments (Mxy) with the
    # moments reported in the direction of the prinicpal reinforcement (Mx & My)

    # Variable Definitions:
    #   M11     = Moments in the 1-1 direction (kip-ft)
    #   M22     = Moments in the 2-2 direction (kip-ft)
    #   M12     = Twisting moment (kip-ft)
    #  [alpha]  = Angle to secondary axis measured CW from x-dir (Degrees)
    #   Mx_pos  = Combined Positive Moment in x-dir (kip-ft)
    #   Ma_pos  = Combined Positive Moment in α-dir (kip-ft)
    #   Mx_neg  = Combined Negative Moment in x-dir (kip-ft)
    #   Ma_neg  = Combined Negative Moment in α-dir (kip-ft)

    # Initialize Results List
    result = list(range(4))

    alpha = math.radians(alpha)     # Convert to Radians

    # Calculation of Positive Moment Demand
    Mx_pos = M11 + 2 * M12 * (1/math.tan(alpha)) + M22 * (1/math.tan(alpha)**2) + abs((M12 + M22 / math.tan(alpha)) / math.sin(alpha))
    Ma_pos = (M22 / math.sin(alpha)**2) + abs((M12 + M22 / math.tan(alpha)) / math.sin(alpha))

    if Mx_pos < 0:
        Mx_pos = 0
        Ma_pos = (M22 + abs((M12 + M22 / (math.tan(alpha))**2) / (M11 + 2 * M12 / math.tan(alpha) + M22 / (math.tan(alpha)**2)))) / (math.sin(alpha)**2)

    elif Ma_pos < 0:
        Ma_pos = 0
        Mx_pos = (M11 + 2 * M12 / math.tan(alpha) + M22 / (math.tan(alpha)**2)) + abs((M12 + M22 / (math.tan(alpha)))**2 / M22)

    if (Mx_pos <= 0) and (Ma_pos <= 0):
        Ma_pos = 0
        Mx_pos = 0

    Mx_neg = M11 + 2 * M12 * (1/math.tan(alpha)) + M22 * (1/math.tan(alpha)**2) - abs((M12 + M22 / math.tan(alpha)) / math.sin(alpha))
    Ma_neg = (M22 / math.sin(alpha)**2) - abs((M12 + M22 / math.tan(alpha)) / math.sin(alpha))

    if Mx_neg > 0:
        Mx_neg = 0
        Ma_neg = (M22 - abs((M12 + M22 / (math.tan(alpha))**2) / (M11 + 2 * M12 / math.tan(alpha) + M22 / (math.tan(alpha)**2)))) / (math.sin(alpha)**2)

    elif Ma_neg > 0:
        Ma_neg = 0
        Mx_neg = (M11 + 2 * M12 / math.tan(alpha) + M22 / (math.tan(alpha)**2)) - abs((M12 + M22 / (math.tan(alpha)))**2 / M22)

    if (Mx_neg >= 0) and (Ma_neg >= 0):
        Ma_neg = 0
        Mx_neg = 0

    result[0] = Mx_pos
    result[1] = Ma_pos
    result[2] = Mx_neg
    result[3] = Ma_neg

    return result
units
def AreaForceShell(model, LoadCases, Groups, Units=4, NLStatic=1, MSStatic=1, MVCombo=1):
    """This function will extract the Area shell Forces at each node for the given load cases,
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
          16  = Ton, cm, C
          """
    
    FldNms = ['NumberResults','Obj','Elm','PointElm','LoadCase','StepType','StepNum',
              'F11','F22','F12','FMax','FMin','FAngle','FVM',
              'M11','M22','M12','MMax','MMin','MAngle',
              'V13','V23','VMax','VAngle','ret']
    
    ret = result_setup(model=model,load_cases=LoadCases,Units=Units,
                       NLStatic=NLStatic,MSStatic=MSStatic,MVCombo=MVCombo)

    # Select all objects in specified groups
    ret = select_groups(model=model,groups=Groups)
    
    output = model.Results.AreaForceShell("",3)
    output_dict = {}

    for i, fldnm in enumerate(FldNms):
        output_dict[fldnm] = output[i]
    return output_dict

def Shell_Stress_Avg(rawResults,grp_by,data_val):
    df_averaged = rawResults.groupby(grp_by)[[data_val]].mean().reset_indx()
    df_averaged = merge(df_averaged,rawResults[["PointElm",
                                                         "Elm"]],on="PointElm")

    return df_averaged

def Shell_Stress_Avg_old(RawResults):
    # This module will take an array of results and average the forces over
    # common area joints.

    FldNms = ['Joint','OutputCase','StepType','StepNum','Xcoord','Ycoord','Zcoord',
              'F11','F22','F12','V13','V23','M11','M22','M12','M11Pos','M11Neg','M22Pos','M22Neg']

    ret=0
    NumberResults = 0
    JtCaseStep_Chk = []
    Obj = []
    Elm = []
    PointElm =[]
    LoadCase = []
    StepType = []
    StepNum = []
    F11 = []
    F22 = []
    F12 = []
    FMax = []
    FMin = []
    FAngle = []
    FVM = []
    M11 = []
    M22 = []
    M12 = []
    MMax = []
    MMin = []
    MAngle = []
    V13 = []
    V23 = []
    VMax = []
    VAngle = []
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
            case 'F11':
                F11 = list(RawResults[i])
            case 'F22':
                F22 = list(RawResults[i])
            case 'F12':
                F12 = list(RawResults[i])
            case 'FMax':
                FMax = list(RawResults[i])
            case 'FMin':
                FMin = list(RawResults[i])
            case 'FVM':
                FVM = list(RawResults[i])
            case 'M11':
                M11 = list(RawResults[i])
            case 'M22':
                M22 = list(RawResults[i])
            case 'M12':
                M12 = list(RawResults[i])
            case 'MMax':
                MMax = list(RawResults[i])
            case 'MMin':
                MMin = list(RawResults[i])
            case 'MAngle':
                MAngle = list(RawResults[i])
            case 'V13':
                V13 = list(RawResults[i])
            case 'V23':
                V23 = list(RawResults[i])
            case 'VMax':
                VMax = list(RawResults[i])
            case 'VAngle':
                VAngle = list(RawResults[i])
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
    dF11 = {}
    dF22 = {}
    dF12 = {}
    dM11 = {}
    dM22 = {}
    dM12 = {}
    dV13 = {}
    dV23 = {}
    dPointElm = dict(zip(JtCaseStep_Chk,PointElm))
    dLoadCase = dict(zip(JtCaseStep_Chk,LoadCase))
    dStepType = dict(zip(JtCaseStep_Chk,StepType))
    dStepNum = dict(zip(JtCaseStep_Chk,StepNum))
    dXcoord = dict(zip(JtCaseStep_Chk,Xcoord))
    dYcoord = dict(zip(JtCaseStep_Chk,Ycoord))
    dZcoord = dict(zip(JtCaseStep_Chk,Zcoord))

    # Assign Dictionaries
    for i in range(NumberResults):

        dF11.setdefault(JtCaseStep_Chk[i],[]).append(F11[i])
        dF22.setdefault(JtCaseStep_Chk[i],[]).append(F22[i])
        dF12.setdefault(JtCaseStep_Chk[i],[]).append(F12[i])
        dM11.setdefault(JtCaseStep_Chk[i],[]).append(M11[i])
        dM22.setdefault(JtCaseStep_Chk[i],[]).append(M22[i])
        dM12.setdefault(JtCaseStep_Chk[i],[]).append(M12[i])
        dV13.setdefault(JtCaseStep_Chk[i],[]).append(V13[i])
        dV23.setdefault(JtCaseStep_Chk[i],[]).append(V23[i])

    # Define the Unique Keys
    UniqueSets = list(set(JtCaseStep_Chk))

    R_Joint = []
    R_Case = []
    R_StepType = []
    R_StepNum = []
    R_F11 = []
    R_F22 = []
    R_F12 = []
    R_M11 = []
    R_M11Pos = []
    R_M11Neg = []
    R_M22 = []
    R_M22Pos = []
    R_M22Neg = []
    R_M12 = []
    R_V13 = []
    R_V23 = []
    R_Xcoord = []
    R_Ycoord = []
    R_Zcoord = []

    Prev_Chk = []

    for i, key in enumerate(UniqueSets):

        R_Joint.append(dPointElm[key])
        R_Case.append(dLoadCase[key])
        R_StepType.append(dStepType[key])
        R_StepNum.append(dStepNum[key])
        R_F11.append(sum(dF11[key])/len(dF11[key]))
        R_F22.append(sum(dF22[key])/len(dF22[key]))
        R_F12.append(sum(dF12[key])/len(dF12[key]))
        R_M11.append(sum(dM11[key])/len(dM11[key]))
        R_M22.append(sum(dM22[key])/len(dM22[key]))
        R_M12.append(sum(dM12[key])/len(dM12[key]))
        R_V13.append(sum(dV13[key])/len(dV13[key]))
        R_V23.append(sum(dV23[key])/len(dV23[key]))
        R_Xcoord.append(dXcoord[key])
        R_Ycoord.append(dYcoord[key])
        R_Zcoord.append(dZcoord[key])

        if R_M11[i] > 0:
            R_M11Pos.append(R_M11[i] + abs(R_M12[i]))
            R_M11Neg.append(0)
        else:
            R_M11Neg.append(R_M11[i] - abs(R_M12[i]))
            R_M11Pos.append(0)

        if R_M22[i] > 0:
            R_M22Pos.append(R_M22[i] + abs(R_M12[i]))
            R_M22Neg.append(0)
        else:
            R_M22Neg.append(R_M22[i] - abs(R_M12[i]))
            R_M22Pos.append(0)
        Prev_Chk.append(item)


        if i%1000 == 0:
            sys.stdout.write('\r')
            sys.stdout.write('{0} of {1} items processed | {2:.2%} Complete'.format(i,len(UniqueSets),i/len(UniqueSets)))
        elif i == len(UniqueSets)-1:
            sys.stdout.write('\r')
            sys.stdout.write('{0} of {1} items processed | {2:.2%} Complete'.format(i,len(UniqueSets),i/len(UniqueSets)))

    Results = [FldNms, R_Joint, R_Case, R_StepType, R_StepNum, R_Xcoord, R_Ycoord, R_Zcoord, R_F11, R_F22, R_F12, R_V13, R_V23, R_M11, R_M22, R_M12, R_M11Pos, R_M11Neg, R_M22Pos, R_M22Neg]

    return Results
