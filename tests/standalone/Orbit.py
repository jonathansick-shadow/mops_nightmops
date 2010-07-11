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

import numpy


class Orbit(object):
    """
    orbitId
    q
    e
    i
    node
    argPeri
    timePeri
    epoch
    hv
    g
    src
	"""
    def __init__(self, movingObjectId, movingObjectVersion, 
                 q, e, i, node, argPeri, timePeri, epoch, 
                 hv, g,
                 src=None):
        """
        movingObjectId: integer, ID of obj associated with this Orbit
        movingObjectVersion: version of the obj associated with this Orbit
        q (AU)
        e
        i (deg)
        node (deg)
        argPeri (deg)
        timePeri (UTC MJD)
        epoch: orbit epoch (UTC MJD)
        hv: absolute magnitude (V mag)
        g: slope parameter
        src: 21 element array (covariance matrix in diagonal form).
        """
        self.movingObjectId = movingObjectId
        self.movingObjectVersion = movingObjectVersion
        self.q = q
        self.e = e
        self.i = i
        self.node = node
        self.argPeri = argPeri
        self.timePeri = timePeri
        self.epoch = epoch
        self.hv = hv
        self.g = g
        self.src = self.setSrc(src)
        return


    def setSrc(self, src):
        """
        If all elements of the covariance list are not None, then cast that
        list into a numpy.array. Return the casted array or None in case the
        covariance is invalid (i.e. has null elements).
        """
        if(None in src):
            return(None)
        return(numpy.array([float(e) for e in src]))





