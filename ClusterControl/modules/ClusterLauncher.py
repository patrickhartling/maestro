# Copyright (C) Infiscape Corporation 2006

import sys
from PyQt4 import QtGui, QtCore
import ClusterLauncherBase
import ClusterLauncherResource
import elementtree.ElementTree as ET
import ClusterModel
#class ClusterTableModel(QAbstractTableModel):
#   pass

def numClassMatches(nodeClassString, subClassString):
   node_classes = nodeClassString.split(",")
   sub_classes = subClassString.split(",")
   print "%s %s" % (node_classes, sub_classes)
   count = 0
   for c in sub_classes:
      if node_classes.count(c) > 0:
         print " -> Match [%s]" % (c)
         count += 1
   return count

def getMaxMatchValue(valueMap, nodeClassString):
   # Keep track of highest matching command.
   max_match_value = None
   max_match = 0

   # Get the number of classes for the node.
   num_node_classes = len(nodeClassString.split(","))

   # For all commmands
   for sub_class, value in valueMap.items():
      # Get the number of classes for the command
      num_value_classes = len(sub_class.split(","))
      # Get the number of matches
      num_matches = numClassMatches(nodeClassString, sub_class)
      # Use the value only if it has the most matches and the
      # number of matches higher then the least descriptive class.
      if num_matches > max_match and (num_matches >= num_value_classes or num_matches >= num_node_classes):
         max_match = num_matches
         max_match_value = value
   return max_match_value

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
      self.mComboBoxes         = {}
      self.appSpecificWidgets  = []
      self.appSpecificLayouts  = []
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

      #for n in top_element.findall("./global_options/option"):
      #   self.globaloptions.append(AppOption(n))
      #for n in top_element.findall("./global_options/group"):
      #   self.globaloptions.append(AppExclusiveOption(n))

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
            hboxlayout = QtGui.QHBoxLayout()
            hboxlayout.setMargin(9)
            hboxlayout.setSpacing(6)
            hboxlayout.setObjectName("hboxlayout")

            lbl = QtGui.QLabel(self.mAppFrame)
            lbl.setObjectName("mCombo1Lbl")
            lbl.setText(opt.group_name)
            hboxlayout.addWidget(lbl)

            group_cb = QtGui.QComboBox(self.mAppFrame)
            hboxlayout.addWidget(group_cb)
            group_cb.setEditable(opt.editable)
               
        
            for c in opt.mChoices:
               group_cb.addItem(c.label)# QtCore.QVariant(c))

            self.vboxlayout1.insertLayout(i + 1, hboxlayout)
            self.appSpecificWidgets.append(group_cb)
            self.appSpecificWidgets.append(lbl)
            self.appSpecificLayouts.append(hboxlayout)
            
            self.connect(group_cb, QtCore.SIGNAL("currentIndexChanged(int)"), self.onComboBox)
            self.mComboBoxes[group_cb] = opt
            #self.connect(group_cb, QtCore.SIGNAL("editTextChanged(QString)"), self.onComboboxChange)

            # This is critical for making the layout update dynamically.
            # http://mats.gmd.de/pipermail/pykde/2001-March/000932.html
            lbl.show()
            group_cb.show()
         else:
#            print "Adding checkbox %i labeled '%s'" % (i, opt.tip)
            label = opt.mChoices[0].label
            cb = QtGui.QCheckBox(str(label), self.mAppFrame)
            cb.setObjectName("checkbox" + str(i))
            cb.setChecked(opt.selected)

            self.mAppFrame.layout().insertWidget(i + 1, cb)
            self.connect(cb, QtCore.SIGNAL("clicked()"), self.onOptionBox)
            self.selectedAppOptions[cb] = opt
            self.appSpecificWidgets.append(cb)

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
      for w in self.appSpecificWidgets:
         self.mAppFrame.layout().removeWidget(w)
         w.deleteLater()
      #for l in self.appSpecificLayouts:
      #   l.deleteLater()

      self.commandOptions      = []
      self.selectedApp         = None
      self.selectedAppOptions  = {}
      self.mComboBoxes         = {}
      self.appSpecificWidgets = []
      self.appSpecificLayouts = []


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

   def onComboBox(self, index):
      print "A: ", index
      self.commandOptions = []
      self._setCommandOptions()

   def _setCommandOptions(self):
      for w, opt in self.selectedAppOptions.items():
         if w.isChecked():
            pass
            #self.commandOptions.append(opt.flag)
         label = opt.mChoices[0].label
         print "%s = %s" % (label, w.isChecked())
      for cb, opt in self.mComboBoxes.items():
         index = cb.currentIndex()
         result = ""
         if index >= len(opt.mChoices):
            result = cb.currentText()
         else:
            result = opt.mChoices[index].label
         print "%s = %s" % (opt.group_name, result)
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
      for node in self.mClusterModel.mNodes:
         command_map = self.apps[self.selectedApp].getCommandMap()
         command = getMaxMatchValue(command_map, node.getClass())
         print "\n Node: [%s] [%s]" % (node.getName(), command)
         if not None == command:
            try:
               node.runCommand(command[0], self.mClusterModel.mOutputLogger)
            except:
               pass

      
      # Construct the list of options as a single string.
      #opts = ""
      #for o in self.commandOptions:
      #   opts += " " + o
      #cmd = cmd + opts

      #if cmd != "" and cmd != None:
      #   print "running command: ", cmd
      #   self.mClusterModel.runRemoteCommand(cmd, cmd)
#     #    self.mClusterModel.runRemoteCommand('rpm -qa', 'rpm -qa')
      #   #self.launchButton.setEnabled(False)
      #   #self.killButton.setEnabled(True)
      #else:
      #   assert "This should never happen"

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

class Choice:
   def __init__(self, xmlElt):
      self.label = xmlElt.get("label")
      values = xmlElt.findall("./value")
      print "Choice: ", self.label
      self.mValues = {}
      for v in values:
         node_class = v.get("class")
         flag = v.get("flag")
         val = v.text
         self.mValues[node_class] = (flag, val)
         print "Class: %s flag: %s val: %s" % (node_class, flag, val)

class AppOption:
   """ Encapsulation of command-line options that may be passed to apps. """
   def __init__(self, xmlElt):
      #self.label = xmlElt.get("name")
      #self.flag  = xmlElt.get("flag")
      self.tip   = xmlElt.get("tooltip")
      #print "name: ", self.label
      print "tip: ", self.tip

      # Can the user edit the options value
      editable = xmlElt.get("editable")
      if editable == "" or editable == None:
         self.editable = True
      elif editable == "true" or editable == "1":
         self.editable = True
      else:
         self.editable = False
         
      # Is the option visible to the user?
      visible = xmlElt.get("visible")
      if visible == "" or visible == None:
         self.visible = True
      elif visible == "true" or visible == "1":
         self.visible = True
      else:
         self.visible = False

      self.mChoices = []
      choices = xmlElt.findall("./choice")
      for c in choices:
         self.mChoices.append(Choice(c))
      #
      #selected = xmlElt.get("selected")

      self.selected = False
      #if selected == "" or selected == None:
      #   self.selected = False
      #elif selected == "true" or selected == "1":
      #   self.selected = True
      #else:
      #   self.selected = False

class AppExclusiveOption(AppOption):
   def __init__(self, xmlElt):
      AppOption.__init__(self, xmlElt)
      self.group_name = xmlElt.get("name")

class Command:
   def __init__(self, xmlElt):
      self.mSubClasses = xmlElt.get("class")
      self.mEnv = xmlElt.get("elt")
      self.mCommand = xmlElt.text

class Application:
   """ Representation of an application that can be launched. """

   def __init__(self, xmlElt):
      self.name = xmlElt.get("name")

      self.mCommandMap = {}
      commands = xmlElt.findall("./commands/command")
      for elt in commands:
         sub_class = elt.get("class")
         command = elt.text
         env = elt.get("env")
         self.mCommandMap[sub_class] = [command, env]

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
      option_elts = xmlElt.findall("./options/option")
      if None != option_elts: #and len(tip_elts) > 0:

         for n in option_elts:
            if len(n) > 1:
               self.options.append(AppExclusiveOption(n))
            else:
               self.options.append(AppOption(n))

   def getCommandMap(self):
      return self.mCommandMap
      
   def getName(self):
      return self.name

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
