#
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

"""
Tests for C++ MovingObjectPrediction and MovingObjectPredictionVector
Python wrappers (including persistence)

Run with:
   python MovingObjectPrediction_1.py
or
   python
   >>> import unittest; T=load("MovingObjectPrediction_1"); unittest.TextTestRunner(verbosity=1).run(T.suite())
"""

import pdb
import unittest
import time
import random
import lsst.daf.base as dafBase
import lsst.pex.policy as pexPolicy
import lsst.daf.persistence as dafPers
import lsst.utils.tests as utilsTests
import lsst.afw.detection as afwDet

import lsst.mops as mops

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def checkMopsPredEqual(v1, v2):
    """Checks that two MopsPredVec objects are equal"""
    assert v1.size() == v2.size()
    for i in xrange(v1.size()):
        assert v1[i] == v2[i]


class MopsPredTestCase(unittest.TestCase):
    """A test case for MopsPred and MopsPredVec"""

    def setUp(self):
        self.mpv1 = mops.MopsPredVec(16)
        self.mpv2 = mops.MopsPredVec()

        for m in xrange(16):
            self.mpv1[m].setId(m)
            ds = mops.MopsPred()
            ds.setId(m)
            ds.setRa(m*20)
            self.mpv2.push_back(ds)

    def tearDown(self):
        del self.mpv1
        del self.mpv2

    def testIterable(self):
        """Check that we can iterate over a MopsPredVec"""
        j = 0
        for i in self.mpv1:
            assert i.getId() == j
            j += 1
        j = 0
        v = self.mpv1[:]
        for i in xrange(v.size()):
            assert v[i].getId() == j
            j += 1

    def testCopyAndCompare(self):
        mpv1Copy = mops.MopsPredVec(self.mpv1)
        mpv2Copy = mops.MopsPredVec(self.mpv2)
        checkMopsPredEqual(mpv1Copy, self.mpv1)
        checkMopsPredEqual(mpv2Copy, self.mpv2)

        mpv1Copy.swap(mpv2Copy)
        checkMopsPredEqual(mpv1Copy, self.mpv2)
        checkMopsPredEqual(mpv2Copy, self.mpv1)

        mpv1Copy.swap(mpv2Copy)
        if mpv1Copy.size() == 0:
            mpv1Copy.push_back(mops.MopsPred())
        else:
            mpv1Copy.pop_back()
        ds = mops.MopsPred()
        ds.setId(123476519374511136)
        mpv2Copy.push_back(ds)
        assert mpv1Copy.size() != self.mpv1.size()
        assert mpv2Copy.size() != self.mpv2.size()

    def testInsertErase(self):
        copy = mops.MopsPredVec()
        split = 8
        inserts = 4
        for i in xrange(split):
            copy.append(self.mpv1[i])
        mop = mops.MopsPred()
        for i in xrange(inserts):
            copy.append(mop)
        for i in xrange(self.mpv1.size() - split):
            copy.append(self.mpv1[split + i])
        del copy[split]
        del copy[split: split + inserts - 1]
        checkMopsPredEqual(self.mpv1, copy)

    def testSlice(self):
        vecSlice = self.mpv1[0:3]
        j = 0
        for i in vecSlice:
            assert i.getId() == j
            j += 1

    def testPersistence(self):
        if dafPers.DbAuth.available("lsst10.ncsa.uiuc.edu", "3306"):
            pol = pexPolicy.Policy()
            pol.set("Formatter.PersistableMovingObjectPredictionVector.TestPreds.templateTableName",
                    "_tmpl_mops_Prediction")
            pol.set("Formatter.PersistableMovingObjectPredictionVector.TestPreds.tableNamePattern",
                    "_tmp_v%(visitId)_Preds")

            pers = dafPers.Persistence.getPersistence(pol)
            loc = dafPers.LogicalLocation("mysql://lsst10.ncsa.uiuc.edu:3306/test")
            props = dafBase.PropertySet()
            props.addInt("visitId", int(time.clock())*16384 + random.randint(0, 16383))
            props.addInt("sliceId", 0)
            props.addInt("numSlices", 1)
            props.addString("itemName", "TestPreds")
            stl = dafPers.StorageList()
            stl.push_back(pers.getPersistStorage("DbStorage", loc))
            pers.persist(mops.PersistableMopsPredVec(self.mpv1), stl, props)
            stl = dafPers.StorageList()
            stl.push_back(pers.getRetrieveStorage("DbStorage", loc))
            persistable = pers.unsafeRetrieve("PersistableMovingObjectPredictionVector", stl, props)
            res = mops.PersistableMopsPredVec.swigConvert(persistable)
            afwDet.dropAllSliceTables(loc, pol.getPolicy(
                "Formatter.PersistableMovingObjectPredictionVector"), props)
            checkMopsPredEqual(res.getPredictions(), self.mpv1)
        else:
            print "skipping database tests"

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


def suite():
    """Returns a suite containing all the test cases in this module."""

    utilsTests.init()

    suites = []
    suites += unittest.makeSuite(MopsPredTestCase)
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    utilsTests.run(suite())

