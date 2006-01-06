# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules/ClusterSettingsBase.ui'
#
# Created: Fri Jan  6 15:59:12 2006
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

class Ui_ClusterSettings(object):
   def setupUi(self, ClusterSettings):
      ClusterSettings.setObjectName("ClusterSettings")
      ClusterSettings.resize(QtCore.QSize(QtCore.QRect(0,0,665,362).size()).expandedTo(ClusterSettings.minimumSizeHint()))
      
      self.hboxlayout = QtGui.QHBoxLayout(ClusterSettings)
      self.hboxlayout.setMargin(9)
      self.hboxlayout.setSpacing(6)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.hboxlayout1 = QtGui.QHBoxLayout()
      self.hboxlayout1.setMargin(0)
      self.hboxlayout1.setSpacing(6)
      self.hboxlayout1.setObjectName("hboxlayout1")
      
      self.listView = QtGui.QListView(ClusterSettings)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
      self.listView.setSizePolicy(sizePolicy)
      self.listView.setObjectName("listView")
      self.hboxlayout1.addWidget(self.listView)
      
      self.vboxlayout = QtGui.QVBoxLayout()
      self.vboxlayout.setMargin(0)
      self.vboxlayout.setSpacing(6)
      self.vboxlayout.setObjectName("vboxlayout")
      
      self.mClusterGroup = QtGui.QGroupBox(ClusterSettings)
      self.mClusterGroup.setObjectName("mClusterGroup")
      self.vboxlayout.addWidget(self.mClusterGroup)
      
      self.mNodeGroup = QtGui.QGroupBox(ClusterSettings)
      self.mNodeGroup.setObjectName("mNodeGroup")
      self.vboxlayout.addWidget(self.mNodeGroup)
      self.hboxlayout1.addLayout(self.vboxlayout)
      self.hboxlayout.addLayout(self.hboxlayout1)
      
      self.retranslateUi(ClusterSettings)

   
   def tr(self, string):
      return QtGui.QApplication.translate("ClusterSettings", string, None, QtGui.QApplication.UnicodeUTF8)
   
   def retranslateUi(self, ClusterSettings):
      ClusterSettings.setWindowTitle(self.tr("Cluster Settings"))
      self.mClusterGroup.setTitle(self.tr("Cluster Settings"))
      self.mNodeGroup.setTitle(self.tr("Node Settings"))

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   ClusterSettings = QtGui.QWidget()
   ui = Ui_ClusterSettings()
   ui.setupUi(ClusterSettings)
   ClusterSettings.show()
   sys.exit(app.exec_())

