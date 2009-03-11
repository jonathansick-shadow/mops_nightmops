// -*- lsst-c++ -*-
/**
 * @file
 * @brief   Implementation of MovingObjectPrediction
 */

#include "lsst/mops/MovingObjectPrediction.h"

namespace lsst { namespace mops {


// -- MovingObjectPrediction ----------------

MovingObjectPrediction::MovingObjectPrediction() :
    _movingObjectId(-1),
    _movingObjectVersion(-1),
    _ra     (0.0),
    _dec    (0.0),
    _smaa   (0.0),
    _smia   (0.0),
    _pa     (0.0),
    _mjd    (0.0),
    _mag    (0.0),
    _magErr (0.0)
{}


bool MovingObjectPrediction::operator==(MovingObjectPrediction const & d) const {
    if (this == &d) {
        return true;
    }
    return _movingObjectId      == d._movingObjectId &&
           _movingObjectVersion == d._movingObjectVersion &&
           _ra                  == d._ra      &&
           _dec                 == d._dec     &&
           _smaa                == d._smaa    &&
           _smia                == d._smia    &&
           _pa                  == d._pa      &&
           _mjd                 == d._mjd     &&
           _mag                 == d._mag     &&
           _magErr              == d._magErr;
}


// -- PersistableMovingObjectPredictionVector ----------------

PersistableMovingObjectPredictionVector::PersistableMovingObjectPredictionVector() :
    lsst::daf::base::Citizen(typeid(*this)),
    _predictions()
{}

PersistableMovingObjectPredictionVector::PersistableMovingObjectPredictionVector(
    MovingObjectPredictionVector const & predictions
) : lsst::daf::base::Citizen(typeid(*this)), _predictions(predictions) {}

PersistableMovingObjectPredictionVector::~PersistableMovingObjectPredictionVector() {}

bool PersistableMovingObjectPredictionVector::operator==(
    MovingObjectPredictionVector const & other
) const {
    if (_predictions.size() != other.size()) {
        return false;
    }
    return std::equal(_predictions.begin(), _predictions.end(), other.begin());
}


}} // end of namespace lsst::mops

