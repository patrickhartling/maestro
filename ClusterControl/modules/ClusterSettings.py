# Copyright (C) Infiscape Corporation 2006

import sys
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
      self.mIcons[ERROR] = QtGui.QIcon(":/win_xp.png")
      self.mIcons[LINUX] = QtGui.QIcon(":/linux2.png")

   def data(self, index, role=QtCore.Qt.DisplayRole):
      if not index.isValid():
         return QtCore.QVariant()
        
      if role == QtCore.Qt.DecorationRole:
         cluster_node = self.mClusterConfig.mNodes[index.row()]
         try:
            index = cluster_node.proxy().getPlatform()
            return QtCore.QVariant(self.mIcons[index])
         except:
            return QtCore.QVariant(self.mIcons[ERROR])

      elif role == QtCore.Qt.DisplayRole:
         return QtCore.QVariant(str(self.mClusterConfig.mNodes[index.row()].getName()))
       
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

   def setupUi(self, widget):
      ClusterSettingsBase.Ui_ClusterSettingsBase.setupUi(self, widget)
      QtCore.QObject.connect(self.refreshButton,QtCore.SIGNAL("clicked()"), self.onRefresh)
      self.icon = QtGui.QIcon(":/linux2.png")

   def onRefresh(self):
      if not None == self.mClusterConfig:
         self.mClusterConfig.refreshConnections()
         self.listView.reset()

   def configure(self, clusterConfig):
      self.mClusterConfig = clusterConfig
      self.cluster_model = ClusterModel(clusterConfig)
      self.listView.setModel(self.cluster_model)

   def getName():
        return "Cluster Settings"
   getName = staticmethod(getName)

def getModuleInfo():
   icon = QtGui.QIcon(":/linux2.png")
   return (ClusterSettings, icon)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   cs = ClusterSettings()
   cs.show()
   sys.exit(app.exec_())

