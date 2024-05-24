
cat_properties_params = "index: $index, code: $code, name: $name, description: $description"
cat_properties_forupdate = "index: $index, name: $name, description: $description"

initializing_database = """
        MATCH (n)
        DETACH DELETE n
        """

create_category = """
                MERGE (C:Category {ID:$code})
                on create set C.ctInsert = datetime()
                on match set C.ctUpdate = datetime()
                """
create_category_prop = """set C += {{ {properties} }}
                return C
                """

create_root =   """
                MERGE (N:NIST {ID:'NIST'})
                on create set N.ctInsert = datetime()
                on match set N.ctUpdate = datetime()
                set N.name = 'NIST'
                WITH N
                MERGE (NP:NIST_Publication {ID:'NIST 800-53 R5'})
                on create set NP.ctInsert = datetime()
                on match set NP.ctUpdate = datetime()
                set NP.name = 'NIST Special Publication 800-53 release 5'
                WITH N,NP
                MERGE (N)-[R:PUBLICATION]->(NP)
                on create set R.ctInsert = datetime()
                on match set R.ctUpdate = datetime()
                WITH NP
                MATCH (C:Category)
                MERGE (C)<-[RCP:CATEGORY_PUB]-(NP)
                on create set RCP.ctInsert = datetime()
                on match set RCP.ctUpdate = datetime()
                RETURN C,NP
                """

