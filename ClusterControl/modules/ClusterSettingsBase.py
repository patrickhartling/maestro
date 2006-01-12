# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules/ClusterSettingsBase.ui'
#
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
      
      self.mClusterListView = QtGui.QListView(ClusterSettingsBase)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.mClusterListView.sizePolicy().hasHeightForWidth())
      self.mClusterListView.setSizePolicy(sizePolicy)
      self.mClusterListView.setObjectName("mClusterListView")
      self.vboxlayout.addWidget(self.mClusterListView)
      
      self.hboxlayout1 = QtGui.QHBoxLayout()
      self.hboxlayout1.setMargin(0)
      self.hboxlayout1.setSpacing(6)
      self.hboxlayout1.setObjectName("hboxlayout1")
      
      spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Minimum)
      self.hboxlayout1.addItem(spacerItem)
      
      self.mRefreshBtn = QtGui.QPushButton(ClusterSettingsBase)
      self.mRefreshBtn.setObjectName("mRefreshBtn")
      self.hboxlayout1.addWidget(self.mRefreshBtn)
      
      self.mAddBtn = QtGui.QPushButton(ClusterSettingsBase)
      self.mAddBtn.setObjectName("mAddBtn")
      self.hboxlayout1.addWidget(self.mAddBtn)
      
      self.mRemoveBtn = QtGui.QPushButton(ClusterSettingsBase)
      self.mRemoveBtn.setObjectName("mRemoveBtn")
      self.hboxlayout1.addWidget(self.mRemoveBtn)
      self.vboxlayout.addLayout(self.hboxlayout1)
      self.hboxlayout.addLayout(self.vboxlayout)
      
      self.vboxlayout1 = QtGui.QVBoxLayout()
      self.vboxlayout1.setMargin(0)
      self.vboxlayout1.setSpacing(6)
      self.vboxlayout1.setObjectName("vboxlayout1")
      
      self.mClusterGroup = QtGui.QGroupBox(ClusterSettingsBase)
      self.mClusterGroup.setObjectName("mClusterGroup")
      
      self.gridlayout = QtGui.QGridLayout(self.mClusterGroup)
      self.gridlayout.setMargin(9)
      self.gridlayout.setSpacing(6)
      self.gridlayout.setObjectName("gridlayout")
      
      self.mMasterCB = QtGui.QComboBox(self.mClusterGroup)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.mMasterCB.sizePolicy().hasHeightForWidth())
      self.mMasterCB.setSizePolicy(sizePolicy)
      self.mMasterCB.setObjectName("mMasterCB")
      self.gridlayout.addWidget(self.mMasterCB,0,1,1,1)
      
      self.mMasterNodeLbl = QtGui.QLabel(self.mClusterGroup)
      self.mMasterNodeLbl.setObjectName("mMasterNodeLbl")
      self.gridlayout.addWidget(self.mMasterNodeLbl,0,0,1,1)
      
      spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
      self.gridlayout.addItem(spacerItem1,1,1,1,1)
      self.vboxlayout1.addWidget(self.mClusterGroup)
      
      self.mNodeGroup = QtGui.QGroupBox(ClusterSettingsBase)
      self.mNodeGroup.setObjectName("mNodeGroup")
      
      self.gridlayout1 = QtGui.QGridLayout(self.mNodeGroup)
      self.gridlayout1.setMargin(9)
      self.gridlayout1.setSpacing(6)
      self.gridlayout1.setObjectName("gridlayout1")
      
      spacerItem2 = QtGui.QSpacerItem(305,91,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
      self.gridlayout1.addItem(spacerItem2,4,1,1,1)
      
      self.mNameEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mNameEdit.setObjectName("mNameEdit")
      self.gridlayout1.addWidget(self.mNameEdit,0,1,1,1)
      
      self.mNameLbl = QtGui.QLabel(self.mNodeGroup)
      self.mNameLbl.setObjectName("mNameLbl")
      self.gridlayout1.addWidget(self.mNameLbl,0,0,1,1)
      
      self.mHostnameEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mHostnameEdit.setReadOnly(False)
      self.mHostnameEdit.setObjectName("mHostnameEdit")
      self.gridlayout1.addWidget(self.mHostnameEdit,1,1,1,1)
      
      self.mHostnameLbl = QtGui.QLabel(self.mNodeGroup)
      self.mHostnameLbl.setObjectName("mHostnameLbl")
      self.gridlayout1.addWidget(self.mHostnameLbl,1,0,1,1)
      
      self.mIpAddressEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mIpAddressEdit.setReadOnly(True)
      self.mIpAddressEdit.setObjectName("mIpAddressEdit")
      self.gridlayout1.addWidget(self.mIpAddressEdit,2,1,1,1)
      
      self.mIpAddressLbl = QtGui.QLabel(self.mNodeGroup)
      self.mIpAddressLbl.setObjectName("mIpAddressLbl")
      self.gridlayout1.addWidget(self.mIpAddressLbl,2,0,1,1)
      
      self.mCurrentOsLbl = QtGui.QLabel(self.mNodeGroup)
      self.mCurrentOsLbl.setObjectName("mCurrentOsLbl")
      self.gridlayout1.addWidget(self.mCurrentOsLbl,3,0,1,1)
      
      self.mCurrentOsEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mCurrentOsEdit.setReadOnly(True)
      self.mCurrentOsEdit.setObjectName("mCurrentOsEdit")
      self.gridlayout1.addWidget(self.mCurrentOsEdit,3,1,1,1)
      self.vboxlayout1.addWidget(self.mNodeGroup)
      self.hboxlayout.addLayout(self.vboxlayout1)
      self.mMasterNodeLbl.setBuddy(self.mMasterCB)
      self.mHostnameLbl.setBuddy(self.mHostnameEdit)
      self.mIpAddressLbl.setBuddy(self.mIpAddressEdit)
      self.mCurrentOsLbl.setBuddy(self.mCurrentOsEdit)
      
      self.retranslateUi(ClusterSettingsBase)

      ClusterSettingsBase.setTabOrder(self.mClusterListView,self.mRefreshBtn)
      ClusterSettingsBase.setTabOrder(self.mRefreshBtn,self.mAddBtn)
      ClusterSettingsBase.setTabOrder(self.mAddBtn,self.mRemoveBtn)
      ClusterSettingsBase.setTabOrder(self.mRemoveBtn,self.mMasterCB)
      ClusterSettingsBase.setTabOrder(self.mMasterCB,self.mNameEdit)
      ClusterSettingsBase.setTabOrder(self.mNameEdit,self.mHostnameEdit)
      ClusterSettingsBase.setTabOrder(self.mHostnameEdit,self.mIpAddressEdit)
      ClusterSettingsBase.setTabOrder(self.mIpAddressEdit,self.mCurrentOsEdit)
   
   def tr(self, string):
      return QtGui.QApplication.translate("ClusterSettingsBase", string, None, QtGui.QApplication.UnicodeUTF8)
   
   def retranslateUi(self, ClusterSettingsBase):
      ClusterSettingsBase.setWindowTitle(self.tr("Cluster Settings"))
      self.mRefreshBtn.setText(self.tr("&Refresh"))
      self.mAddBtn.setToolTip(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add a cluster node.</p></body></html>"))
      self.mAddBtn.setWhatsThis(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add a cluster node.</p></body></html>"))
      self.mAddBtn.setText(self.tr("Add"))
      self.mRemoveBtn.setToolTip(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove selected cluster node.</p></body></html>"))
      self.mRemoveBtn.setWhatsThis(self.tr("<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove selected cluster node.</p></body></html>"))
      self.mRemoveBtn.setText(self.tr("Remove"))
      self.mClusterGroup.setTitle(self.tr("Cluster Settings"))
      self.mMasterNodeLbl.setText(self.tr("Master Node:"))
      self.mNodeGroup.setTitle(self.tr("Node Settings"))
      self.mNameLbl.setText(self.tr("Name:"))
      self.mHostnameLbl.setText(self.tr("Hostname:"))
      self.mIpAddressLbl.setText(self.tr("IP Address:"))
      self.mCurrentOsLbl.setText(self.tr("Current OS:"))

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   ClusterSettingsBase = QtGui.QWidget()
   ui = Ui_ClusterSettingsBase()
   ui.setupUi(ClusterSettingsBase)
   ClusterSettingsBase.show()
   sys.exit(app.exec_())

