from app.general_functions.common import _get_datetime, _get_sdatetime
from app.general_functions import pandas_fn as pd_fns
from app.db import common_dbfunc as dbexec
from app.db.crud.crud_security import category, categoryID_SUBID as control, relatedcontrol

from app.db.database import driver_forneo4j

print(_get_datetime())
print(_get_sdatetime())

port = input (f"port to connect Neo4j (7687): ")
if not port:
    port = '7687'

targetdb = driver_forneo4j(port)

print(f"Driver to db: {targetdb}")

def sendingDB_categories(df):
    print("Adding Categories")
    for index_df, row in df.iterrows():
        index = row['Ix']
        code = row['Unnamed: 1']
        name = row['Unnamed: 2']
        description = row['Unnamed: 3']
        print(index, code, name) #, description)
        query = category.create_category + \
                category.create_category_prop.format(properties=category.cat_properties_forupdate)

        dbexec.execute_write_query(targetdb, query
                                              , index = index
                                              , code = code
                                              , name = name
                                              , description = description.capitalize()
                                            )
    return

def sendingDB_controldef(df):
    print("Adding Categorie's Detail")
    queryCatRoot = control.create_detailcat + \
                    control.create_detailcat_prop.format(properties=control.detailcat_properties_forupdate) + \
                    control.create_detailcat_prop2
    queryCatLeaves = control.create_detailcat_pos + \
                    control.create_detailcat_pos_prop.format(properties=control.detailcat_properties_forupdate) + \
                    control.create_detailcat_pos_prop2   
        
    for index_df, row in df.iterrows():        
        code_ref = row["Control Identifier"]
        name = row["Control_Name"]
        text = row["Control Text"]
        discussion = row["Discussion"]
        controls = row["Related Controls"]

        # slicing code_ref 
        code,ref = code_ref.split('-') 
        reflist = ref.split('(') 
        ref,refpos = reflist[0], reflist[1] if len(reflist) > 1 else None
        refpos = int(refpos.replace(')','')) if refpos else 0
        print(index_df+1, code_ref, code, ref, refpos, controls, refpos)        
        
        if controls.lower() not in ['none','none.','', None]:
            ssubids = controls.replace(' ','').replace('.','').split(',')
            print(f"Related Controls: {ssubids}")
        else:
            ssubids = None
        
        if refpos == 0:    # root - P-10
            query = queryCatRoot
        else:
            query = queryCatLeaves

        dbexec.execute_write_query(targetdb, query
                                            , code = code
                                            , ref = int(ref)
                                            , refpos = refpos
                                            , name = name
                                            , text = text
                                            , discussion = discussion.capitalize()
                                            , controls = ssubids  #controls
                                            )
        
def adding_relatedcontrols():
    print('Adding related-control relationships')
    query = relatedcontrol.create_relatedcontrol_relationship
    dbexec.execute_write_query(targetdb, query)

def adding_rootnodes():
    print('Adding NIST nodes')
    query = category.create_root
    dbexec.execute_write_query(targetdb, query)

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
        sendingDB_categories(df)
    elif gia == 1: # categories' detail
        df = pd_fns._df_NaNbyAny(df, changeto='')
        df = pd_fns._df_renamecolumn(df, 'Control (or Control Enhancement) Name', 'Control_Name')
        sendingDB_controldef(df)

adding_relatedcontrols()
adding_rootnodes()

targetdb.close()
