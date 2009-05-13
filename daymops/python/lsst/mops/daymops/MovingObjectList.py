from DayMOPSObject import DayMOPSObject
from MovingObject import MovingObject, STATUS
import dblib

import lsst.daf.persistence as persistence



class MovingObjectList(DayMOPSObject):
    def __init__(self, movingObjects=[]):
        self._movingObjects = movingObjects
        return
    
    def __len__(self):
        return(len(self._movingObjects))
    
    def __iter__(self):
        return(self._movingObjects.__iter__())
    
    @classmethod
    def getAllMovingObjects(cls, dbLocStr, shallow=True, 
                            sliceId=None, numSlices=None):
        """
        Fetch all active and non merged MovingObjects we know anything about.
        
        Use  sliceId and numSlices to implement some form of parallelism.
        If shallow=False, then fetch the Tracklets also.
        """
        MovingObjectList = cls()
        
        if(not shallow):
            # FIXME: Implement deep copy!
            raise(NotImplementedError('Implement deep copy!'))
        
        # Send the query.
        # sql: select movingObjectId, mopsStatus, h_v, g, 
        #      q, e, i, node, argPeri, timePeri, epoch, 
        #      src01, src02, src03, src04, src05, src06, src07, src08, src09, 
        #      src10, src11, src12, src13, src14, src15, src16, src17, src18, 
        #      src19, src20, src21 from MovingObject where
        #      mopsStatus != "M"
        cols = [('movingObjectId', 'Long'), 
                ('mopsStatus', 'Char'),         # See bug #807
                ('h_v', 'Double'), 
                ('g', 'Double'), 
                ('arcLengthDays', 'Double'),
                ('q', 'Double'), 
                ('e', 'Double'), 
                ('i', 'Double'), 
                ('node', 'Double'), 
                ('argPeri', 'Double'), 
                ('timePeri', 'Double'), 
                ('epoch', 'Double'), 
                ('src01', 'Double'), 
                ('src02', 'Double'), 
                ('src03', 'Double'), 
                ('src04', 'Double'), 
                ('src05', 'Double'), 
                ('src06', 'Double'), 
                ('src07', 'Double'), 
                ('src08', 'Double'), 
                ('src09', 'Double'), 
                ('src10', 'Double'), 
                ('src11', 'Double'), 
                ('src12', 'Double'), 
                ('src13', 'Double'), 
                ('src14', 'Double'), 
                ('src15', 'Double'), 
                ('src16', 'Double'), 
                ('src17', 'Double'), 
                ('src18', 'Double'), 
                ('src19', 'Double'), 
                ('src20', 'Double'), 
                ('src21', 'Double')]
        where = 'mopsStatus != "%s"' %(STATUS['MERGED'])
        if(sliceId != None and numSlices > 1):
            where += ' and movingObjectId %% %d = %d' %(numSlices, sliceId)
        
        # Fetch MovingObjects and their Orbit.
        objs = dblib.simpleTwoObjectFetch(dbLocStr,
                                          table='MovingObject',
                                          className1='MovingObject',
                                          columns1=cols[:5],
                                          className2='Orbit',
                                          columns2=cols[5:],
                                          where=where)
        
        # Now add the Orbit to each MovingObject.
        movingObjects = []
        for (mo, o) in objs:
            mo.setOrbit(o)
            movingObjects.append(mo)
        
        # Add the diaSources to the DiaSourceList instance.
        MovingObjectList.setMovingObjects(movingObjects)
        return(MovingObjectList)
    
    def _getNextMovingObjectId(self, dbLocStr):
        # Since movingObjectId is autoincrement, it cannot be 0. It will get
        # incremented by 1 at the end of the function call...
        movingObjectId = 0
                
        # Connect to the database.
        db = persistence.DbStorage()
        db.setRetrieveLocation(persistence.LogicalLocation(dbLocStr))
        
        db.setTableForQuery('MovingObject')
        db.outColumn('max(movingObjectId)', True)      # isExpr=True
        
        db.query()
        if(db.next() and not db.columnIsNull(0)):
            movingObjectId = db.getColumnByPosLong(0)
        db.finishQuery()
        return(movingObjectId + 1)




