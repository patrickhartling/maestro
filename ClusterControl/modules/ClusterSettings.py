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

class ClusterModel(QtCore.QAbstractListModel):
   """Create a new cluster element"""
   def __init__(self, clusterConfig, parent=None):
      QtCore.QAbstractListModel.__init__(self, parent)
      self.mClusterConfig = clusterConfig
      self.mIcons = {}
      self.mIcons[ERROR] = QtGui.QIcon(":/ClusterSettings/images/error2.png")
      self.mIcons[WIN] = QtGui.QIcon(":/ClusterSettings/images/win_xp.png")
      self.mIcons[WINXP] = QtGui.QIcon(":/ClusterSettings/images/win_xp.png")
      self.mIcons[LINUX] = QtGui.QIcon(":/ClusterSettings/images/linux2.png")

   def data(self, index, role=QtCore.Qt.DisplayRole):
      if not index.isValid():
         return QtCore.QVariant()
        
      if role == QtCore.Qt.DecorationRole:
         cluster_node = self.mClusterConfig.mNodes[index.row()]
         try:
            index = cluster_node.proxy().getService("Settings").getPlatform()
            return QtCore.QVariant(self.mIcons[index])
         except:
            return QtCore.QVariant(self.mIcons[ERROR])
      elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
         return QtCore.QVariant(str(self.mClusterConfig.mNodes[index.row()].getName()))
      elif role == QtCore.Qt.UserRole:
         return self.mClusterConfig.mNodes[index.row()]
       
      return QtCore.QVariant()

   def rowCount(self, parent):
      if parent.isValid():
         return 0
      else:
         return len(self.mClusterConfig.mNodes)

class ClusterSettings(QtGui.QWidget, ClusterSettingsBase.Ui_ClusterSettingsBase):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)
      self.mClusterConfig = None
      self.mSelectedNode = None

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
      if not None == self.mClusterConfig:
         self.mClusterConfig.refreshConnections()

   def onAdd(self):
      """ Called when user presses the add button. """
      if not None == self.mClusterConfig:
         new_node = self.mClusterConfig.addNode()
         self.mClusterListView.clearSelection()
         self.mSelectedNode = None
         self.onNewConnections()

   def onRemove(self):
      """ Called when user presses the remove button. """
      if (not None == self.mClusterConfig) and (not None == self.mSelectedNode):
         self.mClusterListView.clearSelection()
         self.mClusterConfig.removeNode(self.mSelectedNode)
         self.mSelectedNode = None
         self.onNewConnections()

   def nodeSettingsChanged(self):
      """ Apply any user changes. """

      # Can't get a change if a node is not selected
      assert not None == self.mSelectedNode

      modified = False
      # Process changes
      if self.mNameEdit.isModified():
         self.mSelectedNode.setName(str(self.mNameEdit.text()))
         self.mNameEdit.setModified(False)
         modified = True

      if self.mHostnameEdit.isModified():
         self.mSelectedNode.setHostname(str(self.mHostnameEdit.text()))
         self.mHostnameEdit.setModified(False)
         modified = True

         # Disconnect and try to connect to new hostname.
         self.mSelectedNode.disconnect()
         self.mClusterConfig.refreshConnections()

      # Only update gui if something really changed.
      if modified:
         self.refreshNodeInfo()
         self.mClusterListView.reset()

   def onNodeSelected(self):
      """ Called when a cluster node in the list is selected. """
      node = self.mClusterListView.model().data(self.mClusterListView.currentIndex(), QtCore.Qt.UserRole)
      self.mSelectedNode = node
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
      if None == self.mSelectedNode:
         return
      
      # Set node information that we know
      self.mNameEdit.setText(self.mSelectedNode.getName())
      self.mHostnameEdit.setText(self.mSelectedNode.getHostname())

      # Get IP address
      try:
         (hostname, alias_list, ipaddrlist) = socket.gethostbyaddr(self.mSelectedNode.getHostname())
         self.mIpAddressEdit.setText(ipaddrlist[0])
      except:
         self.mIpAddressEdit.setText('Unknown')

      # Get information from proxy
      if not None == self.mSelectedNode.proxy():
         # Get operating system
         try:
            platform = self.mSelectedNode.proxy().getService("Settings").getPlatformName()
            self.mCurrentOsEdit.setText(platform)
         except:
            self.mCurrentOsEdit.setText("Unknown")

   def onNewConnections(self):
      self.mClusterListView.reset()
      self.refreshNodeInfo()

   def configure(self, clusterConfig):
      """ Configure the user interface with data in cluster configuration. """
      # Set the new cluster configuration
      if not None == self.mClusterConfig:
         self.disconnect(self.mClusterConfig, QtCore.SIGNAL("newConnections()"), self.onNewConnections)
      self.mClusterConfig = clusterConfig
      self.connect(self.mClusterConfig, QtCore.SIGNAL("newConnections()"), self.onNewConnections)

      self.mClusterModel = ClusterModel(clusterConfig)

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

