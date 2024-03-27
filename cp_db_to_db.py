
from datetime import datetime as dt
from app.db.database import driver_forneo4j
from app.db.common_dbfunc import execute_read_query, execute_write_query

print(dt.now())
print(str(dt.now()).replace(' ', 'T'))

read_label_objects = """
 MATCH (n)
                RETURN distinct LABELS(n) AS LABEL
                ORDER BY LABEL
                """

read_nodes_objects = """
                MATCH (n:CLASS)
                RETURN n as NODE, elementId(n) as ELEID
                ORDER BY ELEID
                """
write_nodes_objects = """CREATE (n:CLASS)"""
write_nodes_objects_p2 = """
                set n += {{ {properties} }}
                    , n.eleID = $eleid
                return n
                """

read_relationships_nodes = """
                MATCH (n)-[r]->(m)
                return elementId(n) as eleSource,type(r) as relationshipname, elementId(m) as eleTarget
                """
write_relationships_nodes = """
                MATCH (s WHERE s.eleID = $eleSource)
                MATCH (t WHERE t.eleID = $eleTarget)
                MERGE (s)-[r:{relationshipname}]->(t)
                """

dbsource = driver_forneo4j(7689)
dbtarjet = driver_forneo4j(7688)


query = read_label_objects
labelsneo4j = execute_read_query(dbsource, query)
for gia, labels in enumerate(labelsneo4j):
    print(labels)
    for lab in labels['LABEL']:
        #print('lab->', lab)
        query = read_nodes_objects.replace('CLASS',lab)
        #print(query)
        nodes = execute_read_query(dbsource, query) #, id=eleObj, **fields)
        for node in nodes:
            #print('node->', node)
            properties = ', '.join('{0}: ${0}'.format(n) for n in node['NODE'] if n not in ['ctInsert','ctUpdate'])
            print('prop:', properties)

            query_w = write_nodes_objects.replace('CLASS',lab) + \
                        write_nodes_objects_p2.format(properties=properties)

            new_node = execute_write_query(dbtarjet, query_w, eleid=node['ELEID'], **node['NODE'])


query = read_relationships_nodes
relationsneo4j = execute_read_query(dbsource, query)

for gia, relation_recs in enumerate(relationsneo4j):
    print(relation_recs)

    # properties = ', '.join('{0}: ${0}'.format(n) for n in relation_recs if n not in ['ctInsert','ctUpdate'])

    query_w = write_relationships_nodes.format(relationshipname=relation_recs["relationshipname"])

    new_node = execute_write_query(dbtarjet, query_w, eleid=node['ELEID'], **relation_recs)