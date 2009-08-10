'''
Important note

I am not happy about this from an aestetical stand point. However we are 
fetching a lot of pre-computed ephemeris from the database. This means that 
instantiating one Ephemeris class per fetched DB ephem is very expensive. Given
the fact that the Ephemeris class was not doing anything other than being a 
container, it makes sense to replace the class with a tuple (performance-wise).

Each ephemeris is therefore a tuple of the form
    (movingObjectId, movingObjectVersion, mjd, ra, dec, mag, smaa, smia, pa)
and not an Ephemeris instance.
'''
# We need to do this because lsstimport (part of base) changes the dlopen 
# options to RTLD_GLOBAL|RTLD_NOW which SSD does not like (and segfaults).
# We also need to move this import to the top otherwise it segfaults after a few
# other imports... what a mess!!!!!!!!!!! This is definitely a HACK :-(
from sys import getdlopenflags, setdlopenflags
try:
    from DLFCN import RTLD_NOW
except:
    from dl import RTLD_NOW

dlflags = getdlopenflags()
setdlopenflags(RTLD_NOW)
import ssd
setdlopenflags(dlflags)

# Import the rest of the packages.
from Orbit import Orbit
import numpy

import auton

from lsst.daf.base import DateTime
import lsst.daf.persistence as dafPer
from lsst.pex.logging import endr, Log, Rec
import time



# Constants/globals.
RIDICOLOUSLY_VERBOSE = False
EXTRA_RIDICOLOUSLY_VERBOSE = False
MOPS_LOG = Log(Log.getDefaultLog(), 'mops.stage')



def logit(msg): 
    return(Rec(MOPS_LOG, Log.INFO) << msg << endr)


def selectOrbitsForFOV(dbLogicalLocation, 
                       sliceId, 
                       numSlices,
                       fovRA, 
                       fovDec, 
                       fovR, 
                       mjd):
    """
    Select from the orbit database those orbits that, at t=MJD, intersect the
    FOV (field of view) specified by (fovRA, fovDec) and whose size is given by
    fovR (which is the half width of the smallest circle enclosing the actual
    FOV).
    """
    if(RIDICOLOUSLY_VERBOSE): 
        logit('Started with selectOrbitsForFOV')
    
    # We want to select orbits that would intersect an area that is a bit bigger
    # than the FoV, just to be on the safe side. How much bigger? 
    # MaxErrorEllipseRadius bigger to take into account realistic positional 
    # errors of good orbits.
    MaxErrorEllipseRadius = 0.166 # ~1 arcminute in degrees
    
    # Fetch all known orbits and their ephemerides at midnight of the prev night
    # this night and next night.
    # orbitIdsAndPositions = [(orbitID, Ephemeris obj), ...]
    if(RIDICOLOUSLY_VERBOSE): 
        t0 = time.time()
    orbitIdsAndPositions = fetchOrbitIdsAndEphems(dbLogicalLocation, 
                                                  sliceId, 
                                                  numSlices, 
                                                  mjd, 
                                                  deltaMJD=1.)
    if(RIDICOLOUSLY_VERBOSE): 
        logit('  %.02fs: fetchOrbitIdsAndEphems()' %(time.time() - t0))
    if(not orbitIdsAndPositions):
        return([])
    
    # Extract orbit_id, mjd, ra, dec.
    # Remember: each ephemeris is a tuple of the form
    # (movingObjectId, movingObjectVersion, mjd, ra, dec, mag, smaa, smia, pa)
    # and not an Ephemeris instance.
    ephemData = [(oId, e[2], e[3], e[4]) for (oId, e) in orbitIdsAndPositions]
    if(not ephemData):
        return([])
    
    # Create a field structure. We simply need a number for field id.
    fields = [(0, mjd, fovRA, fovDec, fovR + MaxErrorEllipseRadius),] 
    
    # Invoke fieldProximity and get a {fieldID: [orbit_id, ...]} mapping of
    # orbits that intersect our field of view (which was given a fieldId = 0).
    if(RIDICOLOUSLY_VERBOSE): 
        t0 = time.time()
    mapping = auton.fieldproximity(fields=fields, orbits=ephemData, method=0)
    if(RIDICOLOUSLY_VERBOSE): 
        logit('  %.02fs: auton.fieldproximity()' %(time.time() - t0))
    
    # Simply return the orbits corresponding to the IDs we got from 
    # fieldProximity.
    return([fetchOrbit(dbLogicalLocation, oid) for oid in mapping.get('0', [])])


def fetchOrbitIdsAndEphems(dbLogicalLocation, sliceId, numSlices, mjd, 
                           deltaMJD=1.):
    """
    Fetch the orbit Id of all known moving objects from day-MOPS together with
    their precomputed ephemerides at int(mjd)-deltaMJD, int(mjd) and
    int(mjd)+deltaMJD.
    
    @param dbLogicalLocation: pointer to the DB.
    @param sliceId: slice ID.
    @param numSlices: total number of slices.
    @param mjd: MJD of the exposure (UTC).
    @param deltaMJD: temporal distance betweeb successive ephemerides.

    Return
        [(internal_orbitId: Ephemeris obj), ] sorted by mjd
    """
    # Init the persistance middleware.
    if(RIDICOLOUSLY_VERBOSE): 
        t3 = time.time()
    db = dafPer.DbStorage()
    
    # Connect to the DB.
    loc = dafPer.LogicalLocation(dbLogicalLocation)
    db.setRetrieveLocation(loc)
    if(RIDICOLOUSLY_VERBOSE): 
        logit('     %.02fs: connect to DB' %(time.time() - t3))
    
    # Prepare the query.
    if(RIDICOLOUSLY_VERBOSE): 
        t3 = time.time()
    deltaMJD = abs(deltaMJD)
    mjdMin = mjd - deltaMJD
    mjdMax = mjd + deltaMJD
    
    # TODO: handle different MovingObject versions. Meaning choose the highest
    # version. Not needed for DC3a.
    where = 'mjd >= %f and mjd <= %f' %(mjdMin, mjdMax)
    # Poor man parallelism ;-)
    # if(numSlices > 0):
    if(numSlices > 1):
        where += ' and movingObjectId %% %d = %d' %(numSlices, sliceId)
    
    db.startTransaction()
    db.setTableForQuery('_tmpl_mops_Ephemeris')
    db.setQueryWhere(where)
    db.outColumn('movingObjectId')
    db.outColumn('movingObjectVersion')
    db.outColumn('mjd')
    db.outColumn('ra')
    db.outColumn('decl')
    db.outColumn('mag')
    db.outColumn('smaa')
    db.outColumn('smia')
    db.outColumn('pa')
    db.orderBy('movingObjectId')
    db.orderBy('mjd')
    if(RIDICOLOUSLY_VERBOSE): 
        logit('     %.02fs: prepare SQL' %(time.time() - t3))
    
    # Execute the query.
    if(RIDICOLOUSLY_VERBOSE): 
        t3 = time.time()
    db.query()
    if(RIDICOLOUSLY_VERBOSE): 
        logit('     %.02fs: exec SQL' %(time.time() - t3))

    # Fetch the results.
    if(RIDICOLOUSLY_VERBOSE): 
        t0 = time.time()
        t1 = 0
        t2 = 0
    res = []
    while db.next():
        if(RIDICOLOUSLY_VERBOSE): 
            tt2 = time.time()
        movingObjectId = db.getColumnByPosInt64(0)
        movingObjectVersion = db.getColumnByPosInt64(1)
        ephem = (movingObjectId,     # movingObjectId
                 movingObjectVersion,     # movingObjectVersion
                 db.getColumnByPosDouble(2),    # mjd
                 db.getColumnByPosDouble(3),    # ra
                 db.getColumnByPosDouble(4),    # decl
                 db.getColumnByPosDouble(5),    # mag
                 db.getColumnByPosDouble(6),    # smaa
                 db.getColumnByPosDouble(7),    # smia
                 db.getColumnByPosDouble(8))    # pa
        if(RIDICOLOUSLY_VERBOSE): 
            t2 += time.time() - tt2
        # We now create a new temp id made by concatenating the movingobject id 
        # and its version. It will only be used internally.
        # res= [(new_orbit_id, Ephemeris obj), ...]
        if(RIDICOLOUSLY_VERBOSE): 
            tt1 = time.time()
        res.append(('%d-%d' %(movingObjectId, movingObjectVersion), ephem))
        if(RIDICOLOUSLY_VERBOSE): 
            t1 += time.time() - tt1
    
    # We are done with the query.
    db.finishQuery()
    if(RIDICOLOUSLY_VERBOSE): 
        logit('     %.02fs: fetch res' %(time.time() - t0 - t1 - t2))
        logit('     %.02fs: Ephemeris()' %(t2))
        logit('     %.02fs: results.append()' %(t1))
    return(res)
    

def fetchOrbit(dbLogicalLocation, orbitId):
    """
    Fetch the full Orbit corresponding to the internal orbitId:
        orbitId = '%d-%d' %(movingObjectId, movingObjectVersion)
    
    @param dbLogicalLocation: pointer to the DB.
    @param orbitId: orbit ID.
    
    Return
        Orbit obj
    """
    if(EXTRA_RIDICOLOUSLY_VERBOSE): 
        t0 = time.time()
        
    # Init the persistance middleware.
    db = dafPer.DbStorage()
    
    # Connect to the DB.
    loc = dafPer.LogicalLocation(dbLogicalLocation)
    db.setRetrieveLocation(loc)
    
    # Remember that we defined a new internal orbitId as the concatenation of
    # movingObjectId and movingObjectVersion: 
    # orbitId = '%d-%d' %(movingObjectId, movingObjectVersion)
    (movingObjectId, movingObjectVersion) = orbitId.split('-')
    
    # Prepare the query.
    where = 'movingObjectId=%s and movingObjectVersion=%s' \
            %(movingObjectId, movingObjectVersion)
    cols = ['q', 'e', 'i', 'node', 'argPeri', 
            'timePeri', 
            'epoch', 
            'h_v', 'g']
    cols += ['src%02d' %(i) for i in range(1, 22)]
    
    db.startTransaction()
    db.setTableForQuery('MovingObject')
    db.setQueryWhere(where)
    errs = map(lambda c: db.outColumn(c), cols)
    
    # Execute the query.
    db.query()
    if(not db.next()):
        if(RIDICOLOUSLY_VERBOSE): 
            logit('fetchOrbit: SQL query failed!')
            logit('SQL: select %s from MovingObject where %s' \
                  %(','.join(cols), where))
        return
    
    # Create the Orbit object and just spit it out.    
    args = [int(movingObjectId), int(movingObjectVersion), ] + \
           [db.getColumnByPosDouble(i) for i in range(9)] + \
           [[db.getColumnByPosDouble(i) for i in range(9, 30, 1)]]
    
    # We are done with the query.
    db.finishQuery()
    if(EXTRA_RIDICOLOUSLY_VERBOSE): 
        logit('     %.02fs: fetchOrbit()' %(time.time() - t0))
    return(Orbit(*args))


def propagateOrbit(orbit, mjd, obscode):
    """
    Compute the ephemerides for orbit orbit at time mjd from obscode.

    Return
        [RA, Dec, mag, mjd, smaa, smia, pa]

        RA: Right Ascension (deg).
        Dec: Declination (deg).
        mag: apparent magnitude (mag).
        mjd: input ephemerides date time (UTC MJD).
        smaa: 1-sigma error ellipse semi major axis (").
        smia: 1-sigma error ellipse semi minor axis (").
        pa: error ellipse position angle (deg).
    """
    # Extract the orbital params and cast them into a numpy array. Convert the 
    # time of perihelion passage to UTC from TAI.
    orbitalParams = numpy.array([orbit.q,
                                 orbit.e,
                                 orbit.i,
                                 orbit.node,
                                 orbit.argPeri,
                                 DateTime(orbit.timePeri).mjd(DateTime.UTC)])
    if(None in list(orbit.src)):
        orbit.src = None

    # Convert the orbit epoch and the prediction requested mjd from TAI to UTC.
    # positions = [[RA, Dec, mag, mjd, raerr, decerr, smaa, smia, pa], ]
    # Convert orbit epoch and ephemerides MJD to UTC from TAI.
    ephems = ssd.ephemerides(orbitalParams, 
                             DateTime(float(orbit.epoch)).mjd(DateTime.UTC),
                             numpy.array([DateTime(mjd).mjd(DateTime.UTC), ]), 
                             str(obscode),
                             float(orbit.hv), 
                             float(orbit.g), 
                             orbit.src)
    (ra, dec, mag, predMjd, raErr, decErr, smaa, smia, pa) = ephems[0]
    
    # Return the Ephemeris object. Return the TAI mjd instead of the one in UTC.
    return((orbit.movingObjectId, 
            orbit.movingObjectVersion, 
            mjd, 
            ra, 
            dec, 
            mag, 
            smaa, 
            smia, 
            pa))
    





