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
                 g=0.15,
                 trackletList=[]):
        self._movingObjectId = movingObjectId
        self._status = status
        self._orbit = orbit
        self._h_v = h_v
        self._g = g
        self.setTrackletList(trackletList)
        return
    
    def setTrackletList(self, trackletList):
        """
        Autmatically compute the arc length.
        """
        self._tracketList = trackletList
        if(trackletList):
            self._archLength = trackletList.getArcLength()
        else:
            self._archLength = None
        return
    
        
    
    
    
    
        
        
























        
        
    





