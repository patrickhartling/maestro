# Copyright (C) Infiscape Corporation 2006

import sys
from PyQt4 import QtGui, QtCore
import ClusterSettingsBase
import ClusterSettingsResource

#class ClusterTableModel(QAbstractTableModel):
#   pass

class Ui_ClusterSettings(ClusterSettingsBase.Ui_Form):
   def setupUi(self, Form):
      ClusterSettingsBase.Ui_Form.setupUi(self, Form)
      
      self.icon = QtGui.QIcon(":/linux2.png")

   def getName():
        return "Cluster Settings"
   getName = staticmethod(getName)

def getModuleInfo():
   icon = QtGui.QIcon(":/linux2.png")
   return (Ui_ClusterSettings, icon)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   Form = QtGui.QWidget()
   ui = Ui_ClusterSettings()
   ui.setupUi(Form)
   Form.show()
   sys.exit(app.exec_())

