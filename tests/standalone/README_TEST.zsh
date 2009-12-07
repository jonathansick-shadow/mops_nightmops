#!/bin/zsh
# In order to run pipeline_test.py you need to setup Python, MySQL libraries and 
# numpy. One way of doing this in the LSST environment is
source $HOME/loadLSST.zsh 
setup python
setup mysqlclient
setup numpy

# Example invocations are (for TALCS)
# ./pipeline_test.py 1 19.594083 8.669111 53992.3861186
# 
# or, to execute the same thing on several CPUs use
# ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 16 0
# ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 16 1
# ...
# ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 16 15
# on the 16 CPUs you want to use.
# 
# 
# Same thing but for CFHT-LS:
# ./pipeline_test.py fpierfed_cfhtls 1 36.501250 -4.503611 52900.519295 1 0
# 
# and similar for the simulates SMP...

