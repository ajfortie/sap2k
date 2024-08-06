from .. import initialize as sap_init
from ..outputs.shell_output import AreaForceShell
from ..functions.helpers import result_setup
import pandas as pd


model_paths = [r"C:\Users\afortier\OneDrive - Moffatt & Nichol\Temp Print\01-By Project\HI - 11173-01 - B20 & B21\Mod 4 Set\SAP Models\B20 POF Model\B20 Model_AF.sdb"]

# Define Groups
grp_frames = ["Drilled Shafts",
              "Pile Cap A",
              "Pile Cap B"]

grp_areas = ["Wharf Deck",
             "Cut-off Wall"]

grp_nodes = ["Pile Heads",
             "Pile Tip Joint"]

#Initialize SAP Instance
sap_instance = sap_init.SAPModel(Version='24', Visible=True, AttachToInstance=False)

df_deck_demands = pd.DataFrame()
df_base_reactions = pd.DataFrame()
df_reactions = pd.DataFrame()
df_design_summary = pd.DataFrame()

def FindCoords(pt_elm):
    x_cart, y_cart, z_cart, ret = model.PointElm.GetCoordCartesian()
    return [x_cart,y_cart,z_cart]

for path in model_paths:
    model = sap_instance.SAPModel
    model.File.OpenFile(path)
    model_name = model.GetModelFileName(False)
    print(model_name)

    num_res, load_combinations, ret = model.RespCombo.GetNameList()
    print(num_res)
    print(load_combinations)
    df = pd.DataFrame()
    load_combinations = [load_combinations[0],load_combinations[1]]
    # loop through combinations
    for comb in load_combinations:
        df_loc = pd.DataFrame(AreaForceShell(model, comb, grp_areas))
        df_averages = df_loc.groupby(by=['PointElm','LoadCase'])[['F11','F22','F12','V13','V23','M11','M22','M12']].mean().reset_index()
        #df_averages[['x_coord','y_coord','z_coord']] = df_averages['PointElm'].apply(FindCoords)
    model.File.Save()