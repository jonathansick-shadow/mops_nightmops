from DayMOPSObject import DayMOPSObject
from DiaSource import DiaSource
import lsst.daf.persistence as persistence

class DiaSourceList(DayMOPSObject):
    def __init__(self, diaSources=[]):
        self._diaSources = diaSources
        return
        
    def __len__(self):
        return(len(self._diaSources))
    
    def __iter__(self):
        return(self._diaSources.__iter__())
    
    @classmethod
    def diaSourceListForTonight(cls, dbLocStr):
        sourceList = cls()
        
        # Send the query.
        # sql: select d.diaSourceId, d.ra, d.decl, d.filterId, d.taiMidPoint, \
        #      d.obsCode, d.apFlux, d.apFluxErr, d.refMag from \
        #      DIASource d, DIASourceIDTonight t where \
        #      t.DIASourceId=d.diaSourceId;
        db = persistence.DbStorage()
        db.setPersistLocation(persistence.LogicalLocation(dbLocStr))
        db.setTableListForQuery(('DIASource', 'DIASourceIDTonight'))
        db.outColumn('DIASource.diaSourceId')
        db.outColumn('DIASource.ra')
        db.outColumn('DIASource.decl')
        db.outColumn('DIASource.filterId')
        db.outColumn('DIASource.taiMidPoint')
        db.outColumn('DIASource.obsCode')
        db.outColumn('DIASource.apFlux')
        db.outColumn('DIASource.apFluxErr')
        db.outColumn('DIASource.refMag')
        db.setQueryWhere('DIASource.diaSourceId=DIASourceIDTonight.DIASourceId')
        db.query()
        
        # Fetch the results.
        sourceList._diaSources = []
        # FIXME: Update these every time afw updates.
        while(db.next()):
            d = DiaSource()
            d.setDiaSourceId(db.getColumnByPosLong(0))
            d.setRa(db.getColumnByPosDouble(1))
            d.setDec(db.getColumnByPosDouble(2))
            d.setFilterId(db.getColumnByPosInt(3))
            d.setTaiMidPoint(float(db.getColumnByPosDouble(4)))
            d.setObsCode(db.getColumnByPosString(5))
            d.setApFlux(db.getColumnByPosDouble(6))
            d.setApFluxErr(db.getColumnByPosDouble(7))
            d.setRefMag(db.getColumnByPosDouble(8))
            sourceList._diaSources.append(d)
        db.finishQuery()
        del(db)
        return(sourceList)



