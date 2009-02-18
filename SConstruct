# -*- python -*-
#
# Setup our environment
#
import glob, os.path, re, sys
import lsst.SConsUtils as scons

dependencies = ["boost",
                "python",
                "cfitsio",
                "wcslib",
                "pex_exceptions",
                "utils",
                "daf_base",
                "pex_logging",
                "pex_policy",
                "security",
                "daf_persistence",
                "daf_data",
                "afw"]

env = scons.makeEnv(
    "mops",
    r"$HeadURL: svn+ssh://svn.lsstcorp.org/DMS/mops/trunk/SConstruct $",
    [
        ["boost", "boost/cstdint.hpp"],
        ["boost", "boost/test/unit_test.hpp", "boost_unit_test_framework:C++"],
        ["boost", "boost/serialization/base_object.hpp", "boost_serialization:C++"],
        ["python", "Python.h"],
        ["cfitsio", "fitsio.h", "m cfitsio", "ffopen"],
        ["wcslib", "wcslib/wcs.h", "m wcs"], # remove m once SConsUtils bug fixed
        ["pex_exceptions", "lsst/pex/exceptions.h", "pex_exceptions:C++"],
        ["utils", "lsst/utils/Utils.h", "utils:C++"],
        ["daf_base", "lsst/daf/base.h", "daf_base:C++"],
        ["pex_logging", "lsst/pex/logging/Trace.h", "pex_logging:C++"],
        ["pex_policy", "lsst/pex/policy/Policy.h", "pex_policy:C++"],
        ["security", "lsst/security/Security.h", "security:C++"],
        ["daf_persistence", "lsst/daf/persistence.h", "daf_persistence:C++"],
        ["daf_data", "lsst/daf/data.h", "daf_data:C++"],
        ["afw", "lsst/afw/formatters/Utils.h", "afw:C++"],
    ]
)

env.Help("""
LSST Moving Object Pipeline packages
""")

###############################################################################
# Boilerplate below here.  Do not modify.

pkg = env["eups_product"]
env.libs[pkg] += env.getlibs(" ".join(dependencies))

#
# Build/install things
#
for d in Split("lib python/lsst/" + re.sub(r'_', "/", pkg) + " tests"):
    try:
        SConscript(os.path.join(d, "SConscript"))
    except Exception, e:
        print >> sys.stderr, "%s: %s" % (os.path.join(d, "SConscript"), e)

env['IgnoreFiles'] = r"(~$|\.pyc$|^\.svn$|\.o$)"

Alias("install", [env.Install(env['prefix'], "python"),
                  env.Install(env['prefix'], "include"),
                  env.Install(env['prefix'], "lib"),
                  env.Install(env['prefix'], "python"),                  
                  env.InstallAs(os.path.join(env['prefix'], "doc", "doxygen"),
                                os.path.join("doc", "htmlDir")),
                  env.InstallEups(env['prefix'] + "/ups")])

scons.CleanTree(r"*~ core *.so *.os *.o")

#
# Build TAGS files
#
files = scons.filesToTag()
if files:
    env.Command("TAGS", files, "etags -o $TARGET $SOURCES")

env.Declare()