
detailcat_properties_params = "ID: $code, SUBID: $ref, POS: $refpos name: $name, text: $text, " +  \
                                "discussion: $discussion, controls: $controls"
detailcat_properties_forupdate = "name: $name, text: $text, discussion: $discussion, controls: $controls"


# crear node de Detail y su relación con Category
create_detailcat = """
                MERGE (D:CategoryDet {ID:$code, SUBID: $ref})
                on create set D.ctInsert = datetime()
                on match set D.ctUpdate = datetime()
                """
create_detailcat_prop = """set D += {{ {properties} }}"""
create_detailcat_prop2 = """
                        WITH D
                        MATCH (C:Category {ID:$code})
                        MERGE (D)-[R:DETAILCAT]->(C)
                        on create set R.ctInsert = datetime()
                        on match set R.ctUpdate = datetime()
                        return D 
                        """
# crear node de DetailPos y su relación con Detail
create_detailcat_pos = """
                MERGE (DP:CategoryDetPos {ID:$code, SUBID: $ref, POS: $refpos})
                on create set DP.ctInsert = datetime()
                on match set DP.ctUpdate = datetime()
                """
create_detailcat_pos_prop = """set DP += {{ {properties} }}"""
create_detailcat_pos_prop2 = """
                        WITH DP
                        MATCH (D:CategoryDet {ID:$code, SUBID:$ref})
                        MERGE (DP)-[R:DETAILCATPOS]->(D)
                        on create set R.ctInsert = datetime()
                        on match set R.ctUpdate = datetime()
                        return D 
                        """
