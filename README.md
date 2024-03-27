# NIST_graph

# INSTALL AND LOAD XLSX FILE

# docker
1. sudo docker run -d --publish=7474:7474 --publish=7687:7687 --env=NEO4J_AUTH=none --volume=/home/__your-user__/dockerback/dock_NIST/data:/data neo4j

# loading NIST file
2. python3 main.py

# exploring graph database
http://0.0.0.0:7474/browser/   or http://localhost:7474/browser/


# review complete schema - Neo4j Command: 
call db.schema.visualization()

# reviewing Configuration Management (CM): 
match (c:Category {ID:'CM'})-[rd:DETAILCAT]-(cd:CategoryDet)
        -[rp:DETAILCATPOS]-(cdp:CategoryDetPos)
optional match (cdp)-[rcp:RELATEDCONTROL]-(cd2:CategoryDet)
return c, rd, cd, rp, cdp, rcp, cd2


# Categories
ID	    Name 	                                    Elements
"AC"	"Access Control"	                            25
"AT"	"Awareness and Training "	                     6
"AU"	"Audit and Accountability"	                    16
"CA"	"Security Assessment and Authorization "	    9
"CM"	"Configuration Management"	                    14
"CP"	"Contingency Planning"	                        13
"IA"	"Identification and Authentication"	            12
"IP"	"Information Processing"	                    0
"IR"	"Incident Response"	                            10
"MA"	"Maintenance"	                                7
"MP"	"Media Protection"	                            8
"PE"	"Physical and Environmental Protection "	    23
"PL"	"Planning"	                                    11
"PM"	"Program Management"	                        32
"PS"	"Personnel Security"	                        9
"PT"	"Personally Identifiable"	                    8
"RA"	"Vulnerability Scanning"	                    10
"RM"	"Risk Management"	                            0
"SA"	"System and Service Acquisition"	            23
"SC"	"System and Communications Protection "	        51
"SI"	"System and Information Integrity"	            23
"SR"	"Supply Chain Risk Management"	                12

