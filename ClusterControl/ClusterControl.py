# Copyright (C) Infiscape Corporation 2006

import sys, os, os.path, time, traceback
pj = os.path.join

from PyQt4 import QtGui, QtCore
import ClusterControlBase
import ClusterControlResource
import ClusterConfig
import elementtree.ElementTree as ET

import modules

import Pyro

gui_base_dir = ""
try:
   gui_base_dir = os.path.dirname(os.path.abspath(__file__))
except:
   gui_base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

print "Base gui dir:", gui_base_dir


class ClusterControl(QtGui.QMainWindow, ClusterControlBase.Ui_ClusterControlBase):
   def __init__(self, parent = None):
      QtGui.QMainWindow.__init__(self, parent)
      self.setupUi(self)

   def configure(self, clusterConfig):
      for module in self.mModulePanels:
         module.configure(clusterConfig)
      
      clusterConfig.getOutputLogger().subscribeMatch(".*", self.mTextEdit.append)


   def setupUi(self, widget):
      ClusterControlBase.Ui_ClusterControlBase.setupUi(self, widget)

      self.mToolboxButtonGroup = QtGui.QButtonGroup()
      widget.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.mStatusWindow)

      # Load custom modules
      self.mPlugins = {}             # Dict of plugins: mod_name -> (module, ..)
      self.mModulePanels = []
      self.mModuleButtons = []
      self.buildGUI()

   def reloadModules(self):
      """ Reload the entire GUI and all class code for it (ie. modules). """
      self.tearDownGUI()
      #self.reloadGUIModules()
      #self.buildGUI()

   def reloadGUIModules(self):
      """ Reload any GUI related modules. """
      print "Reloading all GUI related modules:"
      try:
         reload(modules)
      except Exception, ex:
         print "Exception reloading gui modules:\n", ex

   def tearDownGUI(self):
      for f in self.mModulePanels:
         self.mStack.removeWidget(f)
         self.mStack.removeChild(f)
      self.mModulePanels = []
      for b in self.mModuleButtons:
         self.mToolbox.removeChild(b)
         self.mToolboxButtonGroup.removeButton(btn)
      self.mModuleButtons = []
      self.mToolbox.layout().removeItem(self.mToolboxSpacer)

   def buildGUI (self):
      self.scanAndLoadPlugins()         # Scan the set of plugins we have
      self.loadModulePlugins()            # Find and load any view plugins
      self.mToolboxSpacer = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
      self.mToolbox.layout().addItem(self.mToolboxSpacer)


   def scanAndLoadPlugins(self):
      """ Scan for plugins in the sub-dirs.  Do initial import as well.
          Recursively scans sub directories looking for "plugin" modules 
         to add to the gui.
      """
      def get_mods(mod_list, dirpath, namelist):
         """ Given a dirpath and list of files in that directory, add all files
             ending in .py to the existing mod_list. """
         mod_list.extend( [pj(dirpath,n) for n in namelist if n.endswith('.py')])

      # XXX: Need better way to find the plugins
      print "Scanning for plugins..."
      mod_list = []
      base_plugin_dir = os.path.join(gui_base_dir,'modules')
      if not os.path.isdir(base_plugin_dir):
         print "Error: plugin dir does not exist: ", base_plugin_dir
         return

      os.path.walk(base_plugin_dir, get_mods, mod_list)

      mod_list = [x for x in mod_list if x.find("__init__") == -1]   # Remove __init__.py files
      mod_list = [x.replace(gui_base_dir,"") for x in mod_list]      # Remove the gui base dir part: view/thing.py
      mod_list = [x.replace(os.sep,".")[:-3] for x in mod_list]      # Replace / with .: .view.thing
      mod_list = [x.lstrip('.') for x in mod_list]                   # strip off the last . : view.thing

      print "   found modules:"
      for m in mod_list:
         print " "*6, m,
         try:
            if not self.mPlugins.has_key(m):        # New module, so import
               print "   importing...",
               __import__(m)
               new_mod = sys.modules[m]             # Must do this way to handle package.mod case correctly (???)
               self.mPlugins[m] = (new_mod,None)
            else:                                   # Existing module, so reload
               print "   reloading...",
               reload(self.mPlugins[m][0])
            print " "*3, "[OK]"
         except Exception, ex:
            print " "*3, "[FAILED]"
            if self.mPlugins.has_key(m):
               del self.mPlugins[m]
            print "Error loading module: [%s] deleting it."%(m,)
            print "   exception:", ex
            traceback.print_exc()

   def loadModulePlugins(self):
      # Find all the view plugin classes
      self.mModulePanels = []
      self.mModuleButtons = []
      num = 0
      for p in self.mPlugins.items():
         mod_name = p[0]
         mod = p[1][0]
         if hasattr(mod,'getModuleInfo'):    # If it has view classes registered
            mod_info = mod.getModuleInfo()
            module_class = None
            new_module = None
            new_icon = None
            try:
               module_class = mod_info[0]
               new_icon = mod_info[1]
               size = QtCore.QSize()
               print "ICON:", new_icon.actualSize(size)
               if None == new_icon:
                  new_icon = QtGui.QIcon(":/construction.png")
               print "Opening view: ", module_class.__name__
            
               # Create module
               new_module = module_class()

               # Keep track of widgets to remove them later
               self.mModulePanels.append(new_module)
               #self.mStack.addWidget(new_module, num)
               index = self.mStack.addWidget(new_module)

               btn = QtGui.QToolButton(self.mToolbox)
               btn.setIcon(new_icon)
               btn.setAutoRaise(1)
               btn.setCheckable(True)
               btn.setMinimumSize(QtCore.QSize(40,40))
               btn.setIconSize(QtCore.QSize(40,40))
               self.mToolbox.layout().addWidget(btn)
               self.mToolboxButtonGroup.addButton(btn, index)

               #self.mToolbox.addWidget(btn)
               #self.mToolbox.insert(btn, num)
               num = num + 1

               QtCore.QObject.connect(self.mToolboxButtonGroup,QtCore.SIGNAL("buttonClicked(int)"),self.mStack.setCurrentIndex)
               #QtCore.QObject.connect(self.mToolboxButtonGroup,QtCore.SIGNAL("buttonClicked(int)"),self.test)
               #self.connect(self.mToolbox,SIGNAL("clicked(int)"),self.test)


               # Keep track of widgets to remove them later
               self.mModuleButtons.append(btn)

            except Exception, ex:
               view_name = "Unknown"
               if module_class:
                  view_name = module_class.getName()
               if new_module:
                  #new_module.destroy()
                  new_module = None
               err_text = "Error loading view:" + view_name + "\n  exception:" + str(ex)
               print err_text
               traceback.print_exc()
               #error_dialog = pyglui.dialogs.StdDialog("Exception: View Load Failed", err_text)         
               #error_dialog.doModal()

      # Set the default button to display
      btn = self.mToolboxButtonGroup.buttons()[0]
      btn.click()
      self.mStack.setCurrentIndex(self.mToolboxButtonGroup.id(btn))

   def test(self, e):
      print e

   def __tr(self,s,c = None):
      return qApp.translate("MainWindow",s,c)

   #def onDebugOutput(self, message):
   #   #self.mTextEdit.append(str(message))
   #   #self.mTextEdit.setText(str(message))
   #   self.mTextEdit.append("Aron")

def main():
   Pyro.config.PYRO_LOGFILE = 'Pyro_sys_log'
   Pyro.config.PYRO_USER_LOGFILE = 'Pyro_user_log'
   Pyro.config.PYRO_TRACELEVEL = 4
   Pyro.config.PYRO_USER_TRACELEVEL = 4
   try:
      app = QtGui.QApplication(sys.argv)

      # Parse xml config file
      tree = ET.ElementTree(file=sys.argv[1])

      # Create cluster configuration
      cluster_config = ClusterConfig.ClusterConfig(tree);

      # Try to make inital connections
      cluster_config.refreshConnections()

      # Create and display GUI
      cc = ClusterControl()
      cc.configure(cluster_config)
      cc.show()
      sys.exit(app.exec_())
   except IOError, ex:
      print "Failed to read %s: %s" % (sys.argv[1], ex.strerror)

def usage():
   print "Usage: %s <XML configuration file>" % sys.argv[0]

if __name__ == '__main__':
   if len(sys.argv) >= 2:
      main()
   else:
      usage()
