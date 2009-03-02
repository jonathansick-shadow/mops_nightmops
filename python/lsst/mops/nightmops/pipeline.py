import lsst.pex.harness.Stage
import lsst.daf.base as datap
import lsst.pex.policy as policy
import lsst.pex.logging as log
from lsst.pex.logging import Trace, Trace_setVerbosity
from lsst.pex.logging import endr, Log, Rec

import lsst.mops.mopsLib as mopsLib
import lsst.mops.nightmops.ephemeris as eph
import lsst.mops.nightmops.ephemDB as ephDB
'''
A note on time and time scales. Internally we always use times and dates as MJD
in UTC. However all times getting in and out of our code are MJDs in TAI.

There are stored procedures to convert between the two:
  MJD UTC -> MJD TAI: 
  MJD TAI -> MJD UTC: utcToMJD(taiToUTC((epoch- 40587.0) * 8.64e13))
'''





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
        Trace_setVerbosity('lsst.mops', 5)
        
        # Get our slice ID  and tot number of slices(for simple parallelism 
        # purposes).        
        sliceId = self.getRank()
        numSlices = self.getUniverseSize() - 1  # want only real slices

        # Get needed params from policy
        ephemDbFromPolicy = self._policy.get('ephemDB')
        fovDiamFromPolicy = self._policy.get('fovDiam')
        obscodeFromPolicy = self._policy.get('obscode')

        # Get objects from clipboard
        self.activeClipboard = self.inputQueue.getNextDataset()
        triggerEvent = self.activeClipboard.get('mops1Event')
        
        fovRA = triggerEvent.findUnique('FOVRA').getValueDouble()
        fovDec = triggerEvent.findUnique('FOVDec').getValueDouble()
        visitId = triggerEvent.findUnique('visitId').getValueInt()
        # Convert the TAI to UTC.
        mjdTAI = taiToUTC(triggerEvent.findUnique('visitTime').getValueDouble())

        # Log the beginning of Mops stage for this slice
        Rec(self.mopsLog, Log.INFO) << 'Began mops stage' << { 'visitId': visitId, 'MJD': mjd } << endr

        # get this Slice's set of potential objects in the FOV
        candidateOrbits = ephDB.selectOrbitsForFOV(ephemDbFromPolicy, 
                                                   sliceId, 
                                                   numSlices, 
                                                   fovRA,
                                                   fovDec,
                                                   fovDiamFromPolicy / 2.,
                                                   mjd)

        # Propagate each orbit to mjd.
        ephems = [ephDB.propagateOrbit(o, mjd, obscodeFromPolicy) 
                  for o in candidateOrbits]
              
        # Try and reduce the list even further by discarding positions that are
        # entirely outside of the Fov.
        # TODO: Implement something sensible here. Do we need it for DC3a?
        # ephems = [e for e in ephems if ephDB._isinside(e, fovRA, fovDec, 
        #                                                fovDiamFromPolicy)]

        Trace('lsst.mops.MopsStage', 3, 
              'Number of orbits in fov: %d' % len(candidateOrbits))

        # Log the number of predicted ephems
        Rec(self.mopsLog, Log.INFO) <<  'Candidate orbits' << { 'nPredObjects': len(candidateOrbits), 'nPredEphems': len(ephems) } << endr

         # build a MopsPredVec for our Stage output
        mopsPreds = mopsLib.MopsPredVec()

        # Remember: each ephemeris is a tuple of the form
        # (movingObjectId, movingObjectVersion, mjd, ra, dec, mag, 
        #  smaa, smia, pa)
        # and not an Ephemeris instance.
        for e in ephems:
            mopsPred = mopsLib.MopsPred()
            mopsPred.setId('%d-%d' %(e[0], e[1]))
            mopsPred.setMjd(e[2])
            mopsPred.setRa(e[3])
            mopsPred.setDec(e[4])
            mopsPred.setSemiMinorAxisLength(e[7])
            mopsPred.setSemiMajorAxisLength(e[6])
            mopsPred.setPositionAngle(e[8])
            mopsPred.setMagnitude(e[5])
            mopsPreds.push_back(mopsPred)
        
        # put output on the clipboard
        self.activeClipboard.put('MopsPreds', 
                                 mopsLib.PersistableMopsPredVec(mopsPreds))
        self.outputQueue.addDataset(self.activeClipboard)
        self.mopsLog.log(Log.INFO, 'Mops stage processing ended')
        return



