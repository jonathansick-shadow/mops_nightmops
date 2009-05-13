from DayMOPSObject import DayMOPSObject
from DiaSource import DiaSource
import lib

import lsst.daf.persistence as persistence



class DiaSourceList(DayMOPSObject):
    def __init__(self, diaSources=[]):
        self.setDiaSources(diaSources)
        return
    
    def setDiaSources(self, diaSources):
        """
        Set the list of DiaSources. Always keep that list sorted by MJD.
        
        @param diaSources: list of DiaSource instances.
        """
        self._diaSources = diaSources
        
        # Always keep self._diaSources sorted by MJD.
        self._diaSources.sort()
        return
        
    def getDiaSources(self):
        """
        Return list of DiaSource instances.
        """
        return(self._diaSources)
        
    def __len__(self):
        return(len(self._diaSources))
    
    def __iter__(self):
        return(self._diaSources.__iter__())
    
    @classmethod
    def diaSourceListForTonight(cls, dbLocStr, sliceId=None, numSlices=None):
        """
        Use  sliceId and numSlices to implement some form of parallelism.
        """
        sourceList = cls()
        
        # Send the query.
        # sql: select d.diaSourceId, d.ra, d.decl, d.filterId, d.taiMidPoint, \
        #      d.obsCode, d.apFlux, d.apFluxErr, d.refMag from \
        #      DIASource d, DIASourceIDTonight t where \
        #      t.DIASourceId=d.diaSourceId;
        db = persistence.DbStorage()
        db.setPersistLocation(persistence.LogicalLocation(dbLocStr))
        db.setTableListForQuery(('DIASource', 'DIASourceIDTonight'))
        db.outColumn('DIASource.diaSourceId')
        db.outColumn('DIASource.ra')
        db.outColumn('DIASource.decl')
        db.outColumn('DIASource.filterId')
        db.outColumn('DIASource.taiMidPoint')
        db.outColumn('DIASource.obsCode')
        db.outColumn('DIASource.apFlux')
        db.outColumn('DIASource.apFluxErr')
        db.outColumn('DIASource.refMag')
        where = 'DIASource.diaSourceId=DIASourceIDTonight.DIASourceId'
        if(sliceId != None and numSlices > 1):
            where += ' and DIASource.diaSourceId %% %d = %d' \
                     %(numSlices, sliceId)
        db.setQueryWhere(where)
        db.query()
        
        # Fetch the results.
        diaSources = []
        # FIXME: Update these every time afw updates.
        while(db.next()):
            d = DiaSource()
            d.setDiaSourceId(db.getColumnByPosLong(0))
            d.setRa(db.getColumnByPosDouble(1))
            d.setDec(db.getColumnByPosDouble(2))
            d.setFilterId(db.getColumnByPosInt(3))
            d.setTaiMidPoint(float(db.getColumnByPosDouble(4)))
            d.setObsCode(db.getColumnByPosString(5))
            d.setApFlux(db.getColumnByPosDouble(6))
            d.setApFluxErr(db.getColumnByPosDouble(7))
            d.setRefMag(db.getColumnByPosDouble(8))
            diaSources.append(d)
        db.finishQuery()
        del(db)
        
        # Add the diaSources to the DiaSourceList instance.
        sourceList.setDiaSources(diaSources)
        return(sourceList)
    
    # Methods used to compute some statistics from our DiaSource objects.
    def computeVelocityStats(self):
        """
        Compute basic velocity information based on the details of members of
        self._diaSources.
        
        Return [velRa, velDec, velModulus] (deg/day)
        """
        # self._diaSources is always sorted by MJD. Compute stats on first and 
        # last DiaSource. We assume lineaqr motion from the first DiaSource to
        # the last only for now.
        if(not self._diaSources or len(self._diaSources) < 2):
            return((None, None, None))
        
        first = self._diaSources[0]
        last = self._diaSources[-1]
        
        # Compute time distance in days.
        timeDistance = last.getTaiMidPoint() - first.getTaiMidPoint()
        if(not timeDistance):
            print([(d.getRa(), d.getDec(), d.getTaiMidPoint()) for d in self._diaSources])
            raise(Exception('No temporal spread in DiaSources!'))
        
        # Compute spherical distance.
        distance = lib.sphericalDistance((first.getRa(), first.getDec()),
                                         (last.getRa(), last.getDec()))
        return([d / timeDistance for d in distance])
    
    def getTimeSpan(self):
        """
        Return the time span in day of self._diaSources. The time span is 
        defined as
        max(d.getTaiMidPoint())-min(d.getTaiMidPoint) for d in self._diaSources
        """
        times = [d.getTaiMidPoint() for d in self._diaSources]
        times.sort()
        return(times[-1] - times[0])
    




























