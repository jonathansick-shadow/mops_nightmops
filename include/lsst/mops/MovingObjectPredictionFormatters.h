// -*- lsst-c++ -*-
/**
 * @file
 * @brief   Formatter subclasses for MovingObjectPrediction and containers thereof
 */

#ifndef LSST_MOPS_MOVING_OBJECT_PREDICTION_FORMATTERS_H
#define LSST_MOPS_MOVING_OBJECT_PREDICTION_FORMATTERS_H

#include "lsst/daf/base.h"
#include "lsst/pex/policy/Policy.h"
#include "lsst/daf/persistence.h"

#include "lsst/mops/MovingObjectPrediction.h"


namespace lsst { namespace mops {


/**
 * Formatter that supports persistence and retrieval with
 * 
 * - lsst::daf::persistence::DbStorage
 * - lsst::daf::persistence::DbTsvStorage
 * - lsst::daf::persistence::BoostStorage
 * 
 * for PersistableMovingObjectPredictionVector instances.
 */
class MovingObjectPredictionVectorFormatter : public lsst::daf::persistence::Formatter {
public:

    virtual ~MovingObjectPredictionVectorFormatter();

    virtual void write(
        lsst::daf::base::Persistable const *,
        lsst::daf::persistence::Storage::Ptr,
        lsst::daf::base::PropertySet::Ptr
    );
    virtual lsst::daf::base::Persistable* read(
        lsst::daf::persistence::Storage::Ptr,
        lsst::daf::base::PropertySet::Ptr
    );
    virtual void update(
        lsst::daf::base::Persistable*,
        lsst::daf::persistence::Storage::Ptr,
        lsst::daf::base::PropertySet::Ptr
    );

    template <class Archive>
    static void delegateSerialize(Archive &, unsigned int const, lsst::daf::base::Persistable *);

private:

    lsst::pex::policy::Policy::Ptr _policy;

    explicit MovingObjectPredictionVectorFormatter(lsst::pex::policy::Policy::Ptr const & policy);

    static lsst::daf::persistence::Formatter::Ptr createInstance(lsst::pex::policy::Policy::Ptr);
    static lsst::daf::persistence::FormatterRegistration registration;

    template <typename T> static void insertRow(T &, MovingObjectPrediction const &);
    static void setupFetch(lsst::daf::persistence::DbStorage &, MovingObjectPrediction &);
};


}}  // end of namespace lsst::mops

#endif // LSST_MOPS_MOVING_OBJECT_PREDICTION_FORMATTERS_H

