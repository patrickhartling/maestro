# Copyright (C) Infiscape Corporation 2006

import sys, socket
from PyQt4 import QtGui, QtCore
import ClusterSettingsBase
import ClusterSettingsResource

ERROR = 0
LINUX = 1
WIN = 2
WINXP = 3
MACOS = 4
MACOSX = 5
HPUX = 6
AIX = 7
SOLARIS = 8

class ClusterSettings(QtGui.QWidget, ClusterSettingsBase.Ui_ClusterSettingsBase):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)
      self.mClusterModel = None

   def setupUi(self, widget):
      """
      Setup all initial gui settings that don't need to know about the cluster configuration.
      """
      ClusterSettingsBase.Ui_ClusterSettingsBase.setupUi(self, widget)
      QtCore.QObject.connect(self.mRefreshBtn,QtCore.SIGNAL("clicked()"), self.onRefresh)
      QtCore.QObject.connect(self.mAddBtn,QtCore.SIGNAL("clicked()"), self.onAdd)
      QtCore.QObject.connect(self.mRemoveBtn,QtCore.SIGNAL("clicked()"), self.onRemove)
      # Call if you want an icon view
      #self.mClusterListView.setViewMode(QtGui.QListView.IconMode)
      self.connect(self.mNameEdit, QtCore.SIGNAL("editingFinished()"), self.nodeSettingsChanged)
      self.connect(self.mHostnameEdit, QtCore.SIGNAL("editingFinished()"), self.nodeSettingsChanged)
   
   def onRefresh(self):
      """ Called when user presses the refresh button. """
      if not None == self.mClusterModel:
         self.mClusterModel.refreshConnections()

   def onAdd(self):
      """ Called when user presses the add button. """
      if not None == self.mClusterModel:
         self.mClusterModel.insertRow(self.mClusterModel.rowCount())

   def onRemove(self):
      """ Called when user presses the remove button. """
      row = self.mClusterListView.currentIndex().row()
      if (not None == self.mClusterModel) and row >= 0:
         self.mClusterModel.removeRow(row)

   def nodeSettingsChanged(self):
      """ Apply any user changes. """

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
         selected_node.setHostname(str(self.mHostnameEdit.text()))
         self.mHostnameEdit.setModified(False)
         modified = True

         # Disconnect and try to connect to new hostname.
         selected_node.disconnect()
         self.mClusterModel.refreshConnections()

      # Only update gui if something really changed.
      if modified:
         self.refreshNodeInfo()
         # Force the cluster model to generate a dataChanged signal.
         self.mClusterListView.model().setData(self.mClusterListView.currentIndex(), QtCore.QVariant(), QtCore.Qt.DisplayRole)

   def onNodeSelected(self):
      """ Called when a cluster node in the list is selected. """
      self.refreshNodeInfo()

   def refreshNodeInfo(self):
      """
      Fills in the node information for the currently selected node. This gets called
      whenever a new node is selected in the list.
      """
      self.mNameEdit.clear()
      self.mHostnameEdit.clear()
      self.mCurrentOsEdit.clear()
      self.mIpAddressEdit.clear()
      
      # Get the currently selected node.
      selected_node = self.mClusterListView.model().data(self.mClusterListView.currentIndex(), QtCore.Qt.UserRole)
      
      # Set node information that we know
      self.mNameEdit.setText(selected_node.getName())
      self.mHostnameEdit.setText(selected_node.getHostname())

      # Get IP address
      try:
         (hostname, alias_list, ipaddrlist) = socket.gethostbyaddr(selected_node.getHostname())
         self.mIpAddressEdit.setText(ipaddrlist[0])
      except:
         self.mIpAddressEdit.setText('Unknown')

      # Get information from proxy
      if not None == selected_node.proxy():
         # Get operating system
         try:
            platform = selected_node.proxy().getService("Settings").getPlatformName()
            self.mCurrentOsEdit.setText(platform)
         except:
            self.mCurrentOsEdit.setText("Unknown")

   def onNewConnections(self):
      self.mClusterListView.reset()
      self.refreshNodeInfo()

   def configure(self, clusterModel):
      """ Configure the user interface with data in cluster configuration. """
      # Set the new cluster configuration
      if not None == self.mClusterModel:
         self.disconnect(self.mClusterModel, QtCore.SIGNAL("newConnections()"), self.onNewConnections)
      self.mClusterModel = clusterModel
      self.connect(self.mClusterModel, QtCore.SIGNAL("newConnections()"), self.onNewConnections)

      # If selection model already exists then disconnect signal
      if not None == self.mClusterListView.selectionModel():
         QtCore.QObject.disconnect(self.mClusterListView.selectionModel(),
            QtCore.SIGNAL("selectionChanged(QItemSelection,QItemSelection)"), self.onNodeSelected)
      self.mClusterListView.setModel(self.mClusterModel)
      self.mMasterCB.setModel(self.mClusterModel)

      # Connect new selection model
      QtCore.QObject.connect(self.mClusterListView.selectionModel(),
         QtCore.SIGNAL("selectionChanged(QItemSelection,QItemSelection)"), self.onNodeSelected)

   def getName():
        return "Cluster Settings"
   getName = staticmethod(getName)

def getModuleInfo():
   icon = QtGui.QIcon(":/ClusterSettings/images/tools.gif")
   return (ClusterSettings, icon)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   cs = ClusterSettings()
   cs.show()
   sys.exit(app.exec_())

