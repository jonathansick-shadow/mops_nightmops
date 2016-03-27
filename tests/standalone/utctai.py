#!/usr/bin/env python

#
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

"""
Conversion routines between date/times in UTC and TAI. All dates are assumed to
be in MJD (Modified Julian Day) format.

API
    mjd_tai = utc_to_tai(mjd_utc)
    mjd_utc = tai_to_utc(mjd_tai)

Note
The difference between UTC and TAI is taken from 
    ftp://maia.usno.navy.mil/ser7/tai-utc.dat
The code below was adapted from IDL routines found here
    http://www.physics.wisc.edu/~craigm/idl/down/tai_utc.pro
"""
import functools


MJD_TO_JD = 2400000.5
JD_TO_MJD = -MJD_TO_JD
DAY_TO_SEC = 86400.
SEC_TO_DAY = 1. / DAY_TO_SEC

TAI_MINUS_UTC = '''
 1961 JAN  1 =JD 2437300.5  TAI-UTC=   1.4228180 S + (MJD - 37300.) X 0.001296 S
 1961 AUG  1 =JD 2437512.5  TAI-UTC=   1.3728180 S + (MJD - 37300.) X 0.001296 S
 1962 JAN  1 =JD 2437665.5  TAI-UTC=   1.8458580 S + (MJD - 37665.) X 0.0011232S
 1963 NOV  1 =JD 2438334.5  TAI-UTC=   1.9458580 S + (MJD - 37665.) X 0.0011232S
 1964 JAN  1 =JD 2438395.5  TAI-UTC=   3.2401300 S + (MJD - 38761.) X 0.001296 S
 1964 APR  1 =JD 2438486.5  TAI-UTC=   3.3401300 S + (MJD - 38761.) X 0.001296 S
 1964 SEP  1 =JD 2438639.5  TAI-UTC=   3.4401300 S + (MJD - 38761.) X 0.001296 S
 1965 JAN  1 =JD 2438761.5  TAI-UTC=   3.5401300 S + (MJD - 38761.) X 0.001296 S
 1965 MAR  1 =JD 2438820.5  TAI-UTC=   3.6401300 S + (MJD - 38761.) X 0.001296 S
 1965 JUL  1 =JD 2438942.5  TAI-UTC=   3.7401300 S + (MJD - 38761.) X 0.001296 S
 1965 SEP  1 =JD 2439004.5  TAI-UTC=   3.8401300 S + (MJD - 38761.) X 0.001296 S
 1966 JAN  1 =JD 2439126.5  TAI-UTC=   4.3131700 S + (MJD - 39126.) X 0.002592 S
 1968 FEB  1 =JD 2439887.5  TAI-UTC=   4.2131700 S + (MJD - 39126.) X 0.002592 S
 1972 JAN  1 =JD 2441317.5  TAI-UTC=  10.0       S + (MJD - 41317.) X 0.0      S
 1972 JUL  1 =JD 2441499.5  TAI-UTC=  11.0       S + (MJD - 41317.) X 0.0      S
 1973 JAN  1 =JD 2441683.5  TAI-UTC=  12.0       S + (MJD - 41317.) X 0.0      S
 1974 JAN  1 =JD 2442048.5  TAI-UTC=  13.0       S + (MJD - 41317.) X 0.0      S
 1975 JAN  1 =JD 2442413.5  TAI-UTC=  14.0       S + (MJD - 41317.) X 0.0      S
 1976 JAN  1 =JD 2442778.5  TAI-UTC=  15.0       S + (MJD - 41317.) X 0.0      S
 1977 JAN  1 =JD 2443144.5  TAI-UTC=  16.0       S + (MJD - 41317.) X 0.0      S
 1978 JAN  1 =JD 2443509.5  TAI-UTC=  17.0       S + (MJD - 41317.) X 0.0      S
 1979 JAN  1 =JD 2443874.5  TAI-UTC=  18.0       S + (MJD - 41317.) X 0.0      S
 1980 JAN  1 =JD 2444239.5  TAI-UTC=  19.0       S + (MJD - 41317.) X 0.0      S
 1981 JUL  1 =JD 2444786.5  TAI-UTC=  20.0       S + (MJD - 41317.) X 0.0      S
 1982 JUL  1 =JD 2445151.5  TAI-UTC=  21.0       S + (MJD - 41317.) X 0.0      S
 1983 JUL  1 =JD 2445516.5  TAI-UTC=  22.0       S + (MJD - 41317.) X 0.0      S
 1985 JUL  1 =JD 2446247.5  TAI-UTC=  23.0       S + (MJD - 41317.) X 0.0      S
 1988 JAN  1 =JD 2447161.5  TAI-UTC=  24.0       S + (MJD - 41317.) X 0.0      S
 1990 JAN  1 =JD 2447892.5  TAI-UTC=  25.0       S + (MJD - 41317.) X 0.0      S
 1991 JAN  1 =JD 2448257.5  TAI-UTC=  26.0       S + (MJD - 41317.) X 0.0      S
 1992 JUL  1 =JD 2448804.5  TAI-UTC=  27.0       S + (MJD - 41317.) X 0.0      S
 1993 JUL  1 =JD 2449169.5  TAI-UTC=  28.0       S + (MJD - 41317.) X 0.0      S
 1994 JUL  1 =JD 2449534.5  TAI-UTC=  29.0       S + (MJD - 41317.) X 0.0      S
 1996 JAN  1 =JD 2450083.5  TAI-UTC=  30.0       S + (MJD - 41317.) X 0.0      S
 1997 JUL  1 =JD 2450630.5  TAI-UTC=  31.0       S + (MJD - 41317.) X 0.0      S
 1999 JAN  1 =JD 2451179.5  TAI-UTC=  32.0       S + (MJD - 41317.) X 0.0      S
 2006 JAN  1 =JD 2453736.5  TAI-UTC=  33.0       S + (MJD - 41317.) X 0.0      S
 2009 JAN  1 =JD 2454832.5  TAI-UTC=  34.0       S + (MJD - 41317.) X 0.0      S
'''


class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


class Converter(object):

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def utc2tai(self, mjd_utc):
        return(mjd_utc + (self._x + (mjd_utc - self._y) * self._z) * SEC_TO_DAY)

    def tai2utc(self, mjd_tai):
        return(mjd_tai - (self._x + self._y * self._z) / (self._z + 1) * SEC_TO_DAY)


@memoized
def _find_jd(jds, jd):
    jds.sort()

    result = None
    for jd_start in jds:
        if(jd >= jd_start):
            result = jds.index(jd_start)
        else:
            return(result)
    return(result)


@memoized
def parse(str=TAI_MINUS_UTC):
    '''
    Parse the TAI-UTC data coming from ftp://maia.usno.navy.mil/ser7/tai-utc.dat
    '''
    import copy
    import re

    data = str.strip().split('\n')
    p = re.compile(
        '\s*[0-9]{4}\s*[A-Z]{3}\s*[0-9]{1}\s*=JD\s*([0-9\.]+)\s+TAI-UTC=\s*([0-9\.]+)\s*S\s\+\s*\(MJD\s*-\s*([0-9\.]+)\)\s*X\s*([0-9\.]+)\s*S')

    jds = []
    converters = []
    for line in data:
        m = p.match(line)
        [jd, tai_utc, mjd_off, mjd_mul] = [float(x) for x in m.groups()]
        # Using lambdas or partial function application does not work. This
        # sucks BIG TIME!
        # converters.append((lambda x: tai_utc + (x - mjd_off) * mjd_mul,
        #                    lambda y: mjd_off + (y - tai_utc) / mjd_mul))
        converters.append(Converter(tai_utc, mjd_off, mjd_mul))
        jds.append(jd)
    return(jds, converters)


def utc_to_tai(mjd_utc, jd_limits=None, converters=None):
    '''
    Given a datetime in UTC MJD format, convert it in TAI
    '''
    return(_convert(mjd_utc, 'utc2tai', jd_limits, converters))


def tai_to_utc(mjd_tai, jd_limits=None, converters=None):
    '''
    Given a datetime in TAI MJD format, convert it in UTC
    '''
    return(_convert(mjd_tai, 'tai2utc', jd_limits, converters))


@memoized
def _convert(mjd, method, jd_limits=None, converters=None):
    if(not jd_limits or not converters):
        jd_limits, converters = parse()

    # Convert the MJD to JD.
    jd = mjd + MJD_TO_JD

    # Find the appropriate conversion formula and apply it.
    i = _find_jd(jd_limits, jd)
    if(i == None):
        # Ops! we are before Jan 1, 1961. Just assume that TAI-UTC=0
        return(mjd)
    return(getattr(converters[i], method)(mjd))


if(__name__ == '__main__'):
    import sys

    if(len(sys.argv) != 3):
        sys.stderr.write('Usage: utctai.py <MJD> (utc|tai)\n')
        sys.exit(1)

    jd_limits, converters = parse()

    mjd = float(sys.argv[1])
    mjd_in = sys.argv[2]
    if(mjd_in.lower() == 'utc'):
        res = utc_to_tai(mjd, jd_limits, converters)
        res_in = 'tai'
    elif(mjd_in.lower() == 'tai'):
        res = tai_to_utc(mjd, jd_limits, converters)
        res_in = 'utc'
    else:
        sys.stderr.write('Usage: utctai.py <MJD> (utc|tai)\n')
        sys.exit(2)
    print('%f %s = %f %s' % (mjd, mjd_in, res, res_in))
    sys.exit(0)





























