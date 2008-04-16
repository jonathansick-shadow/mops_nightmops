# -*- python -*-
#
# Setup our environment
#
import glob, os.path
import lsst.SConsUtils as scons

env = scons.makeEnv(
    "mops",
    r"$HeadURL$",
    [
        ["boost", "boost/version.hpp", "boost_filesystem:C++"],
        ["boost", "boost/regex.hpp", "boost_regex:C++"],
        ["boost", "boost/serialization/base_object.hpp", "boost_serialization:C++"],
        ["python", "Python.h"],
        ["cfitsio", "fitsio.h", "m cfitsio", "ffopen"],
        ["wcslib", "wcslib/wcs.h", "wcs"],
        ["utils", "lsst/utils/Utils.h", "utils:C++"],
        ["daf_base", "lsst/daf/base.h", "daf_base:C++"],
        ["pex_exceptions", "lsst/pex/exceptions.h", "pex_exceptions:C++"],
        ["pex_logging", "lsst/pex/logging/Trace.h", "pex_logging:C++"],
        ["security", "lsst/security/Security.h", "security:C++"],
        ["pex_policy", "lsst/pex/policy/Policy.h", "pex_policy:C++"],
        ["daf_persistence", "lsst/daf/persistence.h", "daf_persistence:C++"],
        ["daf_data", "lsst/daf/data.h", "daf_data:C++"],
        ["afw", "lsst/afw/formatters/Utils.h", "afw:C++"],
    ]
)

#
# Libraries needed to link libraries/executables
#
env.libs["mops"] += env.getlibs("boost wcslib utils daf_base daf_data daf_persistence pex_exceptions pex_logging pex_policy security afw")

#
# Build/install things
#
for d in (
    "include/lsst/mops",
    "lib",
    "python/lsst/mops",
    "tests"
):
    SConscript(os.path.join(d, 'SConscript'))

env['IgnoreFiles'] = r"(~$|\.pyc$|^\.svn$|\.o$)"

Alias("install", [
    env.Install(env['prefix'], "python"),
    env.Install(env['prefix'], "include"),
    env.Install(env['prefix'], "lib"),
    env.Install(env['prefix'], "pipeline"),
    env.InstallEups(os.path.join(env['prefix'], "ups"), glob.glob(os.path.join("ups", "*.table")))
])

scons.CleanTree(r"*~ core *.so *.os *.o")

env.Declare()
env.Help("""
LSST Moving Object Pipeline packages
""")

