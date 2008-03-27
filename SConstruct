# -*- python -*-
#
# Setup our environment
#
import glob, os.path
import lsst.SConsUtils as scons

env = scons.makeEnv("mops",
                    r"$HeadURL$",
                    [])

#
# Build/install things
#
# ........................ NEED TO ADD tests/SConscript.............#
for d in Split('include/lsst/mops python/lsst/mops'):
    SConscript(os.path.join(d, 'SConscript'))

env['IgnoreFiles'] = r"(~$|\.pyc$|^\.svn$|\.o$)"

Alias("install", env.Install(env['prefix'], "python"))
Alias("install", env.Install(env['prefix'], "pipeline"))
Alias("install", env.InstallEups(env['prefix'] + "/ups", glob.glob("ups/*.table")))

scons.CleanTree(r"*~ core *.so *.os *.o")

env.Declare()
env.Help("""
LSST Moving Object Pipeline packages
""")

