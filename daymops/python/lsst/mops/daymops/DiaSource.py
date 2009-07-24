"""
Class to represent a DIASource object.

This is monkeypatching the corresponding C++ class.
"""
from DayMOPSObject import DayMOPSObject
import lsst.afw.detection as detection
import lsst.daf.persistence as persistence


# This should realy left-inherit from DayMOPSObject, but that doesn't work with
# SWIG :-(
class DiaSource(detection.DiaSource):
    """
    Opaque layer above the DIASource and DIASOurceIDTonight tables.
    
    We compare DiaSources by their MJD alone, not their spatial location.
    """
    _refMag = None
    # FIXME: to be obsoleted by fix to bug #796
    _obsCode = ''
    
    def getRefMag(self):
        return(self._refMag)
    
    def setRefMag(self, mag):
        self._refMag = mag
        return
    
    def getObsCode(self):
        # FIXME: to be obsoleted by fix to bug #796
        return(self._obsCode)
    
    def setObsCode(self, obsCode):
        # FIXME: to be obsoleted by fix to bug #796
        if(not isinstance(obsCode, str) or len(obsCode) != 3):
            raise(SyntaxError('obsCode has to be a 3-letter string.'))
        self._obsCode = str(obsCode)
        return
    
    # Aliases
    def setDecl(self, dec):
        return(self.setDec(dec))
    
    def getDecl(self):
        return(self.getDec())
        
    # Comparison by MJD.
    def __lt__(self, other):
        if(other == None):
            return(False)
        return(self.getTaiMidPoint() < other.getTaiMidPoint())
    
    def __le__(self, other):
        if(other == None):
            return(False)
        return(self.getTaiMidPoint() <= other.getTaiMidPoint())
    
    def __eq__(self, other):
        if(other == None):
            return(False)
        return(self.getTaiMidPoint() == other.getTaiMidPoint())
    
    def __ne__(self, other):
        if(other == None):
            return(True)
        return(self.getTaiMidPoint() != other.getTaiMidPoint())

    def __gt__(self, other):
        if(other == None):
            return(False)
        return(self.getTaiMidPoint() > other.getTaiMidPoint())
    
    def __ge__(self, other):
        if(other == None):
            return(False)
        return(self.getTaiMidPoint() >= other.getTaiMidPoint())
    
    
    
    
    
    
    
    