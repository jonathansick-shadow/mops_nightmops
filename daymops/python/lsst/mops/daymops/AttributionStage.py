"""
BASIC SCENARIO

System gets
1. a list of (NOT LINKED AND NOT ATTRIBUTED AND NOT PRECOVERED) Tracklets 
   belonging to the same night
2. the list of all NOT MERGED MovingObjects
3. the list of (RA, Dec, MJD, FieldRadius) of ScienceCCDExposures of the same 
   night as input 1.
4. the MPC OBSCODE of the observatory location
as input.

For each (RA, Dec, MJD, FieldRadius) in the input list 2:
  A. System invokes "Compute Orbit-Field of View Intersection" use case and 
     receives the appropriate subset of the input list of MovingObjects.
  B. For each Moving object in the list from step A:
    B.1. System invokes "Compute Precise Ephemeris" use case and receives the 
         list of predicted ephemeris (i.e. RA, Dec, mag, ErrorEllipse) for the 
         input MovingObject and MJD.
  C. System identifies most likely matches between the aggregated ephemeris list
     and the input list of Tracklets (by invoking "Identify Best DIASource 
     Match").
  D. System invokes "Orbit Determination" use case and recetives the list of 
     newly improved MovingObjects.
  E. System updates the system-level MovingObjects modified in step D (e.g. in 
     the database) with their new parameters.
  F. System markes MovingObjects from step E. as ATTRIBUTED.
  G. System flags the subset of the input Tracklets that were associated to 
     input MovingObjects in step F. as "LINKED".


Policy
  1. MPC observatory OBSCODE
  2. FieldProximity config
  3. OrbitDetermination config
  4. Database name and location

Input
  1. a list of (NOT LINKED AND NOT ATTRIBUTED AND NOT PRECOVERED) Tracklets 
     belonging to the same night
  2. the list of all NOT MERGED MovingObjects
  3. the list of (RA, Dec, MJD, FieldRadius) of ScienceCCDExposures of the same 
     night as input 1.

Output
  1. None/error code?

Side Effects
  DB Inserts
    1. None
  DB Updates
    1. Tracklet status -> LINKED
    2. MovingOject status -> ATTRINUTED
  DB Deletes
    1. None
"""
from DayMOPSStage import DayMOPSStage
from DiaSource import DiaSource
from DiaSourceList import DiaSourceList
import linking

import time




class AttributionStage(DayMOPSStage):
    def __init__(self, stageId=-1, policy=None):
        """
        Standard Stage initializer.
        """
        super(AttributionStage, self).__init__(stageId, policy)
        
        # Read the configuration from policy.
        self.obsCode = self.getValueFromPolicy('obsCode')
        self.residThreshold = self.getValueFromPolicy('residThreshold')
        self.maxSearchRadius = self.getValueFromPolicy('maxSearchRadius')
        self.minSearchRadius = self.getValueFromPolicy('minSearchRadius')
        self.maxArclengthForIod = self.getValueFromPolicy('maxArclengthForIod')
        self.uncertaintySigma = self.getValueFromPolicy('uncertaintySigma')
        self.dbLocStr = self.getValueFromPolicy('database')
        return
    
    
    


    

    
    

















