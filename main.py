#from datetime import datetime as dt
from app.general_functions.common import _get_datetime, _get_sdatetime
from app.general_functions import pandas_fn as pd_fns
from app.db import common_dbfunc as dbexec
from app.db.crud.crud_security import category, control

from app.db.database import driver_forneo4j

import numpy as np

print(_get_datetime())
print(_get_sdatetime())

port = input (f"port to connect Neo4j (7687): ")
if not port:
    port = '7687'

targetdb = driver_forneo4j(port)

print(f"Driver to db: {targetdb}")

def sendingDB_categories(df):
    cols = list(df.columns)
    print(f"xlsx file COLUMNS: {cols}")
    for index_df, row in df.iterrows():
        #print(index_df, row['Unnamed: 1'], row['Unnamed: 2'], row['Unnamed: 3'])
        index = row['Ix']
        code = row['Unnamed: 1']
        name = row['Unnamed: 2']
        description = row['Unnamed: 3']
        print(index, code, name) #, description)
        query = category.create_category + \
                category.create_category_prop.format(properties=category.cat_properties_forupdate)
        #print("query: ", query)

        new_node = dbexec.execute_write_query(targetdb, query
                                              , index = index
                                              , code = code
                                              , name = name
                                              , description = description.capitalize()
                                            )# eleid=node['ELEID'], **node['NODE'])

        #print(f"New node: {new_node}\n\n")
    return


def sendingDB_controldef(df, POS:int):
    cols = list(df.columns) # COLUMNS: ['Control Identifier', 'Control_Name', 'Control Text', 'Discussion', 'Related Controls']
    print(f"xlsx file COLUMNS: {cols}")
    recs = 0

    if POS == 0:
        query = control.create_detailcat + \
                control.create_detailcat_prop.format(properties=control.detailcat_properties_forupdate) + \
                control.create_detailcat_prop2
    else:
        query = control.create_detailcat_pos + \
                control.create_detailcat_pos_prop.format(properties=control.detailcat_properties_forupdate) + \
                control.create_detailcat_pos_prop2

    query_relatedcontrols = control.create_detailcat_ref  # relationship between CatDetail->CatDetail
    query_relatedcontrols_pos = control.create_detailcat_pos_ref  # relationship between CatDetailPos->CatDetail
    #print(query)
        
    for index_df, row in df.iterrows():
        #print(index_df, row)
        if index_df > 2:
            pass #break
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
        print(index_df, code_ref, code, ref, refpos, controls)

        if (POS == 0 and refpos == 0) or \
            (POS == 1 and refpos > 0):
                recs = recs + 1

                new_node = dbexec.execute_write_query(targetdb, query
                                                    , code = code
                                                    , ref = int(ref)
                                                    , refpos = refpos
                                                    , name = name
                                                    , text = text
                                                    , discussion = discussion.capitalize()
                                                    , controls = controls
                                                    )
                # slicing controls SC-8, SC-12, SC-13.                
                if controls.lower() not in ['none','none.','', None]:
                    ssubids = controls.replace(' ','').replace('.','').split(',')
                    print(f"Related Controls: {ssubids}")
                    if POS == 1:
                        for gia, ssubid in enumerate(ssubids):
                            coderef, subid = ssubid.split('-') 
                            #print(coderef, subid)
                            #print('query RELATEDCONTROLS: ', query_relatedcontrols)
                            new_node = dbexec.execute_write_query(targetdb, query_relatedcontrols_pos
                                                                , code = code
                                                                , ref = int(ref)
                                                                , refpos = refpos
                                                                , code_ref = coderef
                                                                , ref_ref = int(subid)
                                                                )
                    else:
                        for gia, ssubid in enumerate(ssubids):
                            coderef, subid = ssubid.split('-') 
                            #print(coderef, subid)
                            #print('query RELATEDCONTROLS: ', query_relatedcontrols)
                            new_node = dbexec.execute_write_query(targetdb, query_relatedcontrols
                                                                , code = code
                                                                , ref = int(ref)
                                                                , refpos = refpos
                                                                , code_ref = coderef
                                                                , ref_ref = int(subid)
                                                                )


    print("registros totales:", recs)
    return

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
        #COLUMNS: ['Control Identifier', 'Control (or Control Enhancement) Name', 'Control Text', 'Discussion', 'Related Controls']
        #df = pd_fns._df_removerows_nulls(df,cols)
        df = pd_fns._df_NaNbyAny(df, changeto='')
        df = pd_fns._df_renamecolumn(df, 'Control (or Control Enhancement) Name', 'Control_Name')
        sendingDB_controldef(df,POS=0)
        sendingDB_controldef(df,POS=1)
    #print("\n\n", df)
        
query = category.create_root

dbexec.execute_write_query(targetdb, query)


targetdb.close()
