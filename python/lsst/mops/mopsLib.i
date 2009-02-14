// -*- lsst-c++ -*-
%define mopsLib_DOCSTRING
"
Python interface to lsst::mops classes. 
"
%enddef

%feature("autodoc", "1");
%module(package="lsst.mops", docstring=mopsLib_DOCSTRING) mopsLib

// Suppress swig complaints
#pragma SWIG nowarn=314                 // print is a python keyword (--> _print)
#pragma SWIG nowarn=362                 // operator=  ignored

%{
#include "lsst/daf/base.h"
#include "lsst/daf/persistence.h"
#include "lsst/mops/MovingObjectPrediction.h"
#include <sstream>
%}

%include "lsst/p_lsstSwig.i"
%include "lsst/daf/base/persistenceMacros.i"

%import "lsst/daf/base/baseLib.i"
%import "lsst/daf/persistence/persistenceLib.i"

%lsst_exceptions()

%rename(MopsPred) lsst::mops::MovingObjectPrediction; 
%rename(PersistableMopsPredVec) lsst::mops::PersistableMovingObjectPredictionVector;

%template(MopsPredVec) std::vector<lsst::mops::MovingObjectPrediction>;

SWIG_SHARED_PTR_DERIVED(PersistableMopsPredVec,
    lsst::daf::base::Persistable,
    lsst::mops::PersistableMovingObjectPredictionVector);


%include "lsst/mops/MovingObjectPrediction.h"

// Provide semi-useful printing of catalog records
%extend lsst::mops::MovingObjectPrediction {
    std::string toString() {
        std::ostringstream os;
        os << "MovingObjectPrediction " << $self->getId();
        os.precision(9);
        os << " (" << $self->getRa() << ", " << $self->getDec() << ")";
        return os.str();
    }
};

%pythoncode %{
MopsPred.__str__  = MopsPred.toString
%}

%lsst_persistable(lsst::mops::PersistableMovingObjectPredictionVector);

