# Copyright (C) Infiscape Corporation 2006

import sys
from PyQt4 import QtGui, QtCore
import TestSettingsBase
import ClusterSettingsResource

#class ClusterTableModel(QAbstractTableModel):
#   pass

class TestSettings(QtGui.QWidget, TestSettingsBase.Ui_Form):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)

   def setupUi(self, widget):
      TestSettingsBase.Ui_Form.setupUi(self, widget)
      
      self.icon = QtGui.QIcon(":/linux2.png")

   def getName():
        return "Cluster Settings"
   getName = staticmethod(getName)

def getModuleInfo():
   icon = QtGui.QIcon(":/linux2.png")
   return (TestSettings, icon)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   Form = QtGui.QWidget()
   ts = TestSettings()
   ts.show()
   sys.exit(app.exec_())

