#!/usr/bin/env python
import unittest

import MySQLdb as DBI

try:
    import lsst.mops.daymops.DiaSourceList as DiaSourceList
    from lsst.mops.daymops.DiaSource import DiaSource
except:
    raise(ImportError('Please setup daymops first.'))




# Constants.
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_DBNAME = 'mops_test'
DB_USER = 'www'
DB_PASS = 'zxcvbnm'




class TestDiaSourceList(unittest.TestCase):
    def setUp(self):
        # Build the connection string for the persistence framework.
        self.dbLocStr = 'mysql://%s:%d/%s' %(DB_HOST, int(DB_PORT), DB_DBNAME)
        
        # Connect to the database.
        self._dbh = DBI.connect(host=DB_HOST,
                                port=int(DB_PORT),
                                user=DB_USER,
                                passwd=DB_PASS,
                                db=DB_DBNAME)
        self._dbc = self._dbh.cursor()
        
        # Retrieve the list of DiaSource instances in the database as well as 
        # the ID of the DiaSources belonging to the current night.
        sql = '''\
select DIASource.diaSourceId, 
       DIASource.ra, 
       DIASource.decl, 
       DIASource.filterId, 
       DIASource.taiMidPoint, 
       DIASource.obsCode, 
       DIASource.apFlux, 
       DIASource.apFluxErr, 
       DIASource.refMag
from DIASource'''
        
        # Send the query.
        n = self._dbc.execute(sql)
        
        # Create the DiaSource objects manually.
        self.trueDiaSources = {}
        row = self._dbc.fetchone()
        while(row):
            (_id, ra, dec, fltr, mjd, ocode, fl, flErr, rMag) = row
            d = DiaSource()
            d.setDiaSourceId(int(_id))
            d.setRa(float(ra))
            d.setDec(float(dec))
            d.setFilterId(int(fltr))
            d.setTaiMidPoint(float(mjd))
            d.setObsCode(str(ocode))
            d.setApFlux(float(fl))
            d.setApFluxErr(float(flErr))
            d.setRefMag(float(rMag))
            self.trueDiaSources[_id] = d
            
            row = self._dbc.fetchone()
        
        # Now get the IDs of the ones for tonight.
        sql = 'select DIASourceIDTonight.DIASourceId from DIASourceIDTonight'
        n = self._dbc.execute(sql)
        self.trueIdsForTonight = [int(r[0]) for r in self._dbc.fetchall()]
        return
    
    def testDiaSourceListForTonightOneSlice(self):
        iter = DiaSourceList.diaSourceListForTonight(self.dbLocStr,
                                                     sliceId=0,
                                                     numSlices=1)
        tonightDiaSources = dict([(d.getDiaSourceId(), d) for d in iter])
        
        # Check that their number is correct.
        self.failUnless(len(tonightDiaSources.keys()) == \
                        len(self.trueIdsForTonight),
                        'incorrect number of DiaSources for tonight.')
        
        # Now check that their attributes match.
        for _id in self.trueIdsForTonight:
            trueSource = self.trueDiaSources.get(_id, None)
            source = tonightDiaSources.get(_id, None)
            
            # Check for existance.
            self.failUnless(trueSource != None, 'database inconsistency error.')
            self.failUnless(source != None, 'no DiaSource for ID %d.' %(_id))
            
            # Check for equality.
            self.failUnlessAlmostEqual(trueSource.getRa(), source.getRa(), 6,
                            'DiaSource ID %d has incorrect RA.' %(_id))
            self.failUnlessAlmostEqual(trueSource.getDec(), source.getDec(), 6,
                            'DiaSource ID %d has incorrect Dec.' %(_id))
            self.failUnlessEqual(trueSource.getFilterId(), source.getFilterId(), 
                            'DiaSource ID %d has incorrect filterId.' %(_id))
            self.failUnlessAlmostEqual(trueSource.getTaiMidPoint(), source.getTaiMidPoint(), 6,
                            'DiaSource ID %d has incorrect taiMidPoint.' %(_id))
            self.failUnlessEqual(trueSource.getObsCode(), source.getObsCode(), 
                            'DiaSource ID %d has incorrect obscode.' %(_id))
            self.failUnlessAlmostEqual(trueSource.getApFlux(), source.getApFlux(), 6,
                            'DiaSource ID %d has incorrect ap. flux.' %(_id))
            self.failUnlessAlmostEqual(trueSource.getApFluxErr(), source.getApFluxErr(), 6,
                            'DiaSource ID %d has incorrect ap.flux err.' %(_id))
            self.failUnlessAlmostEqual(trueSource.getRefMag(), source.getRefMag(), 6,
                            'DiaSource ID %d has incorrect ref. mag.' %(_id))
        return




class DBSetupError(Exception): pass


def sanityCheck():
    # Make sure that the database and tables are there.
    dbh = None
    dbc = None
    try:
        dbh = DBI.connect(host=DB_HOST,
                          port=int(DB_PORT),
                          user=DB_USER,
                          passwd=DB_PASS,
                          db=DB_DBNAME)
        dbc = dbh.cursor()
    except:
        raise(DBSetupError('Please create and populate the %s database.' \
                           %(DB_DBNAME)))
    
    sql = 'select count(*) from DIASource'
    n = dbc.execute(sql)
    n = dbc.fetchone()[0]
    if(not n):
        raise(DBSetupError('Please populate the DIASource table.'))
    
    sql = 'select count(*) from DIASourceIDTonight'
    n = dbc.execute(sql)
    n = dbc.fetchone()[0]
    if(not n):
        raise(DBSetupError('Please populate the DIASourceIDTonight table.'))
    return



if(__name__ == '__main__'):
    sanityCheck()        
    unittest.main()




















