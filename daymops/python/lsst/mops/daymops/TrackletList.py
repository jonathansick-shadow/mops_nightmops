from DayMOPSObject import DayMOPSObject
from DiaSource import DiaSource
import DiaSourceList
from Tracklet import Tracklet, STATUS
import lsst.daf.persistence as persistence



def newTrackletsFromTonight(dbLocStr, shallow=True, 
                            sliceId=None, numSlices=None):
    """
    Use  sliceId and numSlices to implement some form of parallelism.
    If shallow=False, then fetch the DIASources also.
    
    Return interator.
    """
    if(not shallow):
        # FIXME: Implement deep copy!
        raise(NotImplementedError('Implement deep copy!'))
    
    # Send the query.
    # sql: select distinct(t.trackletId), t.velRa, t.velDecl, t.velTot, 
    #      t.status  from mops_Tracklet t, mops_TrackletsToDIASource td, 
    #      DIASourceIDTonight dt where t.status='U' and 
    #      t.trackletId=td.trackletId and td.diaSourceId=dt.DIASourceId
    db = persistence.DbStorage()
    db.setPersistLocation(persistence.LogicalLocation(dbLocStr))
    db.setTableListForQuery(('mops_Tracklet', 
                             'mops_TrackletsToDIASource',
                             'DIASourceIDTonight'))
    db.outColumn('distinct(mops_Tracklet.trackletId)', True)
    db.outColumn('mops_Tracklet.velRa')
    db.outColumn('mops_Tracklet.velDecl')
    db.outColumn('mops_Tracklet.velTot')
    db.outColumn('mops_Tracklet.status')
    
    where = '''mops_Tracklet.status="U" and 
mops_Tracklet.trackletId=mops_TrackletsToDIASource.trackletId and 
mops_TrackletsToDIASource.diaSourceId=DIASourceIDTonight.DIASourceId'''
    if(sliceId != None and numSlices > 1):
        where += ' and mops_Tracklet.trackletId %% %d = %d' \
                 %(numSlices, sliceId)
    db.setQueryWhere(where)
    db.query()
    
    # Fetch the results.
    while(db.next()):
        t = Tracklet()
        t.setTrackletId(db.getColumnByPosLong(0))
        t.setVelRa(db.getColumnByPosDouble(1))
        t.setVelDec(db.getColumnByPosDouble(2))
        t.setVelTot(db.getColumnByPosDouble(3))
        t.setStatus(db.getColumnByPosString(4))
        yield(t)
    db.finishQuery()
    del(db)
    # return


def getArcLength(tracklets):
    """
    Compute the arc length in days from the DiaSources that are part of this
    list of Tracklets.
    """
    # TODO: is this the most efficient way of computing the arc length?
    # Probably not, but at least is pretty elegant.
    diaSources = reduce(lambda a, b: a+b, [t.getDiaSources for t in tracklets])
    return(diaSources.getTimeSpan())


def save(dbLocStr, tracklets):
    # Get the next available trackletId.
    newTrackletId = _getNextTrackletId(dbLocStr)

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
    for tracklet in tracklets:
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
        for diaSource in tracklet.getDiaSources():
            dbSrc.setColumnLong('trackletId', trackletId)
            dbSrc.setColumnLong('diaSourceId', diaSource.getDiaSourceId())
            dbSrc.insertRow()
    dbTrk.endTransaction()
    dbSrc.endTransaction()
    return


def _getNextTrackletId(dbLocStr):
    # Since trackletId is autoincrement, it cannot be 0. It will get
    # incremented by 1 at the end of the function call...
    trackletId = 0
        
    # Connect to the database.
    db = persistence.DbStorage()
    db.setRetrieveLocation(persistence.LogicalLocation(dbLocStr))
    
    db.setTableForQuery('mops_Tracklet')
    db.outColumn('max(trackletId)', True)      # isExpr=True
    
    db.query()
    if(db.next() and not db.columnIsNull(0)):
        trackletId = db.getColumnByPosLong(0)
    db.finishQuery()
    return(trackletId + 1)




