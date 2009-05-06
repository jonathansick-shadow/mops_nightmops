"""
General linking routines and constants.
"""
import lib
from TrackletList import TrackletList

import auton


# Constants
DEFAULT_MAXV = 2.0                # upper velocity cut (deg/day)
DEFAULT_MINOBS = 2                # min DIASources/tracklet
DEFAULT_MAXOBS = None             # max DIASources/tracklet
DEFAULT_EXTENDED = False          # use trail info when available?
DEFAULT_MAXT = 0.05               # max tracklet time length (day)
DEFAULT_EXPTIME = 15.             # image exposure time (s)
DEFAULT_COLLAPSE_ARGS = '0.002 0.002 5.0 0.05' # collapseTracklets arguments.


def trackletsFromDiaSources(sources, maxV=DEFAULT_MAXV, minObs=DEFAULT_MINOBS, 
                            maxT=DEFAULT_MAXT, expTime=DEFAULT_EXPTIME, 
                            useTrailData=DEFAULT_EXTENDED):
    """
    Form Tracklets form DIASources.
    """
    # dets is [id, mjd, ra, dec, mag, obscode, objName, trailLength, trailAngle]
    dets = [(d.getDiaSourceId(),
             d.getTaiMidPoint(),
             d.getRa(),
             d.getDec(),
             lib.fluxToMag(d.getApFlux(), d.getApFluxErr(), d.getRefMag())[0],
             d.getObsCode(),
             str(d.getDiaSourceId()),
             0.,
             0.) for d in sources]
    
    # TODO: Create classes for Tracklets.
    # TODO: compute and use trail information!
    # TODO: Support per DIASource exposure time.
    # TODO: Use fluxes instead of mags.
    return(auton.findtracklets(detections=dets, 
                               maxv=maxV,
                               minobs=int(minObs),
                               maxt=maxT,
                               etime=expTime))


def trackletListFromDiaSourceList(sourceList, maxV=DEFAULT_MAXV, 
                                  minObs=DEFAULT_MINOBS, maxT=DEFAULT_MAXT, 
                                  expTime=DEFAULT_EXPTIME, 
                                  useTrailData=DEFAULT_EXTENDED):
    """
    Form a TrackletList form a DIASourceList.
    """
    rawIdList = trackletsFromDiaSources(sourceList.getDiaSources(), maxV, 
                                        minObs, maxT, expTime, useTrailData)
    return(TrackletList.trackletListFromRawIdList(rawIdList))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    