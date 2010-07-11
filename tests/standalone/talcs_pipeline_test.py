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

import os
import sys
import time



if(len(sys.argv) not in (2, 3)):
    sys.stderr.write('usage: talcs_pipeline_test.py <talcs_log> <num_lines>\n')
    sys.exit(1)
obs_log = sys.argv[1]
try:
    num_lines = int(sys.argv[2])
except:
    num_lines = None

# Read RA, Dec and MJD from obslog. Remember to skip the header (1st line).
in_file = open(obs_log)
header = in_file.readline()

i = 0
ok = 0
not_ok = 0
all_times = []
line = in_file.readline()
while(line and ((num_lines and i < num_lines) or num_lines == None)):
    i += 1
    (ra, dec, t, filter, mjd) = line.strip().split()
    
    t0 = time.time()
    err = os.system('./pipeline_test.py %d %s %s %s' %(i, ra, dec, mjd))
    all_times.append(time.time() - t0)
    
    if(err):
        not_ok += 1
    else:
        ok += 1
    
    # Next!
    line = in_file.readline()
all_times.sort()
if(i):
    print('Fastest: %.02f' %(all_times[0]))
    print('Slowest: %.02f' %(all_times[-1]))
    print('Average: %.02f' %(sum(all_times) / float(i)))
    print('Total:   %.02f' %(sum(all_times)))
    print('OK:      %d' %(ok))
    print('Not OK:  %d' %(not_ok))








