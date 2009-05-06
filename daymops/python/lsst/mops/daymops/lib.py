"""
Utility functions for DayMOPS
"""
from lsst.daf.base import DateTime

import math



# Constants
DEFAULT_UT_OFFSET = -4.
DEG_TO_RAD = math.pi / 180.
RAD_TO_DEG = 1. / DEG_TO_RAD
LOG10 = math.log(10)
K = -2.5 / LOG10




def nsecToNightNumber(nsecs, utOffset=DEFAULT_UT_OFFSET):
    """
    Given a date in UT TAI nsecs and an offset (in hours) from UT, compute the
    corresponding night number.
    
    Night numbers are defined as
        int(DateTime(nsecs).mjd - .5 + utOffset / 24.)
    which means that the night number increases by 1 at the local noon. All 
    nsecs between two consecutive local noons correspond to the same night 
    number.
    
    The offset from UT (utOffset) is defined as
        local time = UT time - utOffset
    
    @param nsecs: the date to convert (in UT TAI nsecs) to night number.
    @param utOffset: offset from localtime to UT (in hours).
    """
    return(mjdToNightNumber(DateTime(nsecs).mjd(DateTime.TAI), utOffset))

    
def nightNumberToNsecRange(nightNumber, utOffset=DEFAULT_UT_OFFSET):
    """
    Given a night number and an offset (in hours) from UT, compute the 
    corresponding UT TAI nsecs range in the form (nsecMin, nsecMax).
    
    Night numbers are defined as
        int(DateTime(nsecs).mjd - 0.5 + utOffset / 24.0)
    which means that the night number increases by 1 at the local noon. All 
    nsecs between two consecutive local noons correspond to the same night 
    number.
    
    The offset from UT (utOffset) is defined as
        local time = UT time - utOffset
    
    @param nightNumber: the night number to convert to UT TAI nsecs.
    @param utOffset: offset from localtime to UT (in hours).
    """
    return([DateTime(t).nsecs(DateTime.TAI) \
            for t in nightNumberToMjdRange(nightNumber, utOffset)])


def mjdToNightNumber(mjd, utOffset=DEFAULT_UT_OFFSET):
    """
    Given a date in UT TAI MJD and an offset (in hours) from UT, compute the
    corresponding night number.
    
    Night numbers are defined as
        int(mjd - .5 + utOffset / 24.)
    which means that the night number increases by 1 at the local noon. All MJDs
    between two consecutive local noons correspond to the same night number.
    
    The offset from UT (utOffset) is defined as
        local time = UT time - utOffset
    
    @param mjd: the date to convert (in UT TAI MJD) to night number.
    @param utOffset: offset from localtime to UT (in hours).
    """
    return(int(mjd - .5 + utOffset / 24.))

    
def nightNumberToMjdRange(nightNumber, utOffset=DEFAULT_UT_OFFSET):
    """
    Given a night number and an offset (in hours) from UT, compute the 
    corresponding UT TAI MJD range in the form (mjdMin, mjdMax).
    
    Night numbers are defined as
        int(mjd - 0.5 + utOffset / 24.0)
    which means that the night number increases by 1 at the local noon. All MJDs
    between two consecutive local noons correspond to the same night number.
    
    The offset from UT (utOffset) is defined as
        local time = UT time - utOffset
    
    @param nightNumber: the night number to convert to UT TAI MJD.
    @param utOffset: offset from localtime to UT (in hours).
    """
    offset = utOffset / 24.
    mjdMin = nightNumber + .50000 - offset
    mjdMax = nightNumber + 1.49999 - offset
    return(mjdMin, mjdMax)


def fluxToMag(flux, fluxErr, refMag=30.):
    """
    Given a flux, its error and a reference magnitude, transform fluxes in mags 
    and flux errors in mag errors.
    
    We use these formulas:
        mag = refMag - 2.5 * Log(flux)
        magErr = (-2.5 / ln(10)) * (fluxErr / flux)
    
    @param flux: flux to convert to mag
    @param fluxErr: error on flux
    @param refMag: reference magnitude (usually 30.)
    
    Return
        (mag, magErr)
    """
    mag = refMag - 2.5 * math.log(flux, 10)
    magErr = K * fluxErr / flux
    return(mag, magErr)


def magToFlux(mag, magErr, refMag=30.):
    """
    Given a mag, its error and a reference magnitude, transform mags in fluxes 
    and mag errors in flux errors.
    
    We use these formulas:
        flux = 10**(-0.4 * (mag - refMag))
        fluxErr = ln(10) * magErr * flux
    
    @param mag: mag to convert to flux
    @param magErr: error on mag
    @param refMag: reference magnitude (usually 30.)
    
    Return
        (flux, fluxErr)
    """
    flux = 10.**(-0.4 * (mag - refMag))
    fluxErr = flux * magErr * LOG10
    return(flux, fluxErr)
















