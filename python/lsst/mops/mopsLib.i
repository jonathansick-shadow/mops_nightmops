// -*- lsst-c++ -*-
%define mopsLib_DOCSTRING
"
Access to persistable C++ objects for MOPS catalog data. 
"
%enddef

%feature("autodoc", "1");
%module(docstring=mopsLib_DOCSTRING) mopsLib

// Suppress swig complaints
// I had trouble getting %warnfilter to work; hence the pragmas
#pragma SWIG nowarn=314                 // print is a python keyword (--> _print)
#pragma SWIG nowarn=362                 // operator=  ignored

%{
#include "lsst/afw/detection/Source.h"
#include "lsst/mops/MovingObjectPrediction.h"
#include "lsst/afw/formatters/Utils.h"
%}

%inline %{
namespace boost { namespace filesystem {} }
%}

%init %{
%}

%pythoncode %{
import lsst.afw.image.afwExceptions
%}

%include "lsst/utils/p_lsstSwig.i"
%include "lsst/daf/persistence/persistenceMacros.i"
%import "lsst/daf/base/Persistable.h"

%import "lsst/daf/base/Citizen.h"
%import "lsst/pex/policy/Policy.h"
%import "lsst/daf/persistence/LogicalLocation.h"
%import "lsst/daf/persistence/Persistence.h"
%import "lsst/daf/persistence/Storage.h"
%import "lsst/daf/base/DataProperty.h"


%include <stdint.i>
%include <std_vector.i>
%include <typemaps.i>

%rename(MopsPred)      lsst::mops::MovingObjectPrediction; 
%rename(MopsPredVec)   lsst::mops::MovingObjectPredictionVector;

%include "lsst/afw/detection/Source.h"
%include "lsst/mops/MovingObjectPrediction.h"
%include "lsst/afw/formatters/Utils.h"


// Provide semi-useful printing of catalog records

%extend lsst::mops::MovingObjectPrediction {
    std::string toString() {
        std::ostringstream os;
        os << "Source " << $self->getId();
        os.precision(9);
        os << " (" << $self->getRa() << ", " << $self->getDec() << ")";
        return os.str();
    }
};

%pythoncode %{
MopsPred.__str__  = MopsPred.toString
%}

// Could define a single large SWIG macro to take care of all of this, but for now
// leave it as is for clarity and easy experimentation

%fragment("MovingObjectPredictionVectorTraits","header",fragment="StdSequenceTraits")
%{
namespace swig {
    template <>
    struct traits_asptr<lsst::mops::MovingObjectPredictionVector>  {
        static int asptr(PyObject *obj, lsst::mops::MovingObjectPredictionVector **vec) {
            return traits_asptr_stdseq<lsst::mops::MovingObjectPredictionVector>::asptr(obj, vec);
        }
    };

    template <>
    struct traits_from<lsst::mops::MovingObjectPredictionVector> {
        static PyObject *from(const lsst::mops::MovingObjectPredictionVector& vec) {
            return traits_from_stdseq<lsst::mops::MovingObjectPredictionVector>::from(vec);
        }
    };
}
%}


// Define an analogue to %std_vector_methods()
// required since we have no access to std::vector::get_allocator()
%define %lsst_vector_methods(vec...)
  vec();
  vec(const vec&);
  vec(size_type size);
  vec(size_type size, const value_type& value);

  bool empty() const;
  size_type size() const;
  void clear();

  void swap(vec& v);

  #ifdef SWIG_EXPORT_ITERATOR_METHODS
  class iterator;
  class reverse_iterator;
  class const_iterator;
  class const_reverse_iterator;

  iterator begin();
  const_iterator begin() const;
  iterator end();
  const_iterator end() const;
  reverse_iterator rbegin();
  const_reverse_iterator rbegin() const;
  reverse_iterator rend();
  const_reverse_iterator rend() const;

  iterator erase(iterator pos);
  iterator erase(iterator first, iterator last);

  iterator insert(iterator pos, const value_type& x);
  void insert(iterator pos, size_type n, const value_type& x);
  #endif

  void pop_back();
  void push_back(const value_type& x);  

  const value_type& front() const;
  const value_type& back() const;
 
  void assign(size_type n, const value_type& x);
  void resize(size_type new_size);
  void resize(size_type new_size, const value_type& x);
 
  void reserve(size_type n);
  size_type capacity() const;

  bool operator==(vec const & v);
  bool operator!=(vec const & v);
%enddef


// Apply SWIG std::vector machinery to catalog classes. These classes contain a std::vector and look 
// like a std::vector, but do not derive from one (since std::vector has a non-virtual destructor).
namespace lsst {
namespace mops {


class MovingObjectPredictionVector : public lsst::daf::base::Persistable {
public:
    typedef size_t size_type;
    typedef ptrdiff_t difference_type;
    typedef MovingObjectPrediction value_type;
    typedef value_type* pointer;
    typedef const value_type* const_pointer;
    typedef MovingObjectPrediction& reference;
    typedef const MovingObjectPrediction& const_reference;
    typedef std::allocator<MovingObjectPrediction> allocator_type;

    %traits_swigtype(lsst::mops::MovingObjectPrediction);

    %fragment(SWIG_Traits_frag(lsst::mops::MovingObjectPredictionVector), "header",
              fragment=SWIG_Traits_frag(lsst::mops::MovingObjectPrediction),
              fragment="MovingObjectPredictionVectorTraits") {
        namespace swig {
            template <>  struct traits<lsst::mops::MovingObjectPredictionVector> {
                typedef pointer_category category;
                static const char* type_name() {
                    return "lsst::mops::MovingObjectPredictionVector";
                }
            };
        }
    }

    %typemap_traits_ptr(SWIG_TYPECHECK_VECTOR, lsst::mops::MovingObjectPredictionVector);

    #ifdef %swig_vector_methods
    // Add swig/language extra methods
    %swig_vector_methods(lsst::mops::MovingObjectPredictionVector);
    #endif

    %lsst_vector_methods(lsst::mops::MovingObjectPredictionVector);
};

}}

// Make sure SWIG generates type information for boost::shared_ptr<lsst::pex::base::Persistable> *,
// even though that type is actually wrapped in the persistence module
%types(boost::shared_ptr<lsst::daf::base::Persistable> *);

// Export instantiations of boost::shared_ptr for persistable data vectors
%lsst_persistable_shared_ptr(MopsPredVecSharedPtr, lsst::mops::MovingObjectPredictionVector);


%pythoncode %{

def MopsPredVecPtr(*args):
    """return a MopsPredVecSharedPtr that owns its own MopsPredVec"""
    v = MopsPredVec(*args)
    v.this.disown()
    out = MopsPredVecSharedPtr(v)
    return out


%}

