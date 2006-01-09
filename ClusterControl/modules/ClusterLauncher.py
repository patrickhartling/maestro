# Copyright (C) Infiscape Corporation 2006

import sys
from PyQt4 import QtGui, QtCore
import ClusterLauncherBase
import ClusterSettingsResource
#import Cluster
#class ClusterTableModel(QAbstractTableModel):
#   pass

class ClusterLauncher(QtGui.QWidget, ClusterLauncherBase.Ui_ClusterLauncherBase):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)

   def setupUi(self, widget):
      ClusterLauncherBase.Ui_ClusterLauncherBase.setupUi(self, widget)
      
      self.icon = QtGui.QIcon(":/linux2.png")

   def getName():
        return "Cluster Launcher"
   getName = staticmethod(getName)

def getModuleInfo():
   icon = QtGui.QIcon(":/linux2.png")
   return (ClusterLauncher, icon)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   cs = ClusterLauncher()
   cs.show()
   sys.exit(app.exec_())

