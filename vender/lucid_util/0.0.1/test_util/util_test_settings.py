# Settings for util tests
#
import os, os.path, sys
pj = os.path.join
import util.plugin

data_dir = os.path.normpath(pj(os.path.dirname(__file__), "test_data"))
plugin_test_dir = pj(data_dir, "plugin_test_dir")


# Interfaces
class IPlugTwo(util.plugin.Plugin):
   """ Simple interface for querying. """
   def getValue(self):
      pass
