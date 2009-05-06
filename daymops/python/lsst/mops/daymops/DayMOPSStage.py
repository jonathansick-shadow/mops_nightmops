"""
DayMOPSStage

Abstract class that provides some basic functionality shared by all DayMOPS 
Stages.
"""
import lsst.pex.harness.Stage as Stage
import lsst.pex.policy as policy
import lsst.pex.logging as logging



class DayMOPSStage(object, Stage.Stage):
    def __init__(self, stageId=-1, policy=None):
        """
        Standard Stage initializer.
        """
        # First init the parent class.
        Stage.Stage.__init__(self, stageId, policy)
        
        # Then setup logging.
        self._log = logging.Log(logging.Log.getDefaultLog(), 
                                self.__class__.__name__)
        if(isinstance(self._log, logging.ScreenLog)):
            self._log.setScreenVerbose(True)
        
        # Read some basic verbose levels from policy. Supported verbosityLevels
        # are: DEBUG, INFO, WARN, FATAL. Default is INFO
        userLevel = self._policy.get('verbosityLevel')
        if(userLevel and hasattr(logging.Log, userLevel)):
            self.verbosityLevel = getattr(logging.Log, userLevel)
            msg = 'Setting log verbosity to %s' %(userLevel)
        elif(not userLevel):
            self.verbosityLevel = logging.Log.DEBUG
            msg = 'Verbosity level not specified. Set to DEBUG.'
        else:
            self.verbosityLevel = logging.Log.DEBUG
            msg = 'Verbosity level "%s" not supported. Set to DEBUG.' \
                  %(userLevel)
        
        logging.Trace_setVerbosity('lsst.daymops', self.verbosityLevel)
        self._log.setThreshold(self.verbosityLevel)
        self.logIt('INFO', msg)
        return
    
    def logIt(self, level, logString):
        """
        Write logString to self._log using the given verbosity level.
        
        @param logString: the message to write in the logs.
        @param level: verbosity level. Accepted values DEBUG, INFO, WARN, FATAL.
        """
        return(logging.Rec(self._log, getattr(logging.Log, level)) << logString << logging.endr)





