# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#

# from lsst.daf.base import DateTime
from Orbit import Orbit

import numpy

import auton
import ssd

import MySQLdb as dbi

import time

from utctai import parse, utc_to_tai, tai_to_utc
jd_limits, converters = parse()



# Database connection stuff.
DB_HOST = 'lsst10'
DB_USER = 'test'
DB_PASSWD = 'globular.test'
DB_DB = 'fpierfed_test'



def selectOrbitsForFOV(fovRA, 
                       fovDec, 
                       fovR, 
                       mjd,
                       num_cores=1,
                       slice_id=0):
    """
    Select from the orbit database those orbits that, at t=MJD, intersect the
    FOV (field of view) specified by (fovRA, fovDec) and whose size is given by
    fovR (which is the half width of the smallest circle enclosing the actual
    FOV).
    """
    # We want to select orbits that would intersect an area that is a bit bigger
    # than the FoV, just to be on the safe side. How much bigger? 
    # MaxErrorEllipseRadius bigger to take into account realistic positional 
    # errors of good orbits.
    MaxErrorEllipseRadius = 0.166 # ~1 arcminute in degrees
    
    # Fetch all known orbits and their ephemerides at midnight of the prev night
    # this night and next night.
    t0 = time.time()
    orbitIdsAndPositions = fetchOrbitIdsAndEphems(mjd, 1, num_cores, slice_id)
    print('  %.02fs: fetchOrbitIdsAndEphems()' %(time.time() - t0))
    
    # Extract orbit_id, mjd, ra, dec.
    ephemData = [(oId, e[2], e[3], e[4]) \
                 for (oId, e) in orbitIdsAndPositions]
    
    # Create a field structure. We simply need a number for field id.
    fields = [(0, mjd, fovRA, fovDec, fovR + MaxErrorEllipseRadius),] 
    
    # Invoke fieldProximity and get a {fieldID: [orbit_id, ...]} mapping of
    # orbits that intersect our field of view (which was given a fieldId = 0).
    t0 = time.time()
    mapping = auton.fieldproximity(fields=fields, orbits=ephemData, method=0)
    print('  %.02fs: auton.fieldproximity()' %(time.time() - t0))
    
    # Simply return the orbits corresponding to the IDs we got from 
    # fieldProximity.
    return([fetchOrbit(oid) for oid in mapping.get('0', [])])


def fetchOrbitIdsAndEphems(mjd, deltaMJD=1., num_cores=1, slice_id=0):
    """
    Fetch the orbit Id of all known moving objects from day-MOPS together with
    their precomputed ephemerides at int(mjd)-deltaMJD, int(mjd) and
    int(mjd)+deltaMJD.
    
    @param mjd: MJD of the exposure (UTC).
    @param deltaMJD: temporal distance betweeb successive ephemerides.

    Return
        [(internal_orbitId: Ephemeris obj), ] sorted by mjd
    """
    t3 = time.time()
    dbh = dbi.connect(host=DB_HOST,
                      user=DB_USER,
                      passwd=DB_PASSWD,
                      db=DB_DB)
    cur = dbh.cursor()
    print('     %.02fs: connect to DB %s' %(time.time() - t3, DB_DB))
    
    # Prepare the query.
    t3 = time.time()
    deltaMJD = abs(deltaMJD)
    mjdMin = mjd - deltaMJD
    mjdMax = mjd + deltaMJD
    
    # FIXME: What if the orbit_ids are not contiguous?
    where = 'mjd >= %f and mjd <= %f' %(mjdMin, mjdMax)
    if(num_cores > 1):
        where += ' and movingObjectId %% %d = %d' %(num_cores, slice_id)
    
    cols = ('movingObjectId', 'movingObjectVersion', 
            'mjd', 
            'ra', 'decl', 
            'mag', 'smaa', 'smia', 'pa')
    
    # TODO: handle different MovingObject versions.
    sql = '''select %s 
             from  _tmpl_mops_Ephemeris
             where %s
             order by movingObjectId, mjd'''
    print('     %.02fs: prepare SQL' %(time.time() - t3))
    
    # Execute the query.
    t3 = time.time()
    cur.execute(sql %(', '.join(cols), where))
    print('     %.02fs: exec SQL' %(time.time() - t3))
    
    # Fetch the results.
    t0 = time.time()
    t1 = 0
    t2 = 0
    results = []
    res = cur.fetchone()
    while(res):
        tt2 = time.time()
        ephem = (int(res[0]),
                 int(res[1]),
                 float(res[2]),
                 float(res[3]),
                 float(res[4]),
                 float(res[5]),
                 float(res[6]),
                 float(res[7]),
                 float(res[8]))
        t2 += time.time() - tt2
        
        # We now create a new temp id made by concatenating the movingobject id 
        # and its version. It will only be used internally.
        # res= [(new_orbit_id, Ephemeris obj), ...]
        tt1 = time.time()
        results.append(('%s-%s' %(res[0], res[1]), ephem))
        t1 += time.time() - tt1
        
        # Get the next row
        res = cur.fetchone()
    # We are done with the query.
    print('     %.02fs: fetch res' %(time.time() - t0 - t1 - t2))
    print('     %.02fs: Ephemeris()' %(t2))
    print('     %.02fs: results.append()' %(t1))
    return(results)
    

def fetchOrbit(orbitId):
    """
    Fetch the full Orbit corresponding to the internal orbitId:
        orbitId = '%d-%d' %(movingObjectId, movingObjectVersion)
    
    @param dbLogicalLocation: pointer to the DB.
    @param orbitId: orbit ID.
    
    Return
        Orbit obj
    """
    dbh = dbi.connect(host=DB_HOST,
                      user=DB_USER,
                      passwd=DB_PASSWD,
                      db=DB_DB)
    cur = dbh.cursor()
    
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
    
    sql = '''select %s from MovingObject where %s'''
    
    # Execute the query.
    cur.execute(sql %(', '.join(cols), where))
    res = cur.fetchone()
    
    # Create the Orbit object and just spit it out.
    elements = [float(res[i]) for i in range(0, 9)]
    src = [float(res[i]) for i in range(9, 30, 1)]
    
    args = [int(movingObjectId), int(movingObjectVersion), ] + elements + [src]
    return(Orbit(*args))


def propagateOrbit(orbit, mjd, obscode):
    """
    Compute the ephemerides for orbit orbit at time mjd from obscode. All input
    and output MJDs are in TAI.

    Return
        [RA, Dec, mag, mjd, smaa, smia, pa]

        RA: Right Ascension (deg).
        Dec: Declination (deg).
        mag: apparent magnitude (mag).
        mjd: input ephemerides date time (TAI MJD).
        smaa: error ellipse semi major axis (deg).
        smia: error ellipse semi minor axis (deg).
        pa: error ellipse position angle (deg).
    """
    # Extract the orbital params and cast them into a numpy array. Convert the 
    # time of perihelion passage to UTC from TAI.
    orbitalParams = numpy.array([orbit.q,
                                 orbit.e,
                                 orbit.i,
                                 orbit.node,
                                 orbit.argPeri,
                                 tai_to_utc(orbit.timePeri, 
                                            jd_limits, 
                                            converters)])
    if(None in list(orbit.src)):
        orbit.src = None
    
    # Convert the orbit epoch and the prediction requested mjd from TAI to UTC.
    # positions = [[RA, Dec, mag, mjd, raerr, decerr, smaa, smia, pa], ]
    ephems = ssd.ephemerides(orbitalParams, 
                             tai_to_utc(float(orbit.epoch),
                                        jd_limits,
                                        converters), 
                             numpy.array([tai_to_utc(mjd,
                                                     jd_limits,
                                                     converters), ]), 
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
    





