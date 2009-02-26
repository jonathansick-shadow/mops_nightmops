#!/usr/bin/env python
# from lsst.daf.base import DateTime
import ephemDB_test as ephDB

import math
import time



def process(visitId, fovRA, fovDec, mjd, num_cores=1, slice_id=0):
    """
    Execute the needed processing code for this Stage


    psuedocode: 
    -determine rank (done)
    -get fov, ra, time, and FOVID from clipboard (done)

    - check whether current mjd range is still valid
    - if not, load orbit_id's for our slice (orbit_id%universe_size == rank)
      and current mjd
    
    -get a python list of all orbits (use allOrbits function, which 
     interrogates the DB)
    -use rank to determine this slice's section of the orbits list
    -use propogateOrbit to interpolate those orbits to a known location
    -write those orbits out to a known database table so AP can read them
    """
    # Get needed params from policy
    fovDiamFromPolicy = 3.5                                        # LSST style!
    obscodeFromPolicy = '568'

    # get this Slice's set of potential objects in the FOV
    t0 = time.time()
    candidateOrbits = ephDB.selectOrbitsForFOV(fovRA,
                                               fovDec,
                                               fovDiamFromPolicy / 2.,
                                               mjd,
                                               num_cores,
                                               slice_id)
    print('%.02fs: ephDB.selectOrbitsForFOV()' %(time.time() - t0))

    # Propagate each orbit to mjd.
    t0 = time.time()
    ephems = [ephDB.propagateOrbit(o, mjd, obscodeFromPolicy) 
              for o in candidateOrbits]
    print('%.02fs: ephDB.propagateOrbit()' %(time.time() - t0))

    mopsPreds = []
    t0 = time.time()
    for e in ephems:
        mopsPreds.append((e[0],
                          e[1],
                          e[2],
                          e[3],
                          e[4],
                          e[7],
                          e[6],
                          e[8],
                          e[5]))
    print('%.02fs: assemble mopsPreds' %(time.time() - t0))
    
    # Make sure that they are all in the FoV.
    # Adjust for fuzziness.
    t0 = time.time()
    fovR = (fovDiamFromPolicy / 2.) + 0.3
    cosDec = math.cos(fovDec * math.pi / 180.)
    dec_min = fovDec - fovR
    dec_max = fovDec + fovR
    ra_min = fovRA - fovR * cosDec
    ra_max = fovRA + fovR * cosDec
    if(dec_min > dec_max):
        t = dec_min
        dec_min = dec_max
        dec_max = t
    if(ra_min > ra_max):
        t = ra_min
        ra_min = ra_max
        ra_max = t
    
    i = 0
    while(i < len(mopsPreds)):
        pred_mjd, pred_ra, pred_dec = mopsPreds[i][2:5]
        if(pred_ra < ra_min or
           pred_ra > ra_max or
           pred_dec < dec_min or
           pred_dec > dec_max):
            print('RA:  ' + str((ra_min, ra_max)))
            print('Dec: ' + str((dec_min, dec_max)))
            print('Out of bounds: ' + str(mopsPreds[i]))
            del(mopsPreds[i])
        else:
            i += 1
    print('%.02fs: final checks' %(time.time() - t0))
    return(candidateOrbits, mopsPreds)


if(__name__ == '__main__'):
    import sys
    
    t0 = time.time()
    if(len(sys.argv) not in (6, 7, 8)):
        sys.stderr.write('usage: pipeline_test.py DB visitId, RA, Dec, mjd\n')
        sys.stderr.write('  optionally: specify number of cores last\n')
        sys.stderr.write('  optionally: specify slice ID last\n')
        sys.stderr.write('All times in TAI, not UTC!\n')
        sys.exit(1)
    [db, visitId, fovRA, fovDec, mjd] = sys.argv[1:6]
    try:
        num_cores = int(sys.argv[6])
    except:
        num_cores = 1
    try:
        slice_id = int(sys.argv[7])
    except:
        slice_id = 0
    
    # Update the database name.
    ephDB.DB_DB = db
    candidateOrbits, mopsPreds = process(int(visitId), 
                                         float(fovRA),
                                         float(fovDec),
                                         # DateTime(float(mjd)).utc2tai(),
                                         float(mjd),
                                         num_cores,
                                         slice_id)
    
    # print('Found a total of %d predictions from %d possible orbits.' \
    #       %(len(mopsPreds), len(candidateOrbits)))
    err = len(mopsPreds) != len(candidateOrbits)
    print('%.02fs: total time' %(time.time() - t0))
    print('Total predictions: %d' %(len(mopsPreds)))
    if(err):
        sys.exit(1)
    sys.exit(0)












