"""
Helper functions to create/retrieve a list of MovingObject instances.
"""
from DayMOPSObject import DayMOPSObject
from MovingObject import MovingObject, STATUS
from Orbit import STABLE_STATUS
import dblib

import lsst.daf.persistence as persistence




def getAllMovingObjects(dbLocStr, shallow=True, sliceId=None, numSlices=None):
    """
    Fetch all active and non merged MovingObjects we know anything about.
    
    Use  sliceId and numSlices to implement some form of parallelism.
    If shallow=False, then fetch the Tracklets also.
    
    @param dbLocStr: database connection string.
    @param shallow: if True, do not bother retrieving Tracklets per MovingObject
    @param sliceId: Id of the current Slice.
    @param numSlices: number of available slices (i.e. MPI universe size - 1)
    
    Return 
    Interator to the list of MovingObject instances.
    """
    return(_getMovingObjects(dbLocStr, 'mopsStatus != "%s"' %(STATUS['MERGED']),
                             shallow, sliceId, numSlices))

def getAllUnstableMovingObjects(dbLocStr, shallow=True, sliceId=None, 
                                numSlices=None):
    """
    Fetch all active and non merged MovingObjects we know anything about.
    
    Use  sliceId and numSlices to implement some form of parallelism.
    If shallow=False, then fetch the Tracklets also.
    
    @param dbLocStr: database connection string.
    @param shallow: if True, do not bother retrieving Tracklets per MovingObject
    @param sliceId: Id of the current Slice.
    @param numSlices: number of available slices (i.e. MPI universe size - 1)
    
    Return 
    Interator to the list of MovingObject instances.
    """
    where = 'mopsStatus != "%s" and stablePass != "%s"' \
            %(STATUS['MERGED'], STABLE_STATUS['STABLE'])
    return(_getMovingObjects(dbLocStr, where, shallow, sliceId, numSlices))


def _getMovingObjects(dbLocStr, where, shallow=True, 
                      sliceId=None, numSlices=None):
    """
    Fetch all MovingObjects specifying the SQL where clause we want to use.
    
    Use  sliceId and numSlices to implement some form of parallelism.
    If shallow=False, then fetch the Tracklets also.
    
    Return an iterator.
    """
    if(not shallow):
        # FIXME: Implement deep copy!
        raise(NotImplementedError('Implement deep fetch!'))
    
    # Send the query.
    # sql: select movingObjectId, mopsStatus, h_v, g, 
    #      q, e, i, node, argPeri, timePeri, epoch, 
    #      src01, src02, src03, src04, src05, src06, src07, src08, src09, 
    #      src10, src11, src12, src13, src14, src15, src16, src17, src18, 
    #      src19, src20, src21 from MovingObject where
    #      mopsStatus != "M"
    cols = [('movingObjectId', 'Long'), 
            ('mopsStatus', 'String'),
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
            ('src21', 'Double'),
            ('stablePass', 'String')]
    if(sliceId != None and numSlices > 1):
        where += ' and movingObjectId %% %d = %d' %(numSlices, sliceId)
    
    # Fetch MovingObjects and their Orbit.
    for (mo, o) in dblib.simpleTwoObjectFetch(dbLocStr,
                                              table='MovingObject',
                                              className1='MovingObject',
                                              columns1=cols[:5],
                                              className2='Orbit',
                                              columns2=cols[5:],
                                              where=where):
        # Patch the src
        o.setSrc([getattr(o, 'getSrc%02d' %(i))() for i in range(1, 22, 1)])
        # print([getattr(o, 'getSrc%02d' %(i))() for i in range(1, 22, 1)])
        
        # Now add the Orbit to each MovingObject.
        mo.setOrbit(o)
        yield(mo)
    # return



def _getNextMovingObjectId(dbLocStr):
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




