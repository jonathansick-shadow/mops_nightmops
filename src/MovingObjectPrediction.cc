// -*- lsst-c++ -*-

/* 
 * LSST Data Management System
 * Copyright 2008, 2009, 2010 LSST Corporation.
 * 
 * This product includes software developed by the
 * LSST Project (http://www.lsst.org/).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the LSST License Statement and 
 * the GNU General Public License along with this program.  If not, 
 * see <http://www.lsstcorp.org/LegalNotices/>.
 */
 
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

