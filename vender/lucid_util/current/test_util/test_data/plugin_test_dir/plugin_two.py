# Define some plugins for testing
# 
import os,sys
import util.plugin
from util_test_settings import IPlugTwo

class PluginA(IPlugTwo):
   def getValue(self):
      return "A"

class PluginB(IPlugTwo):
   def getValue(self):
      return "B"
   
class PluginC(util.plugin.Plugin):
   def getValue(self):
      return "C"
