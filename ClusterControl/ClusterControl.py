# Copyright (C) Infiscape Corporation 2006

import sys, os, os.path, time, traceback
pj = os.path.join

from qt import *
import ClusterControlBase

import modules

gui_base_dir = ""
try:
   gui_base_dir = os.path.dirname(os.path.abspath(__file__))
except:
   gui_base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

print "Base gui dir:", gui_base_dir


class ClusterControl(ClusterControlBase.ClusterControlBase):
   def __init__(self,parent = None,name = None,fl = 0):
      ClusterControlBase.ClusterControlBase.__init__(self,parent,name,fl)


      ### Start
      mStatusWindow = QDockWindow(QDockWindow.InDock, self)
      mStatusWindow.setOrientation(Qt.Horizontal)
      mStatusWindow.setHorizontallyStretchable(True)
      mStatusWindow.setVerticallyStretchable(True)
      mStatusWindow.setResizeEnabled(True);
      mStatusWindow.setCloseMode( QDockWindow.Always );
      mStatusWindow.setNewLine(True)
      mStatusWindow.setCaption(self.__tr("Status Panel"))

      self.mStatusTabPanel = QTabWidget(mStatusWindow,"mStatusTabPanel")
      mStatusWindow.setWidget(self.mStatusTabPanel)

      self.setDockEnabled( mStatusWindow, Qt.DockTop, False);
      self.moveDockWindow( mStatusWindow, Qt.DockBottom );

      self.mStatusTabPanel.setGeometry(QRect(90,130,139,62))

      self.tab = QWidget(self.mStatusTabPanel,"tab")
      self.mStatusTabPanel.insertTab(self.tab,QString.fromLatin1(""))

      self.tab_2 = QWidget(self.mStatusTabPanel,"tab_2")
      self.mStatusTabPanel.insertTab(self.tab_2,QString.fromLatin1(""))


      # Load custom modules
      self.mPlugins = {}             # Dict of plugins: mod_name -> (module, ..)
      self.mModulePanels = []
      self.mModuleButtons = []
      self.buildGUI()

      # Call local language change.
      # XXX: In the future we should remove the call in the base class.
      self.languageChange()


   def languageChange(self):
      ClusterControlBase.ClusterControlBase.languageChange(self)
      #self.setCaption(self.__tr("Form1"))
      self.mStatusTabPanel.changeTab(self.tab,self.__tr("Tab 1"))
      self.mStatusTabPanel.changeTab(self.tab_2,self.__tr("Tab 2"))

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
         #self.mStack.removeChild(f)
      self.mModuleButtons = []
      self.mToolbox.layout().removeItem(self.mToolboxSpacer)

   def buildGUI (self):
      self.scanAndLoadPlugins()         # Scan the set of plugins we have
      self.loadModulePlugins()            # Find and load any view plugins
      self.mToolboxSpacer = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
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
               print "Opening view: ", module_class.__name__
            
               # Create module
               new_module = module_class(self.mStack)
               # Keep track of widgets to remove them later
               self.mModulePanels.append(new_module)
               self.mStack.addWidget(new_module, num)

               btn = QToolButton(self.mToolbox, "Module Button")
               self.mToolbox.insert(btn, num)
               num = num + 1

               #self.connect(self.mToolbox,SIGNAL("buttonClicked(int)"),self.mStack.raiseWidget)
               #self.connect(self.mToolbox,SIGNAL("clicked(int)"),self.test)

               btn.setIconSet(QIconSet(new_icon))
               btn.setAutoRaise(1)
               self.mToolbox.layout().addWidget(btn)

               # Keep track of widgets to remove them later
               self.mModuleButtons.append(btn)

            except Exception, ex:
               view_name = "Unknown"
               #if module_class:
               #   pass
                  #view_name = module_class.getName()
               #if new_module:
                  #new_module.destroy()
                  #new_module = None
               err_text = "Error loading view:" + view_name + "\n  exception:" + str(ex)
               print err_text
               traceback.print_exc()
               #error_dialog = pyglui.dialogs.StdDialog("Exception: View Load Failed", err_text)         
               #error_dialog.doModal()

   def __tr(self,s,c = None):
      return qApp.translate("MainWindow",s,c)

if __name__ == "__main__":
   a = QApplication(sys.argv)
   QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
   w = ClusterControl()
   a.setMainWidget(w)
   w.show()
   a.exec_loop()
