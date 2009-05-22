"""
BASIC SCENARIO

System gets
1. a list of NEW MovingObjects
2. the list of (NOT NEW) MovingObjects
as input.

A. System invokes "Orbit Proximity"

B. For each MovingObject pair identified above:
  B.1. System retrieves the list of DIASources associated to each MovingObject.
  B.2. System invokes "Orbit Determination" on union of the two lists of 
       DIAsources.
  B.3. System marks the two MovingObjects as MERGED and creates a new 
       MovingObject linked to the 2 MERGED ones (using the new orbit derived 
       from the unified list of DIASources) marked as NEW.

RAINY DAY SCENARIO
If step B.2. (OrbitDetermination) failes, the two corresponding MovingObjects 
are left as they are (i.e. their status flags are not modified) and the loop 
continues.



Policy
  1. MPC observatory OBSCODE
  2. OrbitProximity config
  3. OrbitDetermination config
  4. Database name and location

Input
  1. a list of (NEW OR ATTRIBUTED OR PRECOVERED) MovingObjects
  2. a list of NOT (NEW OR ATTRIBUTED OR PRECOVERED) MovingObjects

Output
  1. None/error code?
"""
from DayMOPSStage import DayMOPSStage
import attribution
import lib

import time




class OrbitManagementStage(DayMOPSStage):
    def __init__(self, stageId=-1, policy=None):
        """
        Standard Stage initializer.
        """
        super(OrbitManagementStage, self).__init__(stageId, policy)
        
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
    
    
    


    

    
    

















