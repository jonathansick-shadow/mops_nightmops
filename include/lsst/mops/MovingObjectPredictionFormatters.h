// -*- lsst-c++ -*-
//
//##====----------------                                ----------------====##/
//!
//! \file   MovingObjectPredictionFormatters.h
//! \brief  Formatter subclasses for MovingObjectPrediction
//!         and Persistable containers thereof.
//!
//##====----------------                                ----------------====##/

#ifndef LSST_MOPS_FORMATTERS_MOVING_OBJECT_PREDICTION_FORMATTERS_H
#define LSST_MOPS_FORMATTERS_MOVING_OBJECT_PREDICTION_FORMATTERS_H

#include <string>
#include <vector>

#include <lsst/daf/base/DataProperty.h>
#include <lsst/pex/policy/Policy.h>
#include <lsst/daf/persistence/Formatter.h>
#include <lsst/daf/persistence/DbStorage.h>

#include "lsst/mops/MovingObjectPrediction.h"


namespace lsst {
namespace mops {

using namespace lsst::daf::persistence;
using lsst::pex::policy::Policy;
using lsst::daf::base::DataProperty;


/*!
    Formatter that supports persistence and retrieval with

    - lsst::daf::persistence::DbStorage
    - lsst::daf::persistence::DbTsvStorage
    - lsst::daf::persistence::BoostStorage

    for MovingObjectPredictionVector instances.
 */
class MovingObjectPredictionVectorFormatter : public Formatter {
public:

    virtual ~MovingObjectPredictionVectorFormatter();

    virtual void write(lsst::daf::base::Persistable const *, Storage::Ptr, DataProperty::PtrType);
    virtual lsst::daf::base::Persistable* read(Storage::Ptr, DataProperty::PtrType);
    virtual void update(lsst::daf::base::Persistable*, Storage::Ptr, DataProperty::PtrType);

    template <class Archive> static void delegateSerialize(Archive &, unsigned int const, lsst::daf::base::Persistable *);

private:

    Policy::Ptr _policy;

    MovingObjectPredictionVectorFormatter(Policy::Ptr const &);

    static Formatter::Ptr createInstance(Policy::Ptr);
    static FormatterRegistration registration;

    template <typename T> static void insertRow(T &, MovingObjectPrediction const &);
    static void setupFetch(DbStorage &, MovingObjectPrediction &);
};


}}  // end of namespace lsst::mops

#endif // LSST_MOPS_FORMATTERS_MOVING_OBJECT_PREDICTION_FORMATTERS_H

