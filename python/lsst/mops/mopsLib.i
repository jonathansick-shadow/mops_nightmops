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
#include "lsst/pex/policy.h"
#include "lsst/daf/persistence.h"
#include "lsst/mops/MovingObjectPrediction.h"
#include <sstream>
%}

%include "stdint.i"
%include "lsst/p_lsstSwig.i"
%include "lsst/daf/base/persistenceMacros.i"

%import "lsst/daf/base/baseLib.i"

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

