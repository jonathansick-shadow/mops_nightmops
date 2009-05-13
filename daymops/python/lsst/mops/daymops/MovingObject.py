from DayMOPSObject import DayMOPSObject
from TrackletList import TrackletList
import lsst.daf.persistence as persistence


# Constants
STATUS = {'NEW':            'N',
          'MERGED':         'M',
          'IOD FAILED':     'I',
          'DIFF FAILED':    'F',
          'OK':             'Y'}


class MovingObject(DayMOPSObject):
    def __init__(self, 
                 movingObjectId=None, 
                 status=STATUS['NEW'],
                 orbit=None,
                 h_v=None,
                 g=.150,
                 trackletList=[],
                 arcLength=None):
        self._movingObjectId = movingObjectId
        self._status = status
        self._orbit = orbit
        self._h_v = h_v
        self.setG(g)
        self._archLength = arcLength
        
        # This updates the arcLength...
        self.setTrackletList(trackletList)
        return
    
    def setG(self, g):
        """
        Set self._g to the desired value. If g=None, then use the default value
        of .150
        """
        if(g == None):
            self._g = .150
        else:
            self._g = g
        return
    
    def setTrackletList(self, trackletList):
        """
        Autmatically compute the arc length, updating it.
        """
        self._tracketList = trackletList
        if(trackletList):
            self._archLength = trackletList.getArcLength()
        return
    
    def __str__(self):
        return('MovingObject(movingObjectId=%d)' %(self._movingObjectId))
    
    # Aliases
    def setArcLengthDays(self, length):
        return(self.setArchLength(length))
    
    
    
        
    
    
    
    
        
        
























        
        
    





