from DayMOPSObject import DayMOPSObject
from DiaSource import DiaSource
from DiaSourceList import DiaSourceList
from Tracklet import Tracklet
import lsst.daf.persistence as persistence

class TrackletList(DayMOPSObject):
    def __init__(self, tracklets=[]):
        self._tracklets = tracklets
        return
    
    def __len__(self):
        return(len(self._tracklets))
    
    def __iter__(self):
        return(self._tracklets.__iter__())
    
    def save(self, dbLocStr):
        # Get the next available trackletId.
        newTrackletId = self._getNextTrackletId(dbLocStr)
    
        # Connect to the database.
        dbTrk = persistence.DbStorage()
        dbTrk.setPersistLocation(persistence.LogicalLocation(dbLocStr))
        dbSrc = persistence.DbStorage()
        dbSrc.setPersistLocation(persistence.LogicalLocation(dbLocStr))
        
        # Prepare for insert.
        dbTrk.setTableForInsert('mops_Tracklet')
        dbSrc.setTableForInsert('mops_TrackletsToDIASource')
        
        dbTrk.startTransaction()
        dbSrc.startTransaction()
        for tracklet in self._tracklets:
            # If the tracklet has an id already, use that, otherwise use a new 
            # one.
            trackletId = tracklet.getTrackletId()
            velRa = tracklet.getVelRa()
            velDec = tracklet.getVelDec()
            velTot = tracklet.getVelTot()
            if(trackletId == None):
                trackletId = newTrackletId
                tracklet.setTrackletId(newTrackletId)
                newTrackletId += 1
            
            # Insert values.
            dbTrk.setColumnLong('trackletId', trackletId)
            dbTrk.setColumnString('status', tracklet.getStatus())
            if(velRa != None and velDec != None and velTot != None):
                dbTrk.setColumnDouble('velRa', velRa)
                dbTrk.setColumnDouble('velDecl', velDec)
                dbTrk.setColumnDouble('velTot', velTot)
            else:
                dbTrk.setColumnToNull('velRa')
                dbTrk.setColumnToNull('velDecl')
                dbTrk.setColumnToNull('velTot')
            dbTrk.insertRow()
            
            # Insert the trackletId <-> diaSourceIds info.
            for diaSource in tracklet.getDiaSourceList():
                dbSrc.setColumnLong('trackletId', trackletId)
                dbSrc.setColumnLong('diaSourceId', diaSource.getDiaSourceId())
                dbSrc.insertRow()
        dbTrk.endTransaction()
        dbSrc.endTransaction()
        return
    
    def _getNextTrackletId(self, dbLocStr):
        # Connect to the database.
        db = persistence.DbStorage()
        db.setRetrieveLocation(persistence.LogicalLocation(dbLocStr))
        
        db.setTableForQuery('mops_Tracklet')
        db.outColumn('max(trackletId)', True)      # isExpr=True
        
        db.query()
        if(db.next()):
            if(db.columnIsNull(0)):
                # Since trackletId is autoincrement, it cannot be 0
                trackletId = 0
            else:
                trackletId = db.getColumnByPosLong(0)
        else:
            # Since trackletId is autoincrement, it cannot be 0
            trackletId = 0
        db.finishQuery()
        del(db)
        return(trackletId + 1)




