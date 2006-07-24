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

class SettingsModel(QtCore.QAbstractListModel):
   def __init__(self, clusterModel, parent=None):
      QtCore.QAbstractListModel.__init__(self, parent)

      self.mClusterModel = clusterModel
      self.mIcons = {}
      self.mIcons[ERROR] = QtGui.QIcon(":/ClusterSettings/images/error2.png")
      self.mIcons[WIN] = QtGui.QIcon(":/ClusterSettings/images/win_xp.png")
      self.mIcons[WINXP] = QtGui.QIcon(":/ClusterSettings/images/win_xp.png")
      self.mIcons[LINUX] = QtGui.QIcon(":/ClusterSettings/images/linux2.png")

      self.mOsMap = {}

   def data(self, index, role=QtCore.Qt.DisplayRole):
      if not index.isValid():
         return QtCore.QVariant()

      cluster_node = self.mClusterModel.mNodes[index.row()]
      if role == QtCore.Qt.DecorationRole:
         try:
            ip_address = cluster_node.getIpAddress()
            index = self.mOsMap[ip_address]
            return QtCore.QVariant(self.mIcons[index])
         except:
            return QtCore.QVariant(self.mIcons[ERROR])
      elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
         return QtCore.QVariant(str(cluster_node.getName()))
      elif role == QtCore.Qt.UserRole:
         return cluster_node
       
      return QtCore.QVariant()

   def rowCount(self, parent=QtCore.QModelIndex()):
      if parent.isValid():
         return 0
      else:
         return len(self.mClusterModel.mNodes)

   def setOperatingSystem(self, ipAddress, value):
      self.mOsMap[ipAddress] = value
      self.emit(QtCore.SIGNAL("dataChanged(QModelIndex,QModelIndex)"), QtCore.QModelIndex(), QtCore.QModelIndex())
      self.emit(QtCore.SIGNAL("dataChanged(int)"), 0)

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
      self.mTitleLbl.setBackgroundRole(QtGui.QPalette.Mid)
      self.mTitleLbl.setForegroundRole(QtGui.QPalette.Shadow)
      
      QtCore.QObject.connect(self.mRefreshBtn,QtCore.SIGNAL("clicked()"), self.onRefresh)
      QtCore.QObject.connect(self.mAddBtn,QtCore.SIGNAL("clicked()"), self.onAdd)
      QtCore.QObject.connect(self.mRemoveBtn,QtCore.SIGNAL("clicked()"), self.onRemove)
      # Call if you want an icon view
      #self.mClusterListView.setViewMode(QtGui.QListView.IconMode)
      self.connect(self.mNameEdit, QtCore.SIGNAL("editingFinished()"), self.nodeSettingsChanged)
      self.connect(self.mHostnameEdit, QtCore.SIGNAL("editingFinished()"), self.nodeSettingsChanged)
   
   def configure(self, clusterModel, eventManager, eventDispatcher):
      """ Configure the user interface with data in cluster configuration. """
      # Set the new cluster configuration
      if not None == self.mClusterModel:
         self.disconnect(self.mClusterModel, QtCore.SIGNAL("newConnections()"), self.onNewConnections)
      self.mClusterModel = clusterModel
      self.connect(self.mClusterModel, QtCore.SIGNAL("newConnections()"), self.onNewConnections)
      self.mEventManager = eventManager
      self.mEventDispatcher = eventDispatcher

      self.mEventManager.connect("*", "settings.os", self.onReportOs)


      self.mSettingsModel = SettingsModel(self.mClusterModel)


      # If selection model already exists then disconnect signal
      if not None == self.mClusterListView.selectionModel():
         QtCore.QObject.disconnect(self.mClusterListView.selectionModel(),
            QtCore.SIGNAL("currentChanged(QModelIndex,QModelIndex)"), self.onNodeSelected)
      self.mClusterListView.setModel(self.mSettingsModel)
      #self.mMasterCB.setModel(self.mClusterModel)

      # Connect new selection model
      QtCore.QObject.connect(self.mClusterListView.selectionModel(),
         QtCore.SIGNAL("currentChanged(QModelIndex,QModelIndex)"), self.onNodeSelected)

   def onReportOs(self, nodeId, os):
      print "onReportOs [%s] [%s]" % (nodeId, os)
      self.mSettingsModel.setOperatingSystem(nodeId, os)


   def onRefresh(self):
      """ Called when user presses the refresh button. """
      print "onRefresh"
      if not None == self.mClusterModel:
         self.mClusterModel.refreshConnections()

      self.mEventDispatcher.emit("*", "settings.get_os", ())

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
         #self.refreshNodeInfo()
         # Force the cluster model to generate a dataChanged signal.
         self.mClusterListView.model().setData(self.mClusterListView.currentIndex(), QtCore.QVariant(), QtCore.Qt.DisplayRole)
   
      #def refreshNodeInfo(self):
      #"""
      #Fills in the node information for the currently selected node. This gets called
      #whenever a new node is selected in the list.
      #"""

   def onNodeSelected(self, selected, deselected):
      """ Called when a cluster node in the list is selected. """
      #self.refreshNodeInfo()


      self.mNameEdit.clear()
      self.mHostnameEdit.clear()
      self.mCurrentOsEdit.clear()
      self.mIpAddressEdit.clear()
      
      selected_indexes = self.mClusterListView.selectedIndexes()
      if len(selected_indexes) > 0:
         assert (len(selected_indexes) == 1)
         selected_index = selected_indexes[0]
         # Get the currently selected node.
         selected_node = self.mClusterModel.data(selected_index, QtCore.Qt.UserRole)

         # Set node information that we know
         self.mNameEdit.setText(selected_node.getName())
         self.mHostnameEdit.setText(selected_node.getHostname())

         # Get IP address
         try:
            self.mIpAddressEdit.setText(selected_node.getIpAddress())
         except:
            self.mIpAddressEdit.setText('Unknown')

         # Get information from proxy
#      if not None == selected_node.proxy():
#         # Get operating system
#         try:
#            platform = selected_node.proxy().getService("Settings").getPlatformName()   
#            self.mCurrentOsEdit.setText(platform)
#         except:
#            self.mCurrentOsEdit.setText("Unknown")

   def onNewConnections(self):
      self.mClusterListView.reset()
      self.refreshNodeInfo()



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

