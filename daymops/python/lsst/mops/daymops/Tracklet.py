from DayMOPSObject import DayMOPSObject
from DiaSource import DiaSource
import lsst.daf.persistence as persistence


# Constants
STATUS = {'UNATTRIBUTED':   'U',
          'ATTRIBUTED':     'A',
          'KILLED':         'K'}


class Tracklet(DayMOPSObject):
    def __init__(self, 
                 trackletId=None, 
                 status=STATUS['UNATTRIBUTED'],
                 diaSourceList=[]):
        self._trackletId = trackletId
        self._status = status
        self.setDiaSourceList(diaSourceList)
        return
    
    def __str__(self):
        return('Tracklet(trackletId=%d)' %(self._trackletId))
    
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
    
    # Aliases
    def setVelDecl(self, v):
        return(self.setVelDec(v))
    
    
        
        
























        
        
    





