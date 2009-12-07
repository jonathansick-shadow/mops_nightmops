// -*- lsst-c++ -*-
/**
 * @file
 * @brief   Persistable C++ data object for moving object predictions
 */

#ifndef LSST_MOPS_MOVING_OBJECT_PREDICTION_H
#define LSST_MOPS_MOVING_OBJECT_PREDICTION_H

#include <algorithm>

#include "boost/cstdint.hpp"

#include "lsst/daf/base/Citizen.h"
#include "lsst/daf/base/Persistable.h"


namespace boost { namespace serialization {
    class access;
}}


namespace lsst { namespace mops {

// forward declarations 
class MovingObjectPredictionVectorFormatter;

/**
 * The predicted attributes of a moving object at a specific time. This class is useful
 * when an unadorned data structure is required (e.g. for placement into shared memory) or
 * is all that is necessary.
 */
class MovingObjectPrediction {
public :

    MovingObjectPrediction();

    // Getters required by association pipeline
    boost::int64_t getId() const { return _movingObjectId; }
    int getVersion() const { return _movingObjectVersion; }
    double getRa() const { return _ra; }
    double getDec() const { return _dec; }
    double getSemiMinorAxisLength() const { return _smia; }
    double getSemiMajorAxisLength() const { return _smaa; }
    double getPositionAngle() const { return _pa; }
    double getMjd() const { return _mjd; }
    double getMagnitude() const { return _mag; }
    float getMagnitudeError() const { return _magErr; }

    void setId(boost::int64_t const id) { _movingObjectId = id; }
    void setVersion(int const v) { _movingObjectVersion = v; }
    void setRa(double const ra) { _ra = ra; }
    void setDec(double const dec) { _dec = dec; }
    void setSemiMinorAxisLength(double const smia) { _smia = smia; }
    void setSemiMajorAxisLength(double const smaa) { _smaa = smaa; }
    void setPositionAngle(double const pa) { _pa = pa; }
    void setMjd(double const mjd) { _mjd = mjd; }
    void setMagnitude(double const mag) { _mag = mag; }
    void setMagnitudeError(float const err) { _magErr = err; }

    bool operator==(MovingObjectPrediction const & d) const;

private :

    boost::int64_t _movingObjectId;      ///< ID of the orbit this is a prediction for
    int _movingObjectVersion; ///< version of the orbit this is a prediction for
    double _ra;     ///< right ascension (deg)
    double _dec;    ///< declination (deg)
    double _smaa;   ///< error ellipse semi major axis (deg)
    double _smia;   ///< error ellipse semi minor axis (deg)
    double _pa;     ///< error ellipse position angle (deg)
    double _mjd;    ///< input ephemerides date time (UTC MJD)
    double _mag;    ///< apparent magnitude (mag)
    float  _magErr; ///< error in apparent magnitude

    template <typename Archive> void serialize(Archive & ar, unsigned int const version) {
        ar & _movingObjectId;
        ar & _movingObjectVersion;
        ar & _ra;
        ar & _dec;
        ar & _smaa;
        ar & _smia;
        ar & _pa;
        ar & _mjd;
        ar & _mag;
        ar & _magErr;
    }

    friend class boost::serialization::access;
    friend class MovingObjectPredictionVectorFormatter;
};

inline bool operator!=(MovingObjectPrediction const & d1, MovingObjectPrediction const & d2) {
    return !(d1 == d2);
}


typedef std::vector<MovingObjectPrediction> MovingObjectPredictionVector;

/**
 * A persistable wrapper for a MovingObjectPredictionVector.
 */
class PersistableMovingObjectPredictionVector :
    public lsst::daf::base::Persistable,
    public lsst::daf::base::Citizen
{
public :

    typedef boost::shared_ptr<PersistableMovingObjectPredictionVector> Ptr;

    PersistableMovingObjectPredictionVector();
    PersistableMovingObjectPredictionVector(MovingObjectPredictionVector const & predictions);
    ~PersistableMovingObjectPredictionVector();
    
    MovingObjectPredictionVector & getPredictions() {
        return _predictions;
    }
    MovingObjectPredictionVector const & getPredictions() const {
        return _predictions;
    }

    void setPredictions(MovingObjectPredictionVector const & predictions) {
        _predictions = predictions;
    }
       
    bool operator==(MovingObjectPredictionVector const & other) const;
    
    bool operator==(PersistableMovingObjectPredictionVector const & other) const {
        return other == _predictions;
    }
    
private:
    LSST_PERSIST_FORMATTER(lsst::mops::MovingObjectPredictionVectorFormatter);
    MovingObjectPredictionVector _predictions;
};


}}  // end of namespace lsst::mops

#endif // LSST_MOPS_MOVING_OBJECT_PREDICTION_H


