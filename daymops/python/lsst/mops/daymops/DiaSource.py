from DayMOPSObject import DayMOPSObject
import lsst.afw.detection as detection
import lsst.daf.persistence as persistence


# This should realy left-inherit from DayMOPSObject, but that doesn't work with
# SWIG :-(
class DiaSource(detection.DiaSource):
    """
    Opaque layer above the DIASource and DIASOurceIDTonight tables.
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


