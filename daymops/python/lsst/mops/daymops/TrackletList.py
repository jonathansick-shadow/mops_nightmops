from DayMOPSObject import DayMOPSObject
from DiaSource import DiaSource
from DiaSourceList import DiaSourceList
from Tracklet import Tracklet
import lsst.daf.persistence as persistence

class TrackletList(DayMOPSObject):
    def __init__(self, tracklets=[]):
        self._tracklets = []
        return
    
    def __len__(self):
        return(len(self._tracklets))
    
    def __iter__(self):
        return(self._tracklets.__iter__())
    
    @classmethod
    def trackletListFromRawIdList(cls, rawList):
        """
        Take the output of findTracklets and build a TrackletList instance.
        
        @param rawList: [[diaSourceId, diaSourceId, ...], ...]
        """
        trackletList = cls()
        if(not rawList):
            return(trackletList)
        
        tracklets = []
        for idList in rawList:
            t = Tracklet()
            
            sources = []
            for _id in idList:
                s = DiaSource()
                s.setDiaSourceId(_id)
                sources.append(s)
            sourceList = DiaSourceList(sources)
            t.setDiaSourceList(sourceList)
            tracklets.append(t)
        trackletList.setTracklets(tracklets)
        
        print(len(trackletList))
        return(trackletList)
    
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
            if(trackletId == None):
                trackletId = newTrackletId
                tracklet.setTrackletId(newTrackletId)
                newTrackletId += 1
            
            dbTrk.setColumnLong('trackletId', trackletId)
            dbTrk.insertRow()
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




