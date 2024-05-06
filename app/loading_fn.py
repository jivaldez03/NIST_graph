from app.db import common_dbfunc as dbexec
from app.db.database import targetdb
from app.db.crud.NIST_file import control, control_enhancement
from app.db.crud.NIST_file import category

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
    print("Adding Categories Detail")
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

        # slicing code_ref  (format: MA-3(1))
        code,ref = code_ref.split('-')  # [MA, 3(1)]
        reflist = ref.split('(')        # [3, 1)]
        ref,refpos = reflist[0], reflist[1] if len(reflist) > 1 else None  # 3, 1)
        refpos = int(refpos.replace(')','')) if refpos else 0               # 1
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
    query = control_enhancement.create_relatedcontrol_relationship
    dbexec.execute_write_query(targetdb, query)

def adding_rootnodes():
    print('Adding NIST nodes')
    query = category.create_root
    dbexec.execute_write_query(targetdb, query)
