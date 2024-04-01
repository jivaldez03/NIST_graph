
create_relatedcontrol_relationship = """
                        // adding relationship between CategoryDetPos (leaves)
                        MATCH (c:Category)<-[rd:DETAILCAT]-(cd:CategoryDet)<-[rdp:DETAILCATPOS]-(cdp:CategoryDetPos)
                        UNWIND cdp.controls as relatedcontrol
                        WITH cdp, cdp.controls as controls, relatedcontrol, split(relatedcontrol,'-') as rcontrol
                        WITH cdp, controls, relatedcontrol, rcontrol[0] as sID, rcontrol[1] as sSUBID
                        MATCH (CDT:CategoryDet {ID: sID, SUBID: toInteger(sSUBID)})
                        MERGE (cdp)<-[r:RELATEDCONTROL]-(CDT)
                        ON MATCH SET r.ctUpdate = datetime()
                        ON CREATE SET r.ctInsert = datetime()
                        RETURN cdp.ID as ID, cdp.SUBID as SUBID, relatedcontrol, sID, sSUBID
                        UNION ALL
                        // adding relationship between CategoryDetPos (roots)
                        MATCH (c:Category)-[rd:DETAILCAT]-(cd:CategoryDet)
                        UNWIND cd.controls as relatedcontrol
                        WITH cd, cd.controls as controls, relatedcontrol, split(relatedcontrol,'-') as rcontrol
                        WITH cd, controls, relatedcontrol, rcontrol[0] as sID, rcontrol[1] as sSUBID
                        MATCH (CDT:CategoryDet {ID: sID, SUBID: toInteger(sSUBID)})
                        MERGE (cd)<-[r:RELATEDCONTROL]-(CDT)
                        ON MATCH SET r.ctUpdate = datetime()
                        ON CREATE SET r.ctInsert = datetime()
                        RETURN cd.ID as ID, cd.SUBID as SUBID, relatedcontrol, sID, sSUBID
                        """

