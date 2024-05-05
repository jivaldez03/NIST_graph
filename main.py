from app.general_functions import pandas_fn as pd_fns
from app.db.database import driver_forneo4j
import app.loading_fn as loadf 

port = input (f"port to connect Neo4j (7687): ")
if not port:
    port = '7687'

targetdb = driver_forneo4j(port)

# MAIN SECTION
pdxls = pd_fns._read_file('files/Combined sp800-53r5-control-catalog.xlsx') 
print("sheets: ", pdxls.keys())
for gia, sheet in enumerate(list(pdxls.keys())[0:]):
    print(f"\nsheet: {sheet}")
    df = pdxls[sheet]
    cols = list(df.columns)
    if gia == 0: # categories
        df = pd_fns._df_removerows_nulls(df,cols)
        df = pd_fns._df_NaNbyAny(df, changeto='')
        df = pd_fns._df_renamecolumn(df, 'NIST Special Publication 800-53 (SP 800-53)', 'Ix')
        df = pd_fns._df_changetype(df, 'Ix', 'int')
        loadf.sendingDB_categories(targetdb, df)
    elif gia == 1: # categories' detail
        df = pd_fns._df_NaNbyAny(df, changeto='')
        df = pd_fns._df_renamecolumn(df, 'Control (or Control Enhancement) Name', 'Control_Name')
        loadf.sendingDB_controldef(targetdb, df)

loadf.adding_relatedcontrols(targetdb)
loadf.adding_rootnodes(targetdb)

targetdb.close()
