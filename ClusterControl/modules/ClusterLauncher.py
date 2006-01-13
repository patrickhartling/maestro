# Copyright (C) Infiscape Corporation 2006

import sys
from PyQt4 import QtGui, QtCore
import ClusterLauncherBase
import ClusterLauncherResource
import elementtree.ElementTree as ET
import ClusterModel
#class ClusterTableModel(QAbstractTableModel):
#   pass

class ClusterLauncher(QtGui.QWidget, ClusterLauncherBase.Ui_ClusterLauncherBase):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)

      self.apps    = []
      self.actions = []
      self.globaloptions = []

      # State information for the selected application.
      self.selectedApp         = None
      self.commandOptions      = []
      self.selectedAppOptions  = {}
      self.appSpecificChildren = []
      self.actionDict          = {}   # Storage for user-defined action slots
      self.activeThread        = None

   def configure(self, clusterModel):
      self.mClusterModel = clusterModel
      self.xmlTree = clusterModel.mElement
      top_element = self.xmlTree.find("./launcher")
      assert top_element.tag == "launcher"

      for app_elt in top_element.findall("./applications/app"):
         self.apps.append(Application(app_elt))

      for action_elt in top_element.findall("./controls/action"):
         self.actions.append(Action(action_elt))

      for n in top_element.findall("./global_options/option"):
         self.globaloptions.append(AppOption(n))
      for n in top_element.findall("./global_options/group"):
         self.globaloptions.append(AppExclusiveOption(n))

      self._fillInApps()
      self._fillInControls()

   def _fillInApps(self):
      """ Fills in the application panel. """
      self.appComboBox.clear()
   
      for app in self.apps:
         #self.appComboBox.insertItem(app.getName())
         self.appComboBox.addItem(app.getName())
   
      if len(self.apps) > 0:
         self.appComboBox.setCurrentIndex(0)
         self._setApplication(0)
      else:
         print "ERROR: No applications defined!"
         QApplication.exit(0)

   def _setApplication(self, id):
      if self.selectedApp != None:
         self._resetAppState()
         
      self.selectedApp = id
      app = self.apps[id]
      # XXX:
      #self.statusBar().message(app.getTip())
      self.appComboBox.setToolTip(self.tr(str(app.getTip())))

      # Ensure that the "Help" button is only enabled when the current
      # application has a help URL.
      if app.getHelpURL() == None:
         self.helpButton.setEnabled(False)
      else:
         self.helpButton.setEnabled(True)

      app_opts = app.getOptions()
      all_opts = []
      all_opts.extend(self.globaloptions)
      all_opts.extend(app_opts)

      for i in range(0, len(all_opts)):
         opt = all_opts[i]

         if isinstance(opt, AppExclusiveOption):
            group = QtGui.QGroupBox(str(opt.group_name), self.mAppFrame)
        
            group_layout = QtGui.QVBoxLayout(group)
            group_layout.setMargin(9)
            group_layout.setSpacing(6)
            group_layout.setObjectName("group_layout")
            group.setLayout(group_layout)
            
            for o in opt.options:
               rb = QtGui.QRadioButton(str(o.label), group)

               rb.setEnabled(o.enabled)
               rb.setChecked(o.selected)
               group_layout.addWidget(rb)
               self.connect(rb, QtCore.SIGNAL("clicked()"), self.onOptionBox)
               self.selectedAppOptions[rb] = o

               if o.tip != None and o.tip != "":
                  rb.setToolTip(self.tr(str(o.tip)))

            self.vboxlayout1.insertWidget(i + 1, group)
            self.appSpecificChildren.append(group)

            # This is critical for making the layout update dynamically.
            # http://mats.gmd.de/pipermail/pykde/2001-March/000932.html
            group.show()
         else:
#            print "Adding checkbox %i labeled '%s'" % (i, opt.tip)
            cb = QtGui.QCheckBox(str(opt.label), self.mAppFrame)
            cb.setObjectName("checkbox" + str(i))
            cb.setEnabled(opt.enabled)
            cb.setChecked(opt.selected)

            self.mAppFrame.layout().insertWidget(i + 1, cb)
            self.connect(cb, QtCore.SIGNAL("clicked()"), self.onOptionBox)
            self.selectedAppOptions[cb] = opt
            self.appSpecificChildren.append(cb)

            # This is critical for making the layout update dynamically.
            # http://mats.gmd.de/pipermail/pykde/2001-March/000932.html
            cb.show()

            if opt.tip != None and opt.tip != "":
               cb.setToolTip(self.tr(str(opt.tip)))

      # Forcibly populate self.commandOptions so that anything that is selected
      # by default will show up in the list.
      self._setCommandOptions()

   def _resetAppState(self):
      """ Resets the information associated with the selected application. """
      for w in self.appSpecificChildren:
         self.mAppFrame.layout().removeWidget(w)
         w.deleteLater()

      self.commandOptions      = []
      self.selectedApp         = None
      self.selectedAppOptions  = {}
      self.appSpecificChildren = []


   def _fillInControls(self):
      """ Fills in the controls panel. """

      for i in range(0, len(self.actions)):
         a = self.actions[i]

         button = QtGui.QPushButton(self.cmdFrame)
         button.setObjectName("button" + str(i))
         button.setText(str(a.name))

         self.cmdFrame.layout().insertWidget(i + 3, button)
         self.actionDict[button] = lambda action=a: self.onCommandButton(action)
         self.connect(button, QtCore.SIGNAL("clicked()"), self.actionDict[button])

         if a.tip != None and a.tip != "":
            button.setToolTip(self.tr(str(a.tip)))

   def fileExit(self):
      QApplication.exit(0)

   def appSelect(self):
     self._setApplication(self.appComboBox.currentIndex())

   def loadHelp(self):
      help = helpdialog.HelpDialog(self)
      help.setHelpURL(self.apps[self.selectedApp].getHelpURL())
      help.show()

   def onOptionBox(self):
      self.commandOptions = []
      self._setCommandOptions()

   def _setCommandOptions(self):
      for w, opt in self.selectedAppOptions.items():
         if w.isChecked():
            self.commandOptions.append(opt.flag)
#      print self.commandOptions

   def onCommandButton(self, action):
      if action.command != "" and action.command != None:
         self._runCommandWithLog(action.command)
      else:
         assert "This should never happen"

   def onKillApp(self):
      self.mClusterModel.killCommand()
      #self.launchButton.setEnabled(True)
      #self.killButton.setEnabled(False)

   def launchApp(self):
      """ Invoked when the built-in Launch button is clicked. """
      cmd = self.apps[self.selectedApp].getCommand()
      
      # Construct the list of options as a single string.
      opts = ""
      for o in self.commandOptions:
         opts += " " + o
      cmd = cmd + opts

      if cmd != "" and cmd != None:
         print "running command: ", cmd
         self.mClusterModel.runRemoteCommand(cmd, cmd)
#         self.mClusterModel.runRemoteCommand('rpm -qa', 'rpm -qa')
         #self.launchButton.setEnabled(False)
         #self.killButton.setEnabled(True)
      else:
         assert "This should never happen"

   def setupUi(self, widget):
      ClusterLauncherBase.Ui_ClusterLauncherBase.setupUi(self, widget)
      self.mTitleLbl.setBackgroundRole(QtGui.QPalette.Mid)
      self.mTitleLbl.setForegroundRole(QtGui.QPalette.Shadow)
      
      #self.connect(self.fileExitAction,QtCore.SIGNAL("activated()"),self.fileExit)
      self.connect(self.appComboBox,QtCore.SIGNAL("activated(int)"),self.appSelect)
      self.connect(self.launchButton,QtCore.SIGNAL("clicked()"),self.launchApp)
      self.connect(self.killButton,QtCore.SIGNAL("clicked()"),self.onKillApp)
      #self.connect(self.helpButton,QtCore.SIGNAL("clicked()"),self.loadHelp)
      
      self.icon = QtGui.QIcon(":/linux2.png")

   def getName():
        return "Cluster Launcher"
   getName = staticmethod(getName)

class AppOption:
   """ Encapsulation of command-line options that may be passed to apps. """
   def __init__(self, xmlElt):
      self.label = xmlElt.get("label")
      self.flag  = xmlElt.get("flag")
      self.tip   = xmlElt.get("tooltip")

      enabled = xmlElt.get("enabled")

      if enabled == "" or enabled == None:
         self.enabled = True
      elif enabled == "true" or enabled == "1":
         self.enabled = True
      else:
         self.enabled = False

      selected = xmlElt.get("selected")

      if selected == "" or selected == None:
         self.selected = False
      elif selected == "true" or selected == "1":
         self.selected = True
      else:
         self.selected = False

class AppExclusiveOption:
   def __init__(self, xmlElt):
      self.group_name = xmlElt.get("name")
      self.options = []

      print "AppExclusiveOption name=", self.group_name

      opts = xmlElt.findall("./option")
      for o in opts:
         self.options.append(AppOption(o))

class Application:
   """ Representation of an application that can be launched. """

   def __init__(self, xmlElt):
      self.name = xmlElt.get("name")

      # Could this be any uglier?  I need to learn the Python XML API better...
      self.command = xmlElt.find("./command").text

      help_elts = xmlElt.findall("./helpURL")
      if None != help_elts and len(help_elts) > 0 and help_elts[0].text:
         self.helpURL = help_elts[0].text
      else:
         self.helpURL = None

      tip = self.name  # Fallback in case no tooltip is defined

      tip_elts = xmlElt.findall("./tooltip")
      if None != tip_elts and len(tip_elts) > 0:
         tip = tip_elts[0].text

      self.tip = tip

      self.options = []
      options_elts = xmlElt.findall("./options")
      if None != options_elts and len(tip_elts) > 0:
         option_list = options_elts[0]

         for n in option_list.findall("./option"):
            self.options.append(AppOption(n))
         for n in option_list.findall("./group"):
            self.options.append(AppExclusiveOption(n))
      
   def getName(self):
      return self.name

   def getCommand(self):
      return self.command

   def getTip(self):
      return self.tip

   def getHelpURL(self):
      return self.helpURL

   def getOptions(self):
      return self.options

class Action:
   """
   Representation of user-defined action buttons displayed in the controls
   panel.
   """
   def __init__(self, xmlElt):
      self.name    = xmlElt.get("name")
      self.command = xmlElt.findall("./command")[0].text

      tip = xmlElt.findall("./tooltip")[0].text

      if tip == "" or tip == None:
         tip = self.name

      self.tip = tip

   def getName(self):
      return self.name

   def getTip(self):
      return self.tip


def getModuleInfo():
   icon = QtGui.QIcon(":/ClusterLauncher/images/launch2.gif")
   return (ClusterLauncher, icon)

def main():
   try:
      app = QtGui.QApplication(sys.argv)
      tree = ET.ElementTree(file=sys.argv[1])
      cluster_config = ClusterModel.ClusterModel(tree);
      cs = ClusterLauncher()
      cs.configure(cluster_config)
      cs.show()
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
