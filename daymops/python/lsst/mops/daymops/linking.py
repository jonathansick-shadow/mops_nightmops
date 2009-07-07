"""
General linking routines and constants.
"""
import lib
import DiaSourceList
import Orbit
from Tracklet import Tracklet

import auton
import numpy
import oorb


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
    
    Return [[tracklet1, tracklet2, ...], ]
    """
    dets = []
    # idToTrackletDict = {}
    for t in tracklets:
        # Update the trackletId -> Tracklet instance mapping.
        trackletId = t.getTrackletId()
        # idToTrackletDict[trackletId] = t
        
        # Convert fluxes to mags.
        for d in t.getDiaSources():
            mag, magErr = lib.fluxToMag(d.getApFlux(), 
                                        d.getApFluxErr(), 
                                        d.getRefMag())
            dets.append((trackletId,
                         d.getTaiMidPoint(),
                         d.getRa(),
                         d.getDec(),
                         mag,
                         int(d.getObsCode()),
                         'dummy'))
    
    # Set basic linkTracklets options.
    args = {'detections': dets,
            'min_obs': minNights * 2,
            'min_sup': minNights,
            'plate_width': plateWidth}
    
    # Get the slow tracks.
    args.update({'minv': slowMinV,
                 'maxv': slowMaxV,
                 'vtree_thresh': slowVtreeThresh,
                 'pred_thresh': slowPredThresh})
    rawTracks = auton.linktracklets(**args)
    
    # Get the fast tracks.
    args.update({'minv': fastMinV,
                 'maxv': fastMaxV,
                 'vtree_thresh': fastVtreeThresh,
                 'pred_thresh': fastPredThresh})
    rawTracks += auton.linktracklets(**args)
    
    # What we get from linkTracklets is simply a list of list of trackletIds:
    #   [[trackletId1, trackletId2, ...], ...]
    # We want tracklet instances, not ids.
    return(rawTracks)
#     tracks = []
#     for rawTrack in rawTracks:
#         tracks.append([idToTrackletDict[tId] for tId in rawTrack])
#         track = []
#         for tId in rawTrack:
#             t = idToTrackletDict[tId]
#             track.append(t)
#         tracks.append(track)
#     del(rawTracks)
#     del(idToTrackletDict)
#     return(tracks)


def orbitDetermination(tracks, 
                       elementType='keplerian', 
                       numRangingOrbits=5000,
                       stdDev=8.3333333333333331e-05,
                       obscode='566'):
    """
    Given a list of tracks, determine one or zero orbits per track and return a
    list of the form
        [orbit|None, ]
    where for each track, we either have an orbit or None.
    
    @param tracks:              a list of lists of Tracklet instances.
    @param elementType:         name of the orbital element type to use.
    @param numRangingOrbits:    number of ranging orbits to produce.
    @param stdDev:              observational RA/Dec uncertainty in degrees.
    """
    # We do statistical ranging first, one track at the time. Then we do LSL on
    # the orbits we get from statistical ranging.
    i = -1
    orbits = []
    for track in tracks:
        i += 1
        # track = tracks[i]: [tracklet1, tracklet2, ...]
        trackId = i
        coords = []
        mjds = []
        mags = []
        filters = []
        obscodes = []                           # In reality we only have one!
        
        # Get to the DiaSources.
        for tracklet in track:
            for d in tracklet.getDiaSources():
                coords.append([d.getRa(), stdDev, d.getDec(), stdDev])
                mags.append(lib.fluxToMag(d.getApFlux(), 
                                          d.getApFluxErr(), 
                                          d.getRefMag()))
                mjds.append(d.getTaiMidPoint())
                # TODO: do we need the filter name or is the ID string OK?
                filters.append(str(d.getFilterId()))
        
        # Now convert those to numpy arrays.
        coords = numpy.array(coords, dtype='d')
        coords.shape = (len(coords), 4)
        obscodes = [obscode, ] * len(mjds)
        mjds = numpy.array(mjds, dtype='d')
        mags = numpy.array(mags, dtype='d')
        
        # We can start statistical ranging.
        try:
            # Choose just 3 or 4 detections for ranging.
            rangingOrbits = oorb.ranging_fast(trackId=trackId,
                                              coords=coords[:3],
                                              mjds=mjds[:3],
                                              mags=mags[:3],
                                              obscodes=obscodes[:3],
                                              filters=filters[:3],
                                              elementType=elementType,
                                              numOrbits=numRangingOrbits)
    
            # Now pass them to LSL and this time use all detections.
            # res = (out_orbit, out_covariance, out_sigmas, out_correlation)
            res = oorb.lsl_fast(trackId=trackId,
                                coords=coords,
                                mjds=mjds,
                                mags=mags,
                                obscodes=obscodes,
                                filters=filters,
                                rangingOrbits=rangingOrbits)
        except:
            # Orbit determination failed for this track. Oh well. Try the next 
            # one.
            orbits.append(None)
            continue
        
        # If everything went well, we have an orbit with covariance.
        # res[0]: [a, e, i, node, argPeri, m, epoch, H, G, elTypeId]
        # res[1]: is a 6x6 covariance matrix, get the diagonal form.
        cov = []
        for i in (0, 1, 2, 3, 4, 5):
            for j in range(i):
                cov.append(res[1][i][j])
        orbits.append(Orbit.Orbit(a=res[0][0],
                                  e=res[0][1],
                                  i=res[0][2],
                                  node=res[0][3],
                                  argPeri=res[0][4],
                                  m=res[0][5],
                                  epoch=res[0][6],
                                  src=cov))
    return(orbits)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    