import lsst.pex.harness.Stage
import lsst.pex.policy as policy
import lsst.pex.logging as log
from lsst.pex.logging import Trace, Trace_setVerbosity
from lsst.pex.logging import endr, Log, Rec

import lsst.mops.mopsLib as mopsLib
import lsst.mops.nightmops.ephemDB as ephDB
'''
A note on time and time scales. Internally we always use times and dates as MJD
in TAI. The only exception is the ephemerides routine inside the SSD module. For
that we do the TAI->UTC conversion.

All times coming in from the DB/clipboard and going to DB/clipboard are also in 
TAI.
'''
import time




class MopsStage(lsst.pex.harness.Stage.Stage):
    def __init__(self, stageId=-1, policy=None):
        """
        Standard Stage initializer.
        """
        lsst.pex.harness.Stage.Stage.__init__(self, stageId, policy)
        self.mopsLog = Log(Log.getDefaultLog(), 'mops.stage')
        if isinstance(self.mopsLog, log.ScreenLog):
            self.mopsLog.setScreenVerbose(True)
        return
    
    
    def logit(self, msg, level=Log.INFO):
        """
        Write msg to self.mopsLog using the input level.
        """
        Rec(self.mopsLog, level) << msg << endr
        return


    def process(self): 
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
        tt0 = time.time()
        Trace_setVerbosity('lsst.mops', 5)
        
        # Get our slice ID  and tot number of slices(for simple parallelism 
        # purposes).        
        sliceId = self.getRank()
        numSlices = self.getUniverseSize() - 1  # want only real slices

        # Get needed params from policy
        ephemDbFromPolicy = self._policy.get('ephemDB')
        fovDiamFromPolicy = self._policy.get('fovDiam')
        obscodeFromPolicy = self._policy.get('obscode')
        
        RIDICOLOUSLY_VERBOSE = self._policy.get('RIDICOLOUSLY_VERBOSE')
        EXTRA_RIDICOLOUSLY_VERBOSE = self._policy.get('EXTRA_RIDICOLOUSLY_VERBOSE')
        ephDB.RIDICOLOUSLY_VERBOSE = RIDICOLOUSLY_VERBOSE
        ephDB.EXTRA_RIDICOLOUSLY_VERBOSE = EXTRA_RIDICOLOUSLY_VERBOSE

        self.logit('Verbose flags: %d %d' %(RIDICOLOUSLY_VERBOSE, EXTRA_RIDICOLOUSLY_VERBOSE))

        # Get objects from clipboard. In our case, since we are the first stage
        # and nobody else is touching the clipboard, we can rely on the
        # dangerous assumption that the only key on the Clipboard is the name of
        # the triggering event.
        # FIXME: This is not safe!!!!!!
        self.activeClipboard = self.inputQueue.getNextDataset()
        clipboardKeys = self.activeClipboard.getKeys()
        if(len(clipboardKeys) == 1):
            eventName = clipboardKeys[0]
        else:
            eventName = 'triggerImageprocEvent0'
        triggerEvent = self.activeClipboard.get(eventName)
        fovRA = triggerEvent.getDouble('ra')
        fovDec = triggerEvent.getDouble('decl')
        visitId = triggerEvent.getInt('visitId')
        mjd = triggerEvent.getDouble('dateobs')

        # Log the beginning of Mops stage for this slice
        self.logit('Began mops stage (MJD: %f visitId: %d)' %(mjd, visitId))
        
        # get this Slice's set of potential objects in the FOV
        if(RIDICOLOUSLY_VERBOSE):
            t0 = time.time()
        candidateOrbits = ephDB.selectOrbitsForFOV(ephemDbFromPolicy, 
                                                   sliceId, 
                                                   numSlices, 
                                                   fovRA,
                                                   fovDec,
                                                   fovDiamFromPolicy / 2.,
                                                   mjd)
        if(RIDICOLOUSLY_VERBOSE):
            self.logit('%.02fs: ephDB.selectOrbitsForFOV()' %(time.time() - t0))
        
        # Propagate each orbit to mjd.
        if(RIDICOLOUSLY_VERBOSE):
            t0 = time.time()
        ephems = [ephDB.propagateOrbit(o, mjd, obscodeFromPolicy) 
                  for o in candidateOrbits]
        if(RIDICOLOUSLY_VERBOSE):
            self.logit('%.02fs: ephDB.propagateOrbit()' %(time.time() - t0))
        
        # Try and reduce the list even further by discarding positions that are
        # entirely outside of the Fov.
        # TODO: Implement something sensible here. Do we need it for DC3a?
        # ephems = [e for e in ephems if ephDB._isinside(e, fovRA, fovDec, 
        #                                                fovDiamFromPolicy)]

        Trace('lsst.mops.MopsStage', 3, 
              'Number of orbits in fov: %d' % len(candidateOrbits))

        # Log the number of predicted ephems
        self.logit('Number of predictions: %d' %(len(ephems)))

        # build a MopsPredVec for our Stage output
        if(RIDICOLOUSLY_VERBOSE):
            t0 = time.time()
        mopsPreds = mopsLib.MopsPredVec()

        # Remember: each ephemeris is a tuple of the form
        # (movingObjectId, movingObjectVersion, mjd, ra, dec, mag, 
        #  smaa, smia, pa)
        # and not an Ephemeris instance.
        for e in ephems:
            mopsPred = mopsLib.MopsPred()
            mopsPred.setId(e[0])
            mopsPred.setVersion(e[1])
            mopsPred.setMjd(e[2])
            mopsPred.setRa(e[3])
            mopsPred.setDec(e[4])
            mopsPred.setSemiMinorAxisLength(e[7])
            mopsPred.setSemiMajorAxisLength(e[6])
            mopsPred.setPositionAngle(e[8])
            mopsPred.setMagnitude(e[5])
            mopsPreds.push_back(mopsPred)
        if(RIDICOLOUSLY_VERBOSE):
            self.logit('%.02fs: assemble mopsPreds' %(time.time() - t0))
        
        # put output on the clipboard
        if(RIDICOLOUSLY_VERBOSE):
            t0 = time.time()
        self.activeClipboard.put('MopsPreds', 
                                 mopsLib.PersistableMopsPredVec(mopsPreds))
        self.outputQueue.addDataset(self.activeClipboard)
        self.mopsLog.log(Log.INFO, 'Mops stage processing ended')
        if(RIDICOLOUSLY_VERBOSE):
            self.logit('%.02fs: post clipboard' %(time.time() - t0))
            self.logit('self.process() took %.02fs' %(time.time() - tt0))
        return



