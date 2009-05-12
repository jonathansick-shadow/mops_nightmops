from DayMOPSObject import DayMOPSObject
from DiaSource import DiaSource
import lsst.daf.persistence as persistence


# Constants
STATUS = {'UNATTRIBUTED': 'U',
          'ATTRIBUTED': 'A',
          'KILLED': 'K'}


class Tracklet(DayMOPSObject):
    def __init__(self, trackletId=None, diaSourceList=[]):
        self._trackletId = trackletId
        self._status = STATUS['UNATTRIBUTED']
        self.setDiaSourceList(diaSourceList)
        return
    
    def setDiaSourceList(self, diaSourceList):
        """
        Set the internal diaSourceList.
        
        @param diaSourceList: DiaSourceList instance.
        """
        # if(not diaSourceList or not len(diaSourceList)):
        #     print('Ops: no DiaSources!')
        
        self._diaSourceList = diaSourceList
        
        # Update velocity data.
        if(self._diaSourceList):
            (self._velRa, 
             self._velDec, 
             self._velTot) = self._diaSourceList.computeVelocityStats()
        return
    
    
        
        
























        
        
    





