// -*- lsst-c++ -*-
/**
 * @file 
 * @brief   Testing of IO via the persistence framework for
 *          MovingObjectPrediction and MovingObjectPredictionVector.
 */
#include <sys/time.h>
#include <iostream>
#include <sstream>
#include <cstring>
#include <stdexcept>

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE MovingObjectPredictionIO

#include "boost/test/unit_test.hpp"

#include "lsst/pex/exceptions.h"
#include "lsst/daf/base.h"
#include "lsst/pex/policy/Policy.h"
#include "lsst/daf/persistence.h"

#include "lsst/afw/formatters/Utils.h"
#include "lsst/mops/MovingObjectPrediction.h"

using boost::int32_t;
using boost::int64_t;

using lsst::daf::base::Citizen;
using lsst::daf::base::Persistable;
using lsst::daf::base::PropertySet;
using lsst::pex::policy::Policy;
using lsst::daf::persistence::DbAuth;
using lsst::daf::persistence::LogicalLocation;
using lsst::daf::persistence::Persistence;
using lsst::daf::persistence::Storage;

namespace fmt = lsst::afw::formatters;

using namespace lsst::mops;


static std::string const makeTempFile() {
    char name[64];
    std::strncpy(name, "MovingObjectPrediction_XXXXXX", 63);
    name[63] = 0;
    int const fd = ::mkstemp(name);
    BOOST_REQUIRE_MESSAGE(fd != -1, "Failed to create temporary file");
    ::close(fd);
    return std::string(name);
}


static void initTestData(MovingObjectPredictionVector & v, int sliceId = 0) {
    v.reserve(8);
    for (int i = 0; i < 8; ++i) {
        MovingObjectPrediction data;
        // make sure each field has a different value
        // Note: MovingObjectPrediction ids are generated in ascending order
        int j = i*16;
        data.setId                 (j + sliceId*8*16);
        data.setVersion            (j + sliceId*8*16);
        data.setRa                 (static_cast<double>(j + 1));
        data.setDec                (static_cast<double>(j + 2));
        data.setSemiMinorAxisLength(static_cast<double>(j + 3));
        data.setSemiMajorAxisLength(static_cast<double>(j + 4));
        data.setPositionAngle      (static_cast<double>(j + 5));
        data.setMjd                (static_cast<double>(j + 6));
        data.setMagnitude          (static_cast<double>(j + 7));        
        data.setMagnitudeError     (static_cast<float> (j + 8));        
        v.push_back(data);
    }
}


static void testBoost(void) {
    // Create a blank Policy and PropertySet
    Policy::Ptr policy(new Policy);
    PropertySet::Ptr props(new PropertySet);

    // Setup test location
    LogicalLocation loc(makeTempFile());

    // Intialize test data
    PersistableMovingObjectPredictionVector pvec;
    MovingObjectPredictionVector & mopv = pvec.getPredictions();
    initTestData(mopv);

    Persistence::Ptr pers = Persistence::getPersistence(policy);
    // write out data
    {
        Storage::List storageList;
        storageList.push_back(pers->getPersistStorage("BoostStorage", loc));
        pers->persist(pvec, storageList, props);
    }
    // read in data
    {
        Storage::List storageList;
        storageList.push_back(pers->getRetrieveStorage("BoostStorage", loc));
        Persistable::Ptr p =
            pers->retrieve("PersistableMovingObjectPredictionVector", storageList, props);
        BOOST_REQUIRE_MESSAGE(p.get() != 0, "Failed to retrieve Persistable");
        PersistableMovingObjectPredictionVector::Ptr v =
            boost::dynamic_pointer_cast<PersistableMovingObjectPredictionVector, Persistable>(p);
        BOOST_REQUIRE_MESSAGE(v, "Couldn't cast to PersistableMovingObjectPredictionVector");
        BOOST_CHECK_MESSAGE(v->getPredictions() == mopv,
            "persist()/retrieve() resulted in PersistableMovingObjectPredictionVector corruption");
    }
    ::unlink(loc.locString().c_str());
}


// Make at least a token attempt at generating a unique visit id
// (in-db table name collisions could cause spurious testcase failures)
static int createVisitId() {
    struct timeval tv;
    ::gettimeofday(&tv, 0);
    return static_cast<int>(tv.tv_sec);
}


static PropertySet::Ptr createDbTestProps(
    int         const   sliceId,
    int         const   numSlices,
    std::string const & itemName
) {
    BOOST_REQUIRE_MESSAGE(sliceId < numSlices && numSlices > 0, "invalid slice parameters");

    PropertySet::Ptr props(new PropertySet); 

    if (numSlices > 1) {
        props->add("PersistableMovingObjectPredictionVector.isPerSliceTable", true);
        props->add("PersistableMovingObjectPredictionVector.numSlices",       numSlices);
    }
    props->add("visitId", createVisitId());
    props->add("sliceId",  sliceId);
    props->add("itemName", itemName);
    return props;
}


// comparison operator used to sort MovingObjectPrediction in id order
struct MovingObjectPredictionLessThan {
    bool operator()(MovingObjectPrediction const & d1, MovingObjectPrediction const & d2) {
        return d1.getId() < d2.getId();
    }
};


static void testDb(std::string const & storageType) {
    // Create the required Policy and DataProperty
    Policy::Ptr policy(new Policy);
    // use custom table name patterns for this test
    std::string policyRoot("Formatter.PersistableMovingObjectPredictionVector");
    policy->set(policyRoot + ".TestPreds.templateTableName", "_tmpl_mops_Prediction");
    policy->set(policyRoot + ".TestPreds.tableNamePattern", "_tmp_test_Preds_v%(visitId)");
    Policy::Ptr nested(policy->getPolicy(policyRoot));

    PropertySet::Ptr props(createDbTestProps(0, 1, "TestPreds"));

    Persistence::Ptr pers = Persistence::getPersistence(policy);
    LogicalLocation loc("mysql://lsst10.ncsa.uiuc.edu:3306/test");

    // 1. Test on a single MovingObjectPrediction
    MovingObjectPrediction mop;
    PersistableMovingObjectPredictionVector pvec;
    MovingObjectPredictionVector & mopv = pvec.getPredictions();
    mop.setId(13);
    mop.setVersion(13);
    mop.setRa(360.0);
    mop.setDec(-85.0);
    mop.setPositionAngle(35.0);
    mop.setSemiMajorAxisLength(1.0);
    mop.setSemiMinorAxisLength(0.5); 
    mopv.push_back(mop);

    // write out data
    {
        Storage::List storageList;
        storageList.push_back(pers->getPersistStorage(storageType, loc));
        pers->persist(pvec, storageList, props);
    }
    // and read it back in
    {
        Storage::List storageList;
        storageList.push_back(pers->getRetrieveStorage(storageType, loc));
        Persistable::Ptr p =
            pers->retrieve("PersistableMovingObjectPredictionVector", storageList, props);
        BOOST_REQUIRE_MESSAGE(p != 0, "Failed to retrieve Persistable");
        PersistableMovingObjectPredictionVector::Ptr d =
            boost::dynamic_pointer_cast<PersistableMovingObjectPredictionVector, Persistable>(p);
        BOOST_REQUIRE_MESSAGE(d, "Couldn't cast to PersistableMovingObjectPredictionVector");
        BOOST_CHECK_MESSAGE(d->getPredictions().at(0) == mop,
            "persist()/retrieve() resulted in PersistableMovingObjectPredictionVector corruption");
    }
    fmt::dropAllSliceTables(loc, nested, props);

    // 2. Test on multiple MovingObjectPredictions
    mopv.clear();
    initTestData(mopv);
    // write out data
    {
        Storage::List storageList;
        storageList.push_back(pers->getPersistStorage(storageType, loc));
        pers->persist(pvec, storageList, props);
    }
    // and read it back in
    {
        Storage::List storageList;
        storageList.push_back(pers->getRetrieveStorage(storageType, loc));
        Persistable::Ptr pp =
            pers->retrieve("PersistableMovingObjectPredictionVector", storageList, props);
        BOOST_REQUIRE_MESSAGE(pp != 0, "Failed to retrieve Persistable");
        PersistableMovingObjectPredictionVector::Ptr results =
            boost::dynamic_pointer_cast<PersistableMovingObjectPredictionVector, Persistable>(pp);
        BOOST_REQUIRE_MESSAGE(results, "Couldn't cast to PersistableMovingObjectPredictionVector");
        // sort in ascending id order (database does not give any ordering guarantees
        // in the absence of an ORDER BY clause)
        MovingObjectPredictionVector & v = results->getPredictions();
        std::sort(v.begin(), v.end(), MovingObjectPredictionLessThan());
        BOOST_CHECK_MESSAGE(&v != &mopv && v == mopv,
            "persist()/retrieve() resulted in PersistableMovingObjectPredictionVector corruption");
    }
    fmt::dropAllSliceTables(loc, nested, props);
}


static void testDb2(std::string const & storageType) {
    // Create the required Policy and DataProperty
    Policy::Ptr policy(new Policy);
    std::string policyRoot("Formatter.PersistableMovingObjectPredictionVector");
    // use custom table name patterns for this test
    policy->set(policyRoot + ".TestPreds.templateTableName", "_tmpl_mops_Prediction");
    policy->set(policyRoot + ".TestPreds.tableNamePattern", "_tmp_test_v%(visitId)");

    Policy::Ptr nested(policy->getPolicy(policyRoot));

    Persistence::Ptr pers = Persistence::getPersistence(policy);
    LogicalLocation loc("mysql://lsst10.ncsa.uiuc.edu:3306/test");

    MovingObjectPredictionVector all;
    int const numSlices = 3; // and use multiple slice tables
    PropertySet::Ptr props(createDbTestProps(0, numSlices, "TestPreds"));

    // 1. Write out each slice table seperately
    for (int sliceId = 0; sliceId < numSlices; ++sliceId) {
        props->set("sliceId", sliceId);
        PersistableMovingObjectPredictionVector pvec;
        MovingObjectPredictionVector & mopv = pvec.getPredictions();
        initTestData(mopv, sliceId);
        all.insert(all.end(), mopv.begin(), mopv.end());
        Storage::List storageList;
        storageList.push_back(pers->getPersistStorage(storageType, loc));
        pers->persist(pvec, storageList, props);
    }

    // 2. Read in all slice tables - simulates association pipeline
    //    gathering the results of numSlices NightMOPS processing pipeline slices
    Storage::List storageList;
    storageList.push_back(pers->getRetrieveStorage(storageType, loc));
    Persistable::Ptr pp =
        pers->retrieve("PersistableMovingObjectPredictionVector", storageList, props);
    BOOST_REQUIRE_MESSAGE(pp != 0, "Failed to retrieve Persistable");
    PersistableMovingObjectPredictionVector::Ptr results =
        boost::dynamic_pointer_cast<PersistableMovingObjectPredictionVector, Persistable>(pp);
    BOOST_REQUIRE_MESSAGE(results, "Couldn't cast to PersistableMovingObjectPredictionVector");
    // sort in ascending id order (database does not give any ordering guarantees
    // in the absence of an ORDER BY clause)
    MovingObjectPredictionVector & v = results->getPredictions();
    std::sort(v.begin(), v.end(), MovingObjectPredictionLessThan());
    BOOST_CHECK_MESSAGE(&v != &all && v == all,
        "persist()/retrieve() resulted in PersistableMovingObjectPredictionVector corruption");
    fmt::dropAllSliceTables(loc, nested, props);
}


BOOST_AUTO_TEST_CASE(MovingObjectPredictionIO) {
    try {
        testBoost();
        if (lsst::daf::persistence::DbAuth::available("lsst10.ncsa.uiuc.edu", "3306")) {
            testDb("DbStorage");
            testDb("DbTsvStorage");
            testDb2("DbStorage");
            testDb2("DbTsvStorage");
        }
        lsst::daf::base::Citizen::census(std::cout, 0);
        BOOST_CHECK_MESSAGE(lsst::daf::base::Citizen::census(0) == 0, "Detected memory leaks");
    } catch(std::exception const & ex) {
        BOOST_FAIL(ex.what());
    }
}

