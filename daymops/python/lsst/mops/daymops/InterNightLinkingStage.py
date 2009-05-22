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
  1. a list of (NOT ATTRIBUTED AND NOT PRECOVERED AND NOT LINKED) Tracklets belonging to >=1 nights within the last 30 days

Output
  1. None/error code?
"""
from DayMOPSStage import DayMOPSStage
import attribution
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
        self.residThreshold = self.getValueFromPolicy('residThreshold')
        self.maxSearchRadius = self.getValueFromPolicy('maxSearchRadius')
        self.minSearchRadius = self.getValueFromPolicy('minSearchRadius')
        self.maxArclengthForIod = self.getValueFromPolicy('maxArclengthForIod')
        self.uncertaintySigma = self.getValueFromPolicy('uncertaintySigma')
        self.dbLocStr = self.getValueFromPolicy('database')
        return
    
    def process(self):
        # Fetch the clipboard.
        self.activeClipboard = self.inputQueue.getNextDataset()
        
        # What is our rank?
        i = self.getRank()
        n = self.getUniverseSize() - 1  # want only real slices
        self.logIt('INFO', 'Slice ID: %d/%d' %(i, n))
        
        
        # Do something!
        
        
        # Put the clipboard back.
        self.outputQueue.addDataset(self.activeClipboard)
        return
    
    
    


    

    
    

















