import os,sys,shutil
pj = os.path.join

sys.path.append( pj(os.path.dirname(__file__), "..",".."))

import unittest
import util_test_settings
from util_test_settings import IPlugTwo
import util.plugin


class testPluginManager(unittest.TestCase):
   
   def setUp(self):
      self.pluginMgr = util.plugin.PluginManager()
      self.progress = []      
      
   def tearDown(self):
      if self.pluginMgr:
         self.pluginMgr.unloadAll()
         self.pluginMgr = None

   def catchProgress(self, percent, message):
      self.progress.append( [percent, message] )
      
   def testBasicLoading(self):
      self.pluginMgr.scan([util_test_settings.plugin_test_dir,], self.catchProgress)
      
      self.assert_(len(self.progress) != 0)
      self.assert_(self.progress[-1][0] == 1.0)
      
      # Make sure the plugins that should load actually loaded
      # - Simple local one
      # - Package based one.
      plugins = self.pluginMgr.getPlugins(returnNameDict=True)
      
      known_plugins = ["plugin_one.PluginOne","is_package.plugin_one.PluginOne",
                       "is_package.PkgPlugin","is_package.pluginA.PluginA",
                       "plugin_two.PluginA","plugin_two.PluginB","plugin_two.PluginC",
                       "is_package.another_pkg.PkgPlugin"]
      for x in known_plugins:
         self.assert_(plugins.has_key(x))
      
      # Make sure nothing loaded from not_package
      for x in plugins.iterkeys():
         self.failIf("not_package" in x)

      # Test query with prefix
      plugin_two_plugins = self.pluginMgr.getPlugins(pluginPrefix="plugin_two",returnNameDict=True)
      for x in plugin_two_plugins.iterkeys():
         self.assert_(x.startswith("plugin_two"))
      
   
   def testCallingLoadedPlugin(self):
      self.pluginMgr.scan([util_test_settings.plugin_test_dir,])
      
      plugins = self.pluginMgr.getPlugins(pluginPrefix="plugin_one",returnNameDict=True)
      
      self.assert_(plugins.has_key("plugin_one.PluginOne"))
      plugin_one = plugins["plugin_one.PluginOne"]
      plug_obj = plugin_one()
      
      val = plug_obj.getVal()
      self.assert_(val == 1)
   
   def testQueryByType(self):
      # Query for plugins that implement IPlugTwo
      iplug_two_names = ["plugin_two.PluginA","plugin_two.PluginB"]
      self.pluginMgr.scan([util_test_settings.plugin_test_dir,])

      iplug_two_plugins = self.pluginMgr.getPlugins(plugInType=IPlugTwo, returnNameDict=True)
      
      self.assert_(len(iplug_two_plugins) == 2)
      for n in iplug_two_names:
         self.assert_(iplug_two_plugins.has_key(n))
   
   def testReloading(self):
      # This tests reloading a module with a change to a plugin
      # We use the module "plugin_swap.py" and we copy it's contents
      # from two other files during runtime.  The plugin defined in
      # the module returns a different value depending upon which is loaded
      plugin_mod   = pj(util_test_settings.plugin_test_dir,"plugin_swap.py")
      plugin_mod_a = pj(util_test_settings.plugin_test_dir,"plugin_swap_A.pynot")
      plugin_mod_b = pj(util_test_settings.plugin_test_dir,"plugin_swap_B.pynot")
      
      # Remove old plugin and copy over A
      if os.path.exists(plugin_mod):
         os.remove(plugin_mod)
      shutil.copy(plugin_mod_a, plugin_mod)

      # Scan and make sure plugin is there
      self.pluginMgr.scan([util_test_settings.plugin_test_dir,])
      
      plugins = self.pluginMgr.getPlugins(pluginPrefix="plugin_swap")
      self.assert_(len(plugins) == 1)
      
      swap_a = plugins[0]()
      self.assert_(swap_a.getId() == "A")
      
      # Now reload and test
      os.remove(plugin_mod)
      shutil.copy(plugin_mod_b, plugin_mod)
      self.pluginMgr.reload()
      
      # Test old obj instance
      self.assert_(swap_a.getId() == "B")
      
      # Test old plugin class ref
      # - This will still be to the old class, so we will get an old plugin
      swap_b = plugins[0]()
      self.assert_(swap_b.getId() == "A")
      
      # Test new plugin instance
      plugins = self.pluginMgr.getPlugins(pluginPrefix="plugin_swap")
      self.assert_(len(plugins) == 1)
      swap_b = plugins[0]()
      self.assert_(swap_b.getId() == "B")


   def testRescan(self):
      # Test that we can rescan the directory to pick up "new" plugins      
      plugin_mod   = pj(util_test_settings.plugin_test_dir,"plugin_swap.py")
      plugin_mod_a = pj(util_test_settings.plugin_test_dir,"plugin_swap_A.pynot")
      
      # Remove old plugin for first scan
      if os.path.exists(plugin_mod):
         os.remove(plugin_mod)
         
      self.pluginMgr.scan([util_test_settings.plugin_test_dir,])
      plugins = self.pluginMgr.getPlugins(returnNameDict=True)
      for x in plugins.iterkeys():
         self.failIf(x.startswith("plugin_swap"))
      
      # Copy one over now
      shutil.copy(plugin_mod_a,plugin_mod)
      
      self.pluginMgr.scan([util_test_settings.plugin_test_dir,])
      plugins = self.pluginMgr.getPlugins(pluginPrefix="plugin_swap")
      self.assert_(len(plugins) == 1)


if __name__ == '__main__':
   unittest.main()

