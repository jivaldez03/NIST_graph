from neo4j import GraphDatabase

from app.db.config import settings_any

def driver_forneo4j(port):
    print(f"Connecting: {settings_any.db.get_database_uri_port(port)}")
    driver_neo4j = GraphDatabase.driver(
        settings_any.db.get_database_uri_port(port)
        #, auth=(settings_any.db.NEO4J_USERNAME, settings_any.db.NEO4J_PASSWORD)        
    )
    return driver_neo4j


def driver_close():
    targetdb.close()


port = input (f"port to connect Neo4j (7688): ")
if not port:
    port = '7688'

targetdb = driver_forneo4j(port)