"""
BASIC COURSE
System gets
1. a list of (NOT ATTRIBUTED AND NOT PRECOVERED AND NOT LINKED) Tracklets 
   belonging to >=1 nights within the last 30 days
as input.

A. System invokes "Link Tracklets"

B. System invokes "Orbit Determination" on the Tracklets from step A.

C. System flags the Tracklets from step B. as LINKED.

D. System flags the new MovingObjects from step B. as NEW.



Policy
  1. LinkTracklets config
  2. OrbitDetermination config
  3. MPC observatory OBSCODE
  4. Database name and location

Input
  1. a list of (NOT ATTRIBUTED AND NOT PRECOVERED AND NOT LINKED) Tracklets 
     belonging to >=1 nights within the last 30 days

Output
  1. None/error code?
"""
from DayMOPSStage import DayMOPSStage
import TrackletList
import linking
import lib

import time




class InterNightLinkingStage(DayMOPSStage):
    def __init__(self, stageId=-1, policy=None):
        """
        Standard Stage initializer.
        """
        super(InterNightLinkingStage, self).__init__(stageId, policy)
        
        # Read the configuration from policy.
        self.obsCode = self.getValueFromPolicy('obsCode')
        self.dbLocStr = self.getValueFromPolicy('database')
        
        self.slowMinV = self.getValueFromPolicy('slowMinV')
        self.slowMaxV = self.getValueFromPolicy('slowMaxV')
        self.slowVtreeThresh = self.getValueFromPolicy('slowVtreeThresh')
        self.slowPredThresh = self.getValueFromPolicy('slowPredThresh')
        
        self.fastMinV = self.getValueFromPolicy('fastMinV')
        self.fastMaxV = self.getValueFromPolicy('fastMaxV')
        self.fastVtreeThresh = self.getValueFromPolicy('fastVtreeThresh')
        self.fastPredThresh = self.getValueFromPolicy('fastPredThresh')
        
        self.plateWidth = self.getValueFromPolicy('plateWidth')
        
        self.minNights = self.getValueFromPolicy('minNights')
        self.timeSpan = self.getValueFromPolicy('timeSpan')
        self.utOffset = self.getValueFromPolicy('utOffset')
        return
    
    def process(self):
        # Fetch the clipboard.
        self.activeClipboard = self.inputQueue.getNextDataset()
        
        # What is our rank?
        i = self.getRank()
        n = self.getUniverseSize() - 1  # want only real slices
        self.logIt('INFO', 'Slice ID: %d/%d' %(i, n))
        
        # Get the night number from the clipboard.
        nightNumber = self.activeClipboard.get('nightNumber')
        if(nightNumber == None):
            # No nightNumber on the clipboard. This is either an error or a sign
            # that there were no DiaSources for tonight. Either way say that we
            # quit and quit.
            self.logIt('INFO', 'No nightNumber on the clipboard. Quitting.')
            self.outputQueue.addDataset(self.activeClipboard)
            return
        self.logIt('INFO', 'Processing up to nightNumber %d' %(nightNumber))
        
        # From nightNumber and self.timeSpan, derive the minimum MJD to 
        # consider.
        minMjd = lib.nightNumberToMjdRange(nightNumber, self.utOffset)[0] - \
                 self.timeSpan
        
        # Fetch the list of available Tracklets within the last 30 days (meaning
        # fetch all non linked/attributed etc. Tracklets with at least one
        # DiaSource whose taiMidPoint is within 30 days of tonight's MJD).
        tracklets = []
        for tracklet in TrackletList.newTracklets(self.dbLocStr, 
                                                  shallow=False,
                                                  fromMjd=minMjd,
                                                  toMjd=None,
                                                  sliceId=i, 
                                                  numSlices=n):
            tracklets.append(tracklet)
        self.logIt('INFO', 'Found %d tracklets.' %(len(tracklets)))
        if(not tracklets):
            self.outputQueue.addDataset(self.activeClipboard)
            return
        
        # Create Tracks from those Tracklets. We do this in two steps: a first
        # step for slow movers (as defined in the policy file) and one for fast
        # movers (again as defined in the policy file).
        tracks = linking.linkTracklets(tracklets, 
                                       self.slowMinV,
                                       self.slowMaxV,
                                       self.slowVtreeThresh,
                                       self.slowPredThresh,
                                       self.fastMinV,
                                       self.fastMaxV,
                                       self.fastVtreeThresh,
                                       self.fastPredThresh,
                                       self.minNights,
                                       self.plateWidth)
        self.logIt('INFO', 'Found %d tracks.' %(len(tracks)))
        if(not tracks):
            self.outputQueue.addDataset(self.activeClipboard)
            return
        
        # Pass the Tracks to the OrbitDetermination code.
        # orbitTrackMapping = linking.orbitDetermination(tracks)
        
        # Now we have a number of proposed linkages. We should pass them back to
        # either another stage or our post-processing method for consolidation.
        # The idea behid consolidation is to look for proposed linkages that 
        # share at least one tracklet and choose one of those as "true" and
        # discard all the others. Of course the underlying assumprion (namely
        # that one tracklet can only belong to at most one orbit) is not 
        # necessarily true!
        
        
        # Put the clipboard back.
        self.outputQueue.addDataset(self.activeClipboard)
        return
    
    
    


    

    
    

















