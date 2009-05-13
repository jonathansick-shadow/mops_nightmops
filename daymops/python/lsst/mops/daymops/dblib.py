"""
Simple database-related functions and classes.
"""
import lsst.daf.persistence as persistence

# Supported classes
from MovingObject import MovingObject
from Orbit import Orbit
from Tracklet import Tracklet
from DiaSource import DiaSource



def simpleObjectFetch(dbLocStr, table, className, columns, where=None):
    """
    Fetch relevant rows from a given table and instantiate one object per row.
    It is assumed that the objects to be created have a method called
        setCol_i where col_i is columns[i][0]
    Also, it is essential that one can instantiate the class without passing any
    argument to the constructor. For instance:
        obj = className()
    
    The SQL used is
        select <col1>, <col2>, <col3>[, ...] from table where <where>
    
    Column types are specified together with their names. For instance
        [('trackletId', 'Long'), ('valTot', 'Double'), ...]
    Supported types are those defined in lsst.daf.persistence.
    
    @param dbLocStr: database connection string.
    @param table: the name of the database table to select from.
    @param className: the name of the class to instantiate.
    @param columns: the list of column names, types: [(col1, type1), ...]
    @param where: the where SQL statement.
    
    Return
        [obj1, obj2, ...]
    """
    # Simple sanity check.
    if([c for c in columns if len(c) != 2]):
        raise(Exception('columns must specify both column name and type.'))
    
    if(className not in globals().keys()):
        msg = '%s is not supported yet for simple DB extraction' %(className)
        raise(NotImplementedError(msg))
    
    # Send the query.
    res = []
    db = persistence.DbStorage()
    db.setPersistLocation(persistence.LogicalLocation(dbLocStr))
    db.setTableForQuery(table)
    errs = [db.outColumn(c[0]) for c in columns]
    if(where):
        db.setQueryWhere(where)
    db.query()
    
    # Fetch the results and instantiate the objects.
    while(db.next()):
        res.append(_simpleObjectCreation(db, className, columns))
    db.finishQuery()
    return(res)


def _simpleObjectCreation(db, name, cols):
    """
    This is a bit of black magic, sorry.
    """
    obj = globals()[name]()
    setters = [getattr(obj, 'set%s%s' %(c[0][0].upper(), c[0][1:])) \
               for c in cols]
    fetchers = [getattr(db, 'getColumnByPos%s' %(c[1])) for c in cols]
    
    [setters[cols.index(c)](fetchers[cols.index(c)](cols.index(c))) \
     for c in cols]
    return(obj)


def simpleTwoObjectFetch(dbLocStr, table, className1, columns1, 
                         className2, columns2, where=None):
    """
    Fetch relevant rows from one table and instantiate two objects per row. The
    main use case for this is
        Generate two objects/row from a single table (e.g. MovingObject and
        Orbit from the MovingObject table).
    
    It is assumed that the objects to be created have a method called
        setCol_i where col_i is columns_j[i][0] j=1, 2
    Also, it is essential that one can instantiate the class without passing any
    argument to the constructor. For instance:
        obj = className()
        
    The SQL used is
        select <col1>, <col2>, <col3>[, ...] from table where <where>
    
    Column types are specified together with their names. For instance
        [('trackletId', 'Long'), ('valTot', 'Double'), ...]
    Supported types are those defined in lsst.daf.persistence.
    
    @param dbLocStr: database connection string.
    @param table: the name of the database table to select from.
    @param className1: the name of the first class to instantiate.
    @param className2: the name of the second class to instantiate.
    @param columns1: the list of column names, types for obj1: [(col1, type1), ]
    @param columns2: the list of column names, types for obj2: [(col1, type1), ]
    @param where: the where SQL statement.
    
    Return
        [(obj11, obj21), (obj12, obj22), ...]
    """
    # Simple sanity check.
    if([c for c in columns1+columns2 if len(c) != 2]):
        raise(Exception('columns must specify both column name and type.'))
    
    if(className1 not in globals().keys()):
        msg = '%s is not supported yet for simple DB extraction' %(className1)
        raise(NotImplementedError(msg))
    if(className2 not in globals().keys()):
        msg = '%s is not supported yet for simple DB extraction' %(className2)
        raise(NotImplementedError(msg))
    
    # Send the query.
    res = []
    db = persistence.DbStorage()
    db.setPersistLocation(persistence.LogicalLocation(dbLocStr))
    db.setTableForQuery(table)
    errs = [db.outColumn(c[0]) for c in columns1+columns2]
    if(where):
        db.setQueryWhere(where)
    db.query()
    
    # Fetch the results and instantiate the objects.
    while(db.next()):
        o1 = _simpleObjectCreation(db, className1, columns1)
        o2 = _simpleObjectCreation(db, className2, columns2)
        res.append((o1, o2))
    db.finishQuery()
    return(res)
    
    
    
    
    
    

if(__name__ == '__main__'):
    import sys
    
    tracklets = simpleObjectFetch('mysql://localhost:3306/mops_onelunation',
                                  'mops_Tracklet',
                                  'Tracklet',
                                  [('trackletId', 'Long'),
                                   ('status', 'String'), 
                                   ('velRa', 'Double'), 
                                   ('velDecl', 'Double'),
                                   ('velTot', 'Double')],
                                  where='trackletId < 10')
    for t in tracklets:
        print(t)

    mo_orbs = simpleTwoObjectFetch('mysql://localhost:3306/mops_onelunation',
                                   'MovingObject',
                                   'MovingObject',
                                   [('movingObjectId', 'Long'), 
                                    ('mopsStatus', 'Char'), # bug #807
                                    ('h_v', 'Double'), 
                                    ('g', 'Double'), 
                                    ('arcLengthDays', 'Double')],
                                   'Orbit',
                                   [('q', 'Double'), 
                                    ('e', 'Double'), 
                                    ('i', 'Double'), 
                                    ('node', 'Double'), 
                                    ('argPeri', 'Double'), 
                                    ('timePeri', 'Double'), 
                                    ('epoch', 'Double'), 
                                    ('src01', 'Double'), 
                                    ('src02', 'Double'), 
                                    ('src03', 'Double'), 
                                    ('src04', 'Double'), 
                                    ('src05', 'Double'), 
                                    ('src06', 'Double'), 
                                    ('src07', 'Double'), 
                                    ('src08', 'Double'), 
                                    ('src09', 'Double'), 
                                    ('src10', 'Double'), 
                                    ('src11', 'Double'), 
                                    ('src12', 'Double'), 
                                    ('src13', 'Double'), 
                                    ('src14', 'Double'), 
                                    ('src15', 'Double'), 
                                    ('src16', 'Double'), 
                                    ('src17', 'Double'), 
                                    ('src18', 'Double'), 
                                    ('src19', 'Double'), 
                                    ('src20', 'Double'), 
                                    ('src21', 'Double')],
                                   where='movingObjectId < 10')
    for (mo, orb) in mo_orbs:
        print(mo, orb)
    sys.exit(0)









