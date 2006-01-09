# Copyright (C) Infiscape Corporation 2006

import sys
from PyQt4 import QtGui, QtCore
import ClusterSettingsBase
import ClusterSettingsResource
import Helpers
#class ClusterTableModel(QAbstractTableModel):
#   pass

class ClusterSettings(QtGui.QWidget, ClusterSettingsBase.Ui_ClusterSettingsBase):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)

   def setupUi(self, widget):
      ClusterSettingsBase.Ui_ClusterSettingsBase.setupUi(self, widget)
      
      c = Helpers.ClusterModel(self.listView)
      self.listView.setModel(c)
      self.icon = QtGui.QIcon(":/linux2.png")

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

