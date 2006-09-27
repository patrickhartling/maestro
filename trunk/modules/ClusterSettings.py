# Maestro is Copyright (C) 2006 by Infiscape
#
# Original Author: Aron Bierbaum
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import sys, socket
from PyQt4 import QtGui, QtCore
import ClusterSettingsBase
import ClusterSettingsResource
import Ensemble
import EnsembleModel
import MaestroConstants

ERROR = 0
LINUX = 1
WIN = 2
WINXP = 3
MACOS = 4
MACOSX = 5
HPUX = 6
AIX = 7
SOLARIS = 8

Icons = {}
Icons[MaestroConstants.UNKNOWN] = QtGui.QIcon(":/ClusterSettings/images/error2.png")
Icons[MaestroConstants.WIN] = QtGui.QIcon(":/ClusterSettings/images/win_xp.png")
Icons[MaestroConstants.WINXP] = QtGui.QIcon(":/ClusterSettings/images/win_xp.png")
Icons[MaestroConstants.LINUX] = QtGui.QIcon(":/ClusterSettings/images/linux2.png")

class TargetListItem(QtGui.QListWidgetItem):
   def __init__(self, title, id, index, parent=None):
      QtGui.QListWidgetItem.__init__(self, parent)
      self.mTitle = title
      self.mOs = id
      self.mIndex = index

   def data(self, role):
      if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
         return QtCore.QVariant(self.mTitle)
      elif role == QtCore.Qt.DecorationRole:
         if Icons.has_key(self.mOs):
            return QtCore.QVariant(Icons[self.mOs])
         else:
            return QtCore.QVariant()
      elif role == QtCore.Qt.UserRole:
         return (self.mTitle, self.mOs, self.mIndex)
      return QtCore.QVariant()

class ClusterSettings(QtGui.QWidget, ClusterSettingsBase.Ui_ClusterSettingsBase):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)
      self.mEnsemble = None
      self.mSelectedNode = None

   def setupUi(self, widget):
      """
      Setup all initial gui settings that don't need to know about the cluster configuration.
      """
      ClusterSettingsBase.Ui_ClusterSettingsBase.setupUi(self, widget)
      self.mTitleLbl.setBackgroundRole(QtGui.QPalette.Mid)
      self.mTitleLbl.setForegroundRole(QtGui.QPalette.Shadow)
      
      QtCore.QObject.connect(self.mRefreshBtn,QtCore.SIGNAL("clicked()"), self.onRefresh)
      QtCore.QObject.connect(self.mAddBtn,QtCore.SIGNAL("clicked()"), self.onAdd)
      QtCore.QObject.connect(self.mRemoveBtn,QtCore.SIGNAL("clicked()"), self.onRemove)
      # Call if you want an icon view
      #self.mClusterListView.setViewMode(QtGui.QListView.IconMode)
      self.connect(self.mNameEdit, QtCore.SIGNAL("editingFinished()"), self.onNodeSettingsChanged)
      self.connect(self.mHostnameEdit, QtCore.SIGNAL("editingFinished()"), self.onNodeSettingsChanged)

      # Setup a custom context menu callback.
      self.mClusterListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
      self.connect(self.mClusterListView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
         self.onNodeContextMenu)

      self.connect(self.mTargetList, QtCore.SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),
         self.onCurrentTargetChanged)

      xp_icon = QtGui.QIcon(":/ClusterSettings/images/win_xp.png")
      self.mRebootToWindowsAction = QtGui.QAction(xp_icon, self.tr("Windows"), self)
      self.connect(self.mRebootToWindowsAction, QtCore.SIGNAL("triggered()"), self.onRebootToWindows)
      self.mRebootAllToWindowsAction = QtGui.QAction(xp_icon, self.tr("Windows"), self)
      self.connect(self.mRebootAllToWindowsAction, QtCore.SIGNAL("triggered()"), self.onRebootAllToWindows)

      linux_icon = QtGui.QIcon(":/ClusterSettings/images/linux2.png")
      self.mRebootToLinuxAction = QtGui.QAction(linux_icon, self.tr("Linux"), self)
      self.connect(self.mRebootToLinuxAction, QtCore.SIGNAL("triggered()"), self.onRebootToLinux)
      self.mRebootAllToLinuxAction = QtGui.QAction(linux_icon, self.tr("Linux"), self)
      self.connect(self.mRebootAllToLinuxAction, QtCore.SIGNAL("triggered()"), self.onRebootAllToLinux)

      # Set the default action for the reboot all buttons.
      self.mRebootWinBtn.setDefaultAction(self.mRebootAllToWindowsAction)
      self.mRebootLinuxBtn.setDefaultAction(self.mRebootAllToLinuxAction)

      self.mTestAction = QtGui.QAction(self.tr("&Test"), self)
      self.mTestAction.setShortcut(self.tr("Ctrl+T"))
      self.connect(self.mTestAction, QtCore.SIGNAL("triggered()"), self.onTest)

   def onTest(self):
      if self.mSelectedNode is not None:
         self.mEventManager.emit(self.mSelectedNode.getId(), "reboot.reboot", ())

   def onNodeContextMenu(self, point):
      menu = QtGui.QMenu("Reboot", self)

      temp_callbacks = []
      menu.addAction(self.mRebootToLinuxAction)
      menu.addAction(self.mRebootToWindowsAction)
      menu.addSeparator()
      if self.mSelectedNode is not None:
         # For each target operation system, build a TargetListItem
         for target in self.mSelectedNode.mTargets:
            (title, os, index) = target
            icon = Icons[os]
            node_id = self.mSelectedNode.getId()
            callback = lambda ni=node_id, i=index, t=title: (self.onTargetTriggered(ni, i, t))
            temp_callbacks.append(callback)
            menu.addAction(icon, title, callback)

      menu.exec_(self.mClusterListView.mapToGlobal(point))

   def onTargetTriggered(self, node_id, index, title):
      print "Target: [%s][%s]" % (index, title)
      self.mEventManager.emit(node_id, "reboot.set_default_target", (index, title))
   
   def init(self, ensemble, eventManager):
      """ Configure the user interface.

          @param ensemble: The current Ensemble configuration.
          @param eventManager: Reference to Maestro's EventManager.
      """

      # If an ensemble already exists, disconnect it.
      if self.mEnsemble is not None:
         self.disconnect(self.mEnsemble, QtCore.SIGNAL("newConnections()"), self.onNewConnections)
         self.disconnect(self.mEnsemble, QtCore.SIGNAL("nodeChanged(QString)"), self.onNodeChanged)

      # Set the new ensemble configuration.
      self.mEnsemble = ensemble

      # Connect the new ensemble.
      self.connect(self.mEnsemble, QtCore.SIGNAL("newConnections()"), self.onNewConnections)
      self.connect(self.mEnsemble, QtCore.SIGNAL("nodeChanged(QString)"), self.onNodeChanged)

      self.mEventManager = eventManager

      # Create a model for our ListView
      self.mEnsembleModel = EnsembleModel.EnsembleModel(self.mEnsemble)

      # If selection model already exists then disconnect signal
      if not None == self.mClusterListView.selectionModel():
         QtCore.QObject.disconnect(self.mClusterListView.selectionModel(),
            QtCore.SIGNAL("currentChanged(QModelIndex,QModelIndex)"), self.onNodeSelected)

      # Set the model.
      self.mClusterListView.setModel(self.mEnsembleModel)

      # Connect new selection model
      QtCore.QObject.connect(self.mClusterListView.selectionModel(),
         QtCore.SIGNAL("currentChanged(QModelIndex,QModelIndex)"), self.onNodeSelected)

   def onRefresh(self):
      """ Slot that requests information about all nodes in the Ensemble. """
      if not self.mEnsemble is None:
         self.mEnsemble.refreshConnections()

      self.mEventManager.emit("*", "settings.get_os", ())
      self.mEventManager.emit("*", "reboot.get_targets", ())

   def onAdd(self):
      """ Called when user presses the add button. """
      #if not None == self.mClusterModel:
      #   self.mClusterModel.insertRow(self.mClusterModel.rowCount())
      pass

   def onRemove(self):
      """ Called when user presses the remove button. """
      #row = self.mClusterListView.currentIndex().row()
      #if (not None == self.mClusterModel) and row >= 0:
      #   self.mClusterModel.removeRow(row)
      pass

   def onNodeSettingsChanged(self):
      """ Slot that is called when the user has finished editing a
          field in the node settings.
      """

      # Get the currently selected node.
      selected_node = self.mClusterListView.model().data(self.mClusterListView.currentIndex(), QtCore.Qt.UserRole)

      # Can't get a change if a node is not selected
      assert not None == selected_node

      modified = False
      # Process changes
      if self.mNameEdit.isModified():
         selected_node.setName(str(self.mNameEdit.text()))
         self.mNameEdit.setModified(False)
         modified = True

      if self.mHostnameEdit.isModified():
         # Disconnect and try to connect to new hostname later..
         try:
            ip_address = selected_node.getIpAddress()
            self.mEventManager.disconnectFromNode(ip_address)
         except:
            # Do nothing
            pass

         # Set the new hostname.
         selected_node.setHostname(str(self.mHostnameEdit.text()))
         self.mHostnameEdit.setModified(False)
         modified = True

         # Try to connect to new hostname.
         self.mEnsemble.refreshConnections()

      # Only update gui if something really changed.
      if modified:
         self.refreshNodeSettings()
         # Force the cluster model to generate a dataChanged signal.
         self.mClusterListView.model().setData(self.mClusterListView.currentIndex(), QtCore.QVariant(), QtCore.Qt.DisplayRole)
   
   def onNodeSelected(self, selected, deselected):
      """ Slot that is called when a cluster node is selected. """
      # Get the currently selected node and save it.
      selected_node = self.mClusterListView.model().data(self.mClusterListView.currentIndex(), QtCore.Qt.UserRole)
      self.mSelectedNode = selected_node
      # Refresh all node information.
      self.refreshNodeSettings()
      # We must also refresh the list of all operating system targets.
      self.refreshTargetList()

   def refreshNodeSettings(self):
      """
      Fills in the node information for the currently selected node. This gets called
      whenever a new node is selected in the list.
      """

      # Clear all information
      self.mNameEdit.clear()
      self.mHostnameEdit.clear()
      self.mCurrentOsEdit.clear()
      self.mIpAddressEdit.clear()

      # Early out if there is no node selected.
      if self.mSelectedNode is not None:      
         # Set node information that we know
         self.mNameEdit.setText(self.mSelectedNode.getName())
         self.mHostnameEdit.setText(self.mSelectedNode.getHostname())

         # Get IP address
         try:
            self.mIpAddressEdit.setText(self.mSelectedNode.getIpAddress())
         except:
            self.mIpAddressEdit.setText('Unknown')

         # Get the name of the current platform.
         self.mCurrentOsEdit.setText(self.mSelectedNode.getPlatformName())
         
   def refreshTargetList(self):
      """ Refresh the list of target operation systems. """

      # Clear all current targets out of list.
      self.mTargetList.clear()

      if self.mSelectedNode is not None:
         # For each target operation system, build a TargetListItem
         for target in self.mSelectedNode.mTargets:
            (title, os, index) = target
            tli = TargetListItem(title, os, index)
            self.mTargetList.addItem(tli)

         # Selected the current default target if specified.
         if self.mSelectedNode.mDefaultTargetIndex >= 0:
            self.mTargetList.setCurrentRow(self.mSelectedNode.mDefaultTargetIndex)
            # Ensure that the selected target is visible.
            if self.mTargetList.currentItem() is not None:
               self.mTargetList.scrollToItem(self.mTargetList.currentItem())

   def onCurrentTargetChanged(self, current, previous):
      """ Slot that sets the default target on the selected node to the
          specified index.

          @param current: The currently selected TargetListItem
          @param previous: The previously selected TargetListItem
      """
      assert(self.mSelectedNode is not None)
      # If the previous selection was None, then we know the change was
      # due to UI initialization.
      if current is not None and previous is not None:
         node_id = self.mSelectedNode.getId()
         # Tell the selected node to change it's default target.
         self.mEventManager.emit(node_id, "reboot.set_default_target", (current.mIndex, current.mTitle))

   def onNodeChanged(self, nodeId):
      """ Slot that is called when a node's state changes. If the currently
          selected node changes, we need to update the target list and the
          current default target.

          @param nodeId: The id of the node that changed.
      """
      if self.mSelectedNode is not None and nodeId == self.mSelectedNode.getId():
         self.refreshTargetList()
         self.mClusterListView.model().setData(self.mClusterListView.currentIndex(), QtCore.QVariant(), QtCore.Qt.DisplayRole)

   def onRebootToLinux(self):
      """ Slot that makes the selected node reboot to Linux. """
      assert(self.mSelectedNode is not None)
      node_id = self.mSelectedNode.getId()
      self.mEventManager.emit(node_id, "reboot.switch_os", (MaestroConstants.LINUX,))

   def onRebootToWindows(self):
      """ Slot that makes the selected node reboot to Windows. """
      assert(self.mSelectedNode is not None)
      node_id = self.mSelectedNode.getId()
      self.mEventManager.emit(node_id, "reboot.switch_os", (MaestroConstants.WINXP,))

   def onRebootAllToLinux(self):
      """ Slot that makes all nodes reboot to Linux. """
      self.mEventManager.emit("*", "reboot.switch_os", (MaestroConstants.LINUX,))

   def onRebootAllToWindows(self):
      """ Slot that makes all nodes reboot to Windows. """
      self.mEventManager.emit("*", "reboot.switch_os", (MaestroConstants.WINXP,))

   def onNewConnections(self):
      """ Called when the cluster control has connected to another node. """
      self.mClusterListView.reset()
      # Refresh the information about the node.
      self.refreshNodeSettings()
      # We must also refresh the list of all operating system targets.
      self.refreshTargetList()


   def getName():
        return "Cluster Settings"
   getName = staticmethod(getName)

def getModuleInfo():
   icon = QtGui.QIcon(":/ClusterSettings/images/management.png")
   return (ClusterSettings, icon)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   cs = ClusterSettings()
   cs.show()
   sys.exit(app.exec_())
