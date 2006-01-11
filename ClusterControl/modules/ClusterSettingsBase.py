# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules/ClusterSettingsBase.ui'
#
# Created: Tue Jan 10 18:31:40 2006
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

class Ui_ClusterSettingsBase(object):
   def setupUi(self, ClusterSettingsBase):
      ClusterSettingsBase.setObjectName("ClusterSettingsBase")
      ClusterSettingsBase.resize(QtCore.QSize(QtCore.QRect(0,0,740,591).size()).expandedTo(ClusterSettingsBase.minimumSizeHint()))
      
      self.hboxlayout = QtGui.QHBoxLayout(ClusterSettingsBase)
      self.hboxlayout.setMargin(9)
      self.hboxlayout.setSpacing(6)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.vboxlayout = QtGui.QVBoxLayout()
      self.vboxlayout.setMargin(0)
      self.vboxlayout.setSpacing(6)
      self.vboxlayout.setObjectName("vboxlayout")
      
      self.listView = QtGui.QListView(ClusterSettingsBase)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
      self.listView.setSizePolicy(sizePolicy)
      self.listView.setObjectName("listView")
      self.vboxlayout.addWidget(self.listView)
      
      self.hboxlayout1 = QtGui.QHBoxLayout()
      self.hboxlayout1.setMargin(0)
      self.hboxlayout1.setSpacing(6)
      self.hboxlayout1.setObjectName("hboxlayout1")
      
      spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Minimum)
      self.hboxlayout1.addItem(spacerItem)
      
      self.refreshButton = QtGui.QPushButton(ClusterSettingsBase)
      self.refreshButton.setObjectName("refreshButton")
      self.hboxlayout1.addWidget(self.refreshButton)
      
      self.mRemoveBtn = QtGui.QPushButton(ClusterSettingsBase)
      self.mRemoveBtn.setObjectName("mRemoveBtn")
      self.hboxlayout1.addWidget(self.mRemoveBtn)
      
      self.mRemoveBtn1 = QtGui.QPushButton(ClusterSettingsBase)
      self.mRemoveBtn1.setObjectName("mRemoveBtn1")
      self.hboxlayout1.addWidget(self.mRemoveBtn1)
      self.vboxlayout.addLayout(self.hboxlayout1)
      self.hboxlayout.addLayout(self.vboxlayout)
      
      self.vboxlayout1 = QtGui.QVBoxLayout()
      self.vboxlayout1.setMargin(0)
      self.vboxlayout1.setSpacing(6)
      self.vboxlayout1.setObjectName("vboxlayout1")
      
      self.mClusterGroup = QtGui.QGroupBox(ClusterSettingsBase)
      self.mClusterGroup.setObjectName("mClusterGroup")
      self.vboxlayout1.addWidget(self.mClusterGroup)
      
      self.mNodeGroup = QtGui.QGroupBox(ClusterSettingsBase)
      self.mNodeGroup.setObjectName("mNodeGroup")
      
      self.label = QtGui.QLabel(self.mNodeGroup)
      self.label.setGeometry(QtCore.QRect(12,29,163,70))
      self.label.setObjectName("label")
      
      self.label_3 = QtGui.QLabel(self.mNodeGroup)
      self.label_3.setGeometry(QtCore.QRect(12,105,163,69))
      self.label_3.setObjectName("label_3")
      
      self.label_5 = QtGui.QLabel(self.mNodeGroup)
      self.label_5.setGeometry(QtCore.QRect(12,180,163,70))
      self.label_5.setObjectName("label_5")
      
      self.label_2 = QtGui.QLabel(self.mNodeGroup)
      self.label_2.setGeometry(QtCore.QRect(181,29,163,70))
      self.label_2.setObjectName("label_2")
      
      self.label_4 = QtGui.QLabel(self.mNodeGroup)
      self.label_4.setGeometry(QtCore.QRect(181,105,163,69))
      self.label_4.setObjectName("label_4")
      
      self.label_6 = QtGui.QLabel(self.mNodeGroup)
      self.label_6.setGeometry(QtCore.QRect(181,180,163,70))
      self.label_6.setObjectName("label_6")
      self.vboxlayout1.addWidget(self.mNodeGroup)
      self.hboxlayout.addLayout(self.vboxlayout1)
      
      self.retranslateUi(ClusterSettingsBase)

   
   def tr(self, string):
      return QtGui.QApplication.translate("ClusterSettingsBase", string, None, QtGui.QApplication.UnicodeUTF8)
   
   def retranslateUi(self, ClusterSettingsBase):
      ClusterSettingsBase.setWindowTitle(self.tr("Cluster Settings"))
      self.refreshButton.setText(self.tr("&Refresh"))
      self.mRemoveBtn.setToolTip(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add a cluster node.</p></body></html>"))
      self.mRemoveBtn.setWhatsThis(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add a cluster node.</p></body></html>"))
      self.mRemoveBtn.setText(self.tr("Add"))
      self.mRemoveBtn1.setToolTip(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove selected cluster node.</p></body></html>"))
      self.mRemoveBtn1.setWhatsThis(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove selected cluster node.</p></body></html>"))
      self.mRemoveBtn1.setText(self.tr("Remove"))
      self.mClusterGroup.setTitle(self.tr("Cluster Settings"))
      self.mNodeGroup.setTitle(self.tr("Node Settings"))
      self.label.setText(self.tr("Hostname:"))
      self.label_3.setText(self.tr("IP Address:"))
      self.label_5.setText(self.tr("Current OS:"))
      self.label_2.setText(self.tr("timmy.infiscape.com"))
      self.label_4.setText(self.tr("192.168.1.188"))
      self.label_6.setText(self.tr("Linux"))

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   ClusterSettingsBase = QtGui.QWidget()
   ui = Ui_ClusterSettingsBase()
   ui.setupUi(ClusterSettingsBase)
   ClusterSettingsBase.show()
   sys.exit(app.exec_())

