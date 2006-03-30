#!/bin/env python

# Copyright (C) Infiscape Corporation 2006

import sys

from PyQt4 import QtGui, QtCore
import ClusterEditorBase
import ClusterModel
import elementtree.ElementTree as ET

class ClusterEditor(QtGui.QWidget, ClusterEditorBase.Ui_ClusterEditor):
   def __init__(self, parent = None):
      QtGui.QMainWindow.__init__(self, parent)
      self.setupUi(self)
      self.mTreeModel = None
      self.mAppSpecificWidgets = []
      self.mSelectedApp = None

   def setupUi(self, widget):
      ClusterEditorBase.Ui_ClusterEditor.setupUi(self, widget)
      #self.mParentDelegate = ClusterModel.ParentDelegate()
      #self.mTreeView.setItemDelegate(self.mParentDelegate)
      self.connect(self.mAppComboBox,QtCore.SIGNAL("activated(int)"),self.onAppSelect)

   def setTree(self, tree):
      # Create cluster configuration
      self.mTreeModel = ClusterModel.TreeModel(tree)
      self.mTableModel = ClusterModel.TableModel()
      self.mTreeView.setModel(self.mTreeModel)
      self.mTableView.setModel(self.mTableModel)

      self._fillInApps()

      #self.connect(self.mTreeView, QtCore.SIGNAL("pressed(QModelIndex)"), self.onElementSelected)
      # Connect new selection model
      QtCore.QObject.connect(self.mTreeView.selectionModel(),
         QtCore.SIGNAL("selectionChanged(QItemSelection,QItemSelection)"), self.onElementSelected)
      #QtCore.QObject.connect(self.mTreeView.selectionModel(),
      #   QtCore.SIGNAL("currentChanged(QItemSelection,QItemSelection)"), self.onElementSelected)

   def onElementSelected(self, newSelection, oldSelection):
      #print "Current row: %s" % (self.mTreeView.currentIndex().row())
      if len(newSelection.indexes()) > 0:
         selected_element = self.mTreeView.model().data(newSelection.indexes()[0], QtCore.Qt.UserRole)
      else:
         selected_element = None
      print "Selected: %s" % (selected_element)
      self.mTableModel.setElement(selected_element)
      self.mTableView.reset()
      self.mTableView.resizeColumnsToContents()

   def onAppSelect(self):
     self._setApplication(self.mAppComboBox.currentIndex())

   def _fillInApps(self):
      """ Fills in the application panel. """
      self.mAppComboBox.clear()

      apps = self.mTreeModel.mAppLabel.mChildren
   
      for app in apps:
         #self.mAppComboBox.insertItem(app.getName())
         self.mAppComboBox.addItem(app.getName())
   
      if len(apps) > 0:
         self.mAppComboBox.setCurrentIndex(0)
         self._setApplication(0)
      else:
         print "ERROR: No applications defined!"
         QApplication.exit(0)

   def _setApplication(self, index):
      if self.mSelectedApp != None:
         self._resetAppState()

      apps = self.mTreeModel.mAppLabel.mChildren
      assert index < len(apps)
      self.mSelectedApp = apps[index]
      print "Setting application [%s] [%s]" % (index, self.mSelectedApp.getName())
      """
      sh = QtGui.QFrame()
      test = QtGui.QLabel(sh)
      test.setText("Aron")
      #sh = QtGui.QLabel()
      #sh.setText("Aron")
      sh.setParent(self.mLaunchFrame)
      self.mLaunchFrame.layout().addWidget(sh)
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(3))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(sh.sizePolicy().hasHeightForWidth())
      sh.setSizePolicy(sizePolicy)
      #sh.setGeometry(QtCore.QRect(90,120,120,80))
      sh.setFrameShape(QtGui.QFrame.StyledPanel)
      sh.setFrameShadow(QtGui.QFrame.Raised)
      sh.show()
      """
      for c in self.mSelectedApp.mChildren:
         if c.mVisible:
            sh = _buildWidget(c)
            sh.setParent(self.mLaunchFrame);
            self.mLaunchFrame.layout().insertWidget(self.mLaunchFrame.layout().count()-1, sh)
            self.mAppSpecificWidgets.append(sh)
            sh.show()

   def _resetAppState(self):
      """ Resets the information associated with the selected application. """
      for w in self.mAppSpecificWidgets:
         self.mLaunchFrame.layout().removeWidget(w)
         w.deleteLater()
      #for l in self.appSpecificLayouts:
      #   l.deleteLater()

      #self.commandChoices      = []
      #self.selectedApp         = None
      #self.selectedAppOptions  = {}
      #self.mComboBoxes         = {}
      self.mAppSpecificWidgets = []
      #self.appSpecificLayouts = []



def _buildWidget(obj):
   name = obj.getName()

   if isinstance(obj, ClusterModel.Application):
      pass
   #   print "Building Application Sheet... ", name
   #   sh = QtGui.QLabel(self)
   #   sh.setText("Hi")
   #   sh.show()
   elif isinstance(obj, ClusterModel.GlobalOption):
      pass
   #   print "Building Global Option Sheet... ", name
   elif isinstance(obj, ClusterModel.Group):
      print "Building Group Sheet... ", name
      sh = GroupSheet(obj)
      return sh
   elif isinstance(obj, ClusterModel.Choice):
      print "Building Choice Sheet... ", name
      sh = ChoiceSheet(obj)
      return sh
   if isinstance(obj, ClusterModel.Arg):
      print "Building Arg Sheet... ", name
      sh = ArgSheet(obj)
      return sh
   elif isinstance(obj, ClusterModel.Command):
      print "Building Command Sheet... ", name
      sh = CommandSheet(obj)
      return sh
   elif isinstance(obj, ClusterModel.Cwd):
      print "Building CWD Sheet... ", name
      sh = CwdSheet(obj)
      return sh
   elif isinstance(obj, ClusterModel.EnvVar):
      print "Building EnvVar Sheet... ", name
      sh = EnvVarSheet(obj)
      return sh

class ChoiceSheet(QtGui.QFrame):
   def __init__(self, obj, parent = None):
      QtGui.QFrame.__init__(self, parent)

      self.mObj = obj
      self.mSelectedFrame = None

      # XXX: Might want to put some where else.
      self.setupUi()
      self._fillCombo()
      self.connect(self.mChoice, QtCore.SIGNAL("activated(int)"), self.choiceSelected)

   def setupUi(self):

      self.gridlayout = QtGui.QGridLayout(self)
      self.gridlayout.setMargin(1)
      self.gridlayout.setSpacing(1)
      self.gridlayout.setObjectName("gridlayout")
      
      self.mChoiceLabel = QtGui.QLabel(self)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.mChoiceLabel.sizePolicy().hasHeightForWidth())
      self.mChoiceLabel.setSizePolicy(sizePolicy)
      self.mChoiceLabel.setObjectName("mChoiceLabel")
      self.mChoiceLabel.setText(self.mObj.mLabel)
      self.gridlayout.addWidget(self.mChoiceLabel,0,0,1,2)
      
      spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
      self.gridlayout.addItem(spacerItem,1,0,1,1)
      
      self.mChoice = QtGui.QComboBox(self)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(0))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.mChoice.sizePolicy().hasHeightForWidth())
      self.mChoice.setSizePolicy(sizePolicy)
      self.mChoice.setObjectName("mChoice")
      self.gridlayout.addWidget(self.mChoice,0,2,1,1)

   def _fillCombo(self):
      for c in self.mObj.mChildren:
         print c.getName()
         self.mChoice.addItem(c.getName())
   
      if len(self.mObj.mChildren) > 0:
         self.mChoice.setCurrentIndex(0)
         self._setChoice(0)
      else:
         print "ERROR: No choices defined!"
         QApplication.exit(0)

   
   def choiceSelected(self):
     self._setChoice(self.mChoice.currentIndex())

   def _setChoice(self, index):
      if self.mSelectedFrame is not None:
         self.layout().removeWidget(self.mSelectedFrame)
         self.mSelectedFrame.deleteLater()

      self.mSelectedFrame = None
      # XXX: Add error testing
      self.mObj.mSelected = index
      obj = self.mObj.mChildren[index]
      if obj is not None and obj.mVisible:
         self.mSelectedFrame = _buildWidget(obj)
         self.mSelectedFrame.setParent(self)
         self.gridlayout.addWidget(self.mSelectedFrame,1,1,1,2)
      
class GroupSheet(QtGui.QGroupBox):
   def __init__(self, obj, parent = None):
      QtGui.QFrame.__init__(self, parent)

      self.mObj = obj

      #sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(3))
      #sizePolicy.setHorizontalStretch(0)
      #sizePolicy.setVerticalStretch(0)
      #sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
      #self.setSizePolicy(sizePolicy)
      #self.setMinimumSize(QtCore.QSize(16,16))
      #self.setFrameShape(QtGui.QFrame.StyledPanel)
      #self.setFrameShadow(QtGui.QFrame.Raised)

      # XXX: Might want to put some where else.
      self.setupUi()

   def setupUi(self):
      self.setTitle(self.mObj.mLabel)

      self.vboxlayout1 = QtGui.QVBoxLayout(self)
      self.vboxlayout1.setMargin(1)
      self.vboxlayout1.setSpacing(1)
      self.vboxlayout1.setObjectName("vboxlayout1")

      for c in self.mObj.mChildren:
         if c.mVisible:
            sh = _buildWidget(c)
            sh.setParent(self);
            self.layout().addWidget(sh)
            #self.mAppSpecificWidgets.append(sh)
            #sh.show()

class CommandSheet(QtGui.QWidget):
   def __init__(self, obj, parent = None):
      QtGui.QFrame.__init__(self, parent)

      self.mObj = obj

      # XXX: Might want to put some where else.
      self.setupUi()

   def setupUi(self):
      self.hboxlayout = QtGui.QHBoxLayout(self)
      self.hboxlayout.setMargin(1)
      self.hboxlayout.setSpacing(1)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.mCommandLabel = QtGui.QLabel(self)
      self.mCommandLabel.setObjectName("mCommandLabel")
      command_text = "Command [" + self.mObj.mClass + "]:"
      self.mCommandLabel.setText(command_text)
      self.hboxlayout.addWidget(self.mCommandLabel)
      
      self.mCommand = QtGui.QLineEdit(self)
      self.mCommand.setObjectName("mCommand")
      self.mCommand.setText(self.mObj.mValue)
      self.mCommand.setEnabled(self.mObj.mEditable)
      self.hboxlayout.addWidget(self.mCommand)
      self.connect(self.mCommand, QtCore.SIGNAL("editingFinished()"),self.onEdited)

   def onEdited(self):
      print self.mCommand.text()
      self.mObj.mValue = self.mCommand.text()

class CwdSheet(QtGui.QWidget):
   def __init__(self, obj, parent = None):
      QtGui.QFrame.__init__(self, parent)

      self.mObj = obj

      # XXX: Might want to put some where else.
      self.setupUi()

   def setupUi(self):
      self.hboxlayout = QtGui.QHBoxLayout(self)
      self.hboxlayout.setMargin(1)
      self.hboxlayout.setSpacing(1)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.mCwdLabel = QtGui.QLabel(self)
      self.mCwdLabel.setObjectName("mCurrentWorkingDirLabel")
      command_text = "Current Working Directory [" + self.mObj.mClass + "]:"
      self.mCwdLabel.setText(command_text)
      self.hboxlayout.addWidget(self.mCwdLabel)
      
      self.mCwd = QtGui.QLineEdit(self)
      self.mCwd.setObjectName("mCwd")
      self.mCwd.setText(self.mObj.mValue)
      self.mCwd.setEnabled(self.mObj.mEditable)
      self.hboxlayout.addWidget(self.mCwd)
      self.connect(self.mCwd, QtCore.SIGNAL("editingFinished()"),self.onEdited)

   def onEdited(self):
      print self.mCwd.text()
      self.mObj.mValue = self.mCwd.text()

class ArgSheet(QtGui.QWidget):
   def __init__(self, obj, parent = None):
      QtGui.QFrame.__init__(self, parent)

      self.mObj = obj

      # XXX: Might want to put some where else.
      self.setupUi()

   def setupUi(self):
      self.hboxlayout = QtGui.QHBoxLayout(self)
      self.hboxlayout.setMargin(1)
      self.hboxlayout.setSpacing(1)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.mArgLabel = QtGui.QLabel(self)
      self.mArgLabel.setObjectName("mCurrentWorkingDirLabel")
      command_text = self.mObj.mLabel + "[" + self.mObj.mClass + "]:"
      self.mArgLabel.setText(command_text)
      self.hboxlayout.addWidget(self.mArgLabel)
      
      self.mArg = QtGui.QLineEdit(self)
      self.mArg.setObjectName("mArg")
      self.mArg.setText(self.mObj.mValue)
      self.mArg.setEnabled(self.mObj.mEditable)
      self.hboxlayout.addWidget(self.mArg)
      self.connect(self.mArg, QtCore.SIGNAL("editingFinished()"),self.onEdited)

   def onEdited(self):
      print self.mArg.text()
      self.mObj.mValue = self.mArg.text()

class EnvVarSheet(QtGui.QWidget):
   def __init__(self, obj, parent = None):
      QtGui.QFrame.__init__(self, parent)

      self.mObj = obj

      # XXX: Might want to put some where else.
      self.setupUi()

   def setupUi(self):
      self.hboxlayout = QtGui.QHBoxLayout(self)
      self.hboxlayout.setMargin(1)
      self.hboxlayout.setSpacing(1)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.mEnvVarLabel = QtGui.QLabel(self)
      self.mEnvVarLabel.setObjectName("mCurrentWorkingDirLabel")
      command_text = self.mObj.mLabel + "[" + self.mObj.mClass + "]:"
      self.mEnvVarLabel.setText(command_text)
      self.hboxlayout.addWidget(self.mEnvVarLabel)
      
      self.mEnvVar = QtGui.QLineEdit(self)
      self.mEnvVar.setObjectName("mEnvVar")
      self.mEnvVar.setText(self.mObj.mValue)
      self.mEnvVar.setEnabled(self.mObj.mEditable)
      self.hboxlayout.addWidget(self.mEnvVar)
      self.connect(self.mEnvVar, QtCore.SIGNAL("editingFinished()"),self.onEdited)

   def onEdited(self):
      print self.mEnvVar.text()
      self.mObj.mValue = self.mEnvVar.text()

def main():
   try:
      app = QtGui.QApplication(sys.argv)

      # Parse xml config file
      tree = ET.ElementTree(file=sys.argv[1])


      # Create and display GUI
      ce = ClusterEditor()
      
      ce.setTree(tree)
      ce.show()
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
