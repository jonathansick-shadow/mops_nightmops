"""
BASIC COURSE
System gets
1. a list of clusters of trackletIds, one cluster per Track
as input.

A. System invokes "Orbit Determination" on the Tracklets from step A.

B. System flags the Tracklets from step B. as LINKED.

C. System flags the new MovingObjects from step B. as NEW.



Policy
  2. OrbitDetermination config
  3. MPC observatory OBSCODE
  4. Database name and location

Input
  1. a list of clusters of trackletIds, one cluster per Track

Output
  1. None/error code?
"""
from DayMOPSStage import DayMOPSStage
from MovingObject import MovingObject, STATUS
import MovingObjectList
import TrackList
import linking
import lib

import time




class OrbitDeterminationStage(DayMOPSStage):
    def __init__(self, stageId=-1, policy=None):
        """
        Standard Stage initializer.
        """
        super(OrbitDeterminationStage, self).__init__(stageId, policy)
        
        # Read the configuration from policy.
        self.obsCode = str(self.getValueFromPolicy('obsCode'))
        self.dbLocStr = self.getValueFromPolicy('database')
                
        self.minNights = self.getValueFromPolicy('minNights')
        self.timeSpan = self.getValueFromPolicy('timeSpan')
        self.utOffset = self.getValueFromPolicy('utOffset')
        
        self.numRangingOrbits = self.getValueFromPolicy('numRangingOrbits')
        self.elementType = self.getValueFromPolicy('elementType')
        self.stdDev = self.getValueFromPolicy('stdDev')
        return
    
    def process(self):
        # Fetch the clipboard.
        self.activeClipboard = self.inputQueue.getNextDataset()
        
        # What is our rank?
        i = self.getRank()
        n = self.getUniverseSize() - 1  # want only real slices
        self.logIt('INFO', 'Slice ID: %d/%d' %(i, n))
        
        # Get all Tracks from the database.
        tracks = [t for t in TrackList.newTracks(self.dbLocStr, shallow=False,
                                                 sliceId=i, numSlices=n)]
        if(not tracks):
            self.outputQueue.addDataset(self.activeClipboard)
            self.logIt('INFO', 'Found 0 tracks found. Quitting.')
            return
        self.logIt('INFO', 'Found %d tracks.' %(len(tracks)))
                
        # Pass the Tracks to the OrbitDetermination code.
        movingObjects = []
        numOrbits = 0
        for track in tracks:
            o = linking.orbitDetermination(track, 
                                           self.elementType,
                                           self.numRangingOrbits,
                                           self.stdDev,
                                           self.obsCode):
            
            # Count the number of not null orbits.
            if(o != None):
                self.logIt('INFO', 'Found an Orbit!')
                numOrbits += 1
                
                # Create temporary MovingObject instances ad write them to the 
                # database.
                movingObjects.append(MovingObject(movingObjectId=None, 
                    status=STATUS['PRELIMINARY']), orbit=o,
                    tracklets=track.getTracklets())
                
        self.logIt('INFO', 'Found %d possible Orbits.' %(numOrbits))
        if(not orbits):
            self.outputQueue.addDataset(self.activeClipboard)
            return
        
        # Now we have a number of proposed linkages. We pass them back to 
        # another stage for consolidation. The idea behid consolidation is to 
        # look for proposed linkages that share at least one tracklet and choose
        # one of those as "true" and discard all the others. Of course the 
        # underlying assumprion (namely that one tracklet can only belong to at 
        # most one orbit) is not necessarily true!
        
        # Save these preliminary MovingObjects to the database.
        # Do not update the status of each Tracklet instance since these are 
        # just preliminary linkages and not necessarily true.
        MovingObjectList.save(self.dbLocStr, movingObjects, False)
        
        # Put the clipboard back.
        self.outputQueue.addDataset(self.activeClipboard)
        return
    
    
    


    

    
    

















