#!/bin/bash

MPDHOSTSFILE=$HOME/etc/mpd.hosts
NCPUS=4

mpdboot  --ncpus=$NCPUS --file=$MPDHOSTSFILE

mpirun Pipeline.py

sleep 1s

mpdallexit

