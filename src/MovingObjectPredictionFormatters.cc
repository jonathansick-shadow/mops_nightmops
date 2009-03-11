// -*- lsst-c++ -*-
/**
 * @file
 * @brief   Implementation of persistence for MovingObjectPrediction instances
 */

#include <memory>

#include "lsst/daf/base.h"
#include "lsst/pex/exceptions.h"
#include "lsst/daf/persistence.h"

#include "boost/any.hpp"
#include "boost/format.hpp"

#include "lsst/afw/formatters/Utils.h"

#include "lsst/mops/MovingObjectPrediction.h"
#include "lsst/mops/MovingObjectPredictionFormatters.h"


namespace mops = lsst::mops;
namespace ex = lsst::pex::exceptions;
namespace fmt = lsst::afw::formatters;

using lsst::daf::base::Persistable;
using lsst::daf::base::PropertySet;
using lsst::daf::persistence::BoostStorage;
using lsst::daf::persistence::DbStorage;
using lsst::daf::persistence::DbTsvStorage;
using lsst::daf::persistence::Formatter;
using lsst::daf::persistence::FormatterRegistration;
using lsst::daf::persistence::Storage;
using lsst::pex::policy::Policy;


// -- MovingObjectPredictionVectorFormatter ----------------

mops::MovingObjectPredictionVectorFormatter::MovingObjectPredictionVectorFormatter(
    Policy::Ptr const & policy
) :
    Formatter(typeid(*this)),
    _policy(policy)
{}

mops::MovingObjectPredictionVectorFormatter::~MovingObjectPredictionVectorFormatter() {}


FormatterRegistration mops::MovingObjectPredictionVectorFormatter::registration(
    "PersistableMovingObjectPredictionVector",
    typeid(mops::PersistableMovingObjectPredictionVector),
    createInstance
);


Formatter::Ptr mops::MovingObjectPredictionVectorFormatter::createInstance(Policy::Ptr policy) {
    return Formatter::Ptr(new MovingObjectPredictionVectorFormatter(policy));
}


/**
 * Inserts a single MovingObjectPrediction into a database table using @a db
 * (an instance of lsst::daf::persistence::DbStorage or subclass thereof).
 */
template <typename T>
void mops::MovingObjectPredictionVectorFormatter::insertRow(T & db, MovingObjectPrediction const & p) {
    db.template setColumn<boost::int64_t>("movingObjectId", p._movingObjectId);
    db.template setColumn<int>("movingObjectVersion", p._movingObjectVersion);
    db.template setColumn<double> ("ra",     p._ra);
    db.template setColumn<double> ("decl",   p._dec);
    db.template setColumn<double> ("mjd",    p._mjd);
    db.template setColumn<double> ("smia",   p._smia);
    db.template setColumn<double> ("smaa",   p._smaa);
    db.template setColumn<double> ("pa",     p._pa);
    db.template setColumn<double> ("mag",    p._mag);
    db.template setColumn<float>  ("magErr", p._magErr);
    db.insertRow();
}

/// @cond
template void mops::MovingObjectPredictionVectorFormatter::insertRow<DbStorage>(DbStorage &, MovingObjectPrediction const &);
template void mops::MovingObjectPredictionVectorFormatter::insertRow<DbTsvStorage>(DbTsvStorage &, MovingObjectPrediction const &);
/// @endcond


/** Prepares for reading MovingObjectPrediction instances from a database table. */
void mops::MovingObjectPredictionVectorFormatter::setupFetch(DbStorage & db, MovingObjectPrediction & p) {
    db.outParam("movingObjectId", &(p._movingObjectId));
    db.outParam("movingObjectVersion", &(p._movingObjectVersion));
    db.outParam("ra",     &(p._ra));
    db.outParam("decl",   &(p._dec));
    db.outParam("mjd",    &(p._mjd));
    db.outParam("smia",   &(p._smia));
    db.outParam("smaa",   &(p._smaa));
    db.outParam("pa",     &(p._pa));
    db.outParam("mag",    &(p._mag));
    db.outParam("magErr", &(p._magErr));
}


template <class Archive>
void mops::MovingObjectPredictionVectorFormatter::delegateSerialize(
    Archive &          archive,
    unsigned int const version,
    Persistable *      persistable
) {
    PersistableMovingObjectPredictionVector * p =
        dynamic_cast<PersistableMovingObjectPredictionVector *>(persistable);
    archive & boost::serialization::base_object<Persistable>(*p);
    MovingObjectPredictionVector::size_type sz;

    if (Archive::is_loading::value) {
        MovingObjectPrediction data;
        archive & sz;
        p->_predictions.clear();
        p->_predictions.reserve(sz);
        for (; sz > 0; --sz) {
            archive & data;
            p->_predictions.push_back(data);
        }
    } else {
        sz = p->_predictions.size();
        archive & sz;
        MovingObjectPredictionVector::iterator const end(p->_predictions.end());
        for (MovingObjectPredictionVector::iterator i = p->_predictions.begin(); i != end; ++i) {
            archive & *i;
        }
    }
}

template void mops::MovingObjectPredictionVectorFormatter::delegateSerialize<boost::archive::text_oarchive>(
    boost::archive::text_oarchive &, unsigned int const, Persistable *
);
template void mops::MovingObjectPredictionVectorFormatter::delegateSerialize<boost::archive::text_iarchive>(
    boost::archive::text_iarchive &, unsigned int const, Persistable *
);
//template void mops::MovingObjectPredictionVectorFormatter::delegateSerialize<boost::archive::binary_oarchive>(
//    boost::archive::binary_oarchive &, unsigned int const, Persistable *
//);
//template void mops::MovingObjectPredictionVectorFormatter::delegateSerialize<boost::archive::binary_iarchive>(
//    boost::archive::binary_iarchive &, unsigned int const, Persistable *
//);


void mops::MovingObjectPredictionVectorFormatter::write(
    Persistable const *persistable,
    Storage::Ptr       storage,
    PropertySet::Ptr   additionalData
) {
    if (persistable == 0) {
        throw LSST_EXCEPT(ex::InvalidParameterException, "No Persistable provided");
    }
    if (!storage) {
        throw LSST_EXCEPT(ex::InvalidParameterException, "No Storage provided");
    }

    PersistableMovingObjectPredictionVector const * p =
        dynamic_cast<PersistableMovingObjectPredictionVector const *>(persistable);
    if (p == 0) {
        throw LSST_EXCEPT(ex::RuntimeErrorException,
                          "Persistable was not of concrete type MovingObjectPredictionVector");
    }
    MovingObjectPredictionVector const & predictions = p->getPredictions();

    if (typeid(*storage) == typeid(BoostStorage)) {
        BoostStorage * bs = dynamic_cast<BoostStorage *>(storage.get());
        if (bs == 0) {
            throw LSST_EXCEPT(ex::RuntimeErrorException, "Didn't get BoostStorage");
        }
        bs->getOArchive() & *p;
    } else if (typeid(*storage) == typeid(DbStorage) || typeid(*storage) == typeid(DbTsvStorage)) {
        std::string itemName(fmt::getItemName(additionalData));
        std::string name(fmt::getVisitSliceTableName(_policy, additionalData));
        std::string model = _policy->getString(itemName + ".templateTableName");
        bool mayExist = !fmt::extractOptionalFlag(additionalData, itemName + ".isPerSliceTable");
        if (typeid(*storage) == typeid(DbStorage)) {
            DbStorage * db = dynamic_cast<DbStorage *>(storage.get());
            if (db == 0) {
                throw LSST_EXCEPT(ex::RuntimeErrorException, "Didn't get DbStorage");
            }
            db->createTableFromTemplate(name, model, mayExist);
            db->setTableForInsert(name);
            MovingObjectPredictionVector::const_iterator const end(predictions.end());
            for (MovingObjectPredictionVector::const_iterator i = predictions.begin(); i != end; ++i) {
                insertRow<DbStorage>(*db, *i);
            }
        } else {
            DbTsvStorage * db = dynamic_cast<DbTsvStorage *>(storage.get());
            if (db == 0) {
                throw LSST_EXCEPT(ex::RuntimeErrorException, "Didn't get DbTsvStorage");
            }
            db->createTableFromTemplate(name, model, mayExist);
            db->setTableForInsert(name);
            MovingObjectPredictionVector::const_iterator const end(predictions.end());
            for (MovingObjectPredictionVector::const_iterator i = predictions.begin(); i != end; ++i) {
                insertRow<DbTsvStorage>(*db, *i);
            }
        }
    } else {
        throw LSST_EXCEPT(ex::InvalidParameterException, "Storage type is not supported");
    }
}


Persistable* mops::MovingObjectPredictionVectorFormatter::read(
    Storage::Ptr     storage,
    PropertySet::Ptr additionalData
) {
    std::auto_ptr<PersistableMovingObjectPredictionVector> p(new PersistableMovingObjectPredictionVector);

    if (typeid(*storage) == typeid(BoostStorage)) {
        BoostStorage* bs = dynamic_cast<BoostStorage *>(storage.get());
        if (bs == 0) {
            throw LSST_EXCEPT(ex::RuntimeErrorException, "Didn't get BoostStorage");
        }
        bs->getIArchive() & *p;
    } else if (typeid(*storage) == typeid(DbStorage) || typeid(*storage) == typeid(DbTsvStorage)) {
        DbStorage * db = dynamic_cast<DbStorage *>(storage.get());
        if (db == 0) {
            throw LSST_EXCEPT(ex::RuntimeErrorException, "Didn't get DbStorage");
        }
        std::vector<std::string> tables;
        fmt::getAllVisitSliceTableNames(tables, _policy, additionalData);

        MovingObjectPredictionVector predictions;
 
        // loop over all retrieve tables, reading in everything
        std::vector<std::string>::const_iterator const end = tables.end();
        for (std::vector<std::string>::const_iterator i = tables.begin(); i != end; ++i) {
            db->setTableForQuery(*i);
            MovingObjectPrediction data;
            setupFetch(*db, data);
            db->query();
            while (db->next()) {
                if (db->columnIsNull(0)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"orbit_id\"");
                }
                if (db->columnIsNull(1)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"ra_deg\"");
                }
                if (db->columnIsNull(2)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"dec_deg\"");
                }
                if (db->columnIsNull(3)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"mjd\"");
                }
                if (db->columnIsNull(4)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"smia\"");
                }
                if (db->columnIsNull(5)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"smaa\"");
                }
                if (db->columnIsNull(6)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"pa\"");
                }
                if (db->columnIsNull(7)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"mag\"");
                }
                if (db->columnIsNull(8)) {
                    throw LSST_EXCEPT(ex::RuntimeErrorException, "null column \"magErr\"");
                }
                predictions.push_back(data);
            }
            db->finishQuery();
        }
        std::swap(predictions, p->_predictions);
    } else {
        throw LSST_EXCEPT(ex::InvalidParameterException, "Storage type is not supported");
    }
    return p.release();
}


void mops::MovingObjectPredictionVectorFormatter::update(Persistable*, Storage::Ptr, PropertySet::Ptr) {
    throw LSST_EXCEPT(ex::RuntimeErrorException, "MovingObjectPredictionVectorFormatter: updates not supported");
}

