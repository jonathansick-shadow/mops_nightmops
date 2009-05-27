"""
General linking routines and constants.
"""
import lib
import DiaSourceList
from Tracklet import Tracklet

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
    
    # Build a dictionary so that given a diaSourceId we can fetch the 
    # corresponding DiaSource instance.
    idDict = dict([(d.getDiaSourceId(), d) for d in sources])
    
    # TODO: compute and use trail information!
    # TODO: Support per-DIASource exposure time.
    # TODO: Use fluxes instead of mags.
    trackletToDiaSourceId = auton.findtracklets(detections=dets, 
                                                maxv=maxV,
                                                minobs=int(minObs),
                                                maxt=maxT,
                                                etime=expTime)
    
    # Create Tracklet instances.
    tracklets = [Tracklet(diaSources=[idDict[_id] for _id in ids]) \
                 for ids in trackletToDiaSourceId]
    
    for t in tracklets:
        if(not t._diaSources):
            raise(Exception('Empty tracklet!'))
    return(tracklets)


def linkTracklets(tracklets, slowMinV, slowMaxV, slowVtreeThresh,slowPredThresh,
                  fastMinV, fastMaxV, fastVtreeThresh, fastPredThresh,minNights,
                  plateWidth):
    """
    Given a list of tracklets, link them into tracks. Do two passes: one for 
    slow movers (defined as having velocity between slowMinV and slowMaxV) and
    one for fast movers (defined as having velocity between fastMinV and 
    fastMaxV).
    
    Return [[trackletId1, trackletID2, ...], ]
    """
    dets = []
    for t in tracklets:
        for d in t.getDiaSources():
            mag, magErr = lib.fluxToMag(d.getApFlux(), 
                                        d.getApFluxErr(), 
                                        d.getRefMag())
            dets.append((t.getTrackletId(),
                         d.getTaiMidPoint(),
                         d.getRa(),
                         d.getDec(),
                         mag,
                         int(d.getObsCode()),
                         'dummy'))
    
    args = {'detections': dets,
            'min_obs': minNights * 2,
            'min_sup': minNights,
            'plate_width': plateWidth}
    
    # Get the slow tracks.
    args.update({'minv': slowMinV,
                 'maxv': slowMaxV,
                 'vtree_thresh': slowVtreeThresh,
                 'pred_thresh': slowPredThresh})
    tracks = auton.linktracklets(**args)
    
    # Get the fast tracks.
    args.update({'minv': fastMinV,
                 'maxv': fastMaxV,
                 'vtree_thresh': fastVtreeThresh,
                 'pred_thresh': fastPredThresh})
    tracks += auton.linktracklets(**args)
    return(tracks)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    