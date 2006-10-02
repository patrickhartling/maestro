#!/bin/env python

# Maestro is Copyright (C) 2006 by Infiscape
#
# Original Author: Aron Bierbaum
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.




import sys
from PyQt4 import QtCore, QtGui

class Ui_EnsembleViewBase(object):
   def setupUi(self, EnsembleViewBase):
      EnsembleViewBase.setObjectName("EnsembleViewBase")
      EnsembleViewBase.resize(QtCore.QSize(QtCore.QRect(0,0,742,489).size()).expandedTo(EnsembleViewBase.minimumSizeHint()))

      self.vboxlayout = QtGui.QVBoxLayout(EnsembleViewBase)
      self.vboxlayout.setMargin(9)
      self.vboxlayout.setSpacing(6)
      self.vboxlayout.setObjectName("vboxlayout")

      self.mTitleLbl = QtGui.QLabel(EnsembleViewBase)

      font = QtGui.QFont(self.mTitleLbl.font())
      font.setFamily("Sans Serif")
      font.setPointSize(12)
      font.setWeight(50)
      font.setItalic(False)
      font.setUnderline(False)
      font.setStrikeOut(False)
      font.setBold(False)
      self.mTitleLbl.setFont(font)
      self.mTitleLbl.setAutoFillBackground(True)
      self.mTitleLbl.setFrameShape(QtGui.QFrame.StyledPanel)
      self.mTitleLbl.setFrameShadow(QtGui.QFrame.Sunken)
      self.mTitleLbl.setLineWidth(3)
      self.mTitleLbl.setObjectName("mTitleLbl")
      self.vboxlayout.addWidget(self.mTitleLbl)

      self.hboxlayout = QtGui.QHBoxLayout()
      self.hboxlayout.setMargin(0)
      self.hboxlayout.setSpacing(6)
      self.hboxlayout.setObjectName("hboxlayout")

      self.vboxlayout1 = QtGui.QVBoxLayout()
      self.vboxlayout1.setMargin(0)
      self.vboxlayout1.setSpacing(6)
      self.vboxlayout1.setObjectName("vboxlayout1")

      self.mClusterListView = QtGui.QListView(EnsembleViewBase)

      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.mClusterListView.sizePolicy().hasHeightForWidth())
      self.mClusterListView.setSizePolicy(sizePolicy)
      self.mClusterListView.setObjectName("mClusterListView")
      self.vboxlayout1.addWidget(self.mClusterListView)

      self.hboxlayout1 = QtGui.QHBoxLayout()
      self.hboxlayout1.setMargin(0)
      self.hboxlayout1.setSpacing(6)
      self.hboxlayout1.setObjectName("hboxlayout1")

      spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Minimum)
      self.hboxlayout1.addItem(spacerItem)

      self.mRefreshBtn = QtGui.QPushButton(EnsembleViewBase)
      self.mRefreshBtn.setObjectName("mRefreshBtn")
      self.hboxlayout1.addWidget(self.mRefreshBtn)

      self.mAddBtn = QtGui.QPushButton(EnsembleViewBase)
      self.mAddBtn.setObjectName("mAddBtn")
      self.hboxlayout1.addWidget(self.mAddBtn)

      self.mRemoveBtn = QtGui.QPushButton(EnsembleViewBase)
      self.mRemoveBtn.setObjectName("mRemoveBtn")
      self.hboxlayout1.addWidget(self.mRemoveBtn)
      self.vboxlayout1.addLayout(self.hboxlayout1)
      self.hboxlayout.addLayout(self.vboxlayout1)

      self.vboxlayout2 = QtGui.QVBoxLayout()
      self.vboxlayout2.setMargin(0)
      self.vboxlayout2.setSpacing(6)
      self.vboxlayout2.setObjectName("vboxlayout2")

      self.mNodeGroup = QtGui.QGroupBox(EnsembleViewBase)
      self.mNodeGroup.setObjectName("mNodeGroup")

      self.gridlayout = QtGui.QGridLayout(self.mNodeGroup)
      self.gridlayout.setMargin(9)
      self.gridlayout.setSpacing(6)
      self.gridlayout.setObjectName("gridlayout")

      self.mHostnameLbl = QtGui.QLabel(self.mNodeGroup)
      self.mHostnameLbl.setObjectName("mHostnameLbl")
      self.gridlayout.addWidget(self.mHostnameLbl,1,0,1,1)

      self.mIpAddressEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mIpAddressEdit.setAutoFillBackground(False)
      self.mIpAddressEdit.setReadOnly(True)
      self.mIpAddressEdit.setObjectName("mIpAddressEdit")
      self.gridlayout.addWidget(self.mIpAddressEdit,2,1,1,1)

      self.mNameLbl = QtGui.QLabel(self.mNodeGroup)
      self.mNameLbl.setObjectName("mNameLbl")
      self.gridlayout.addWidget(self.mNameLbl,0,0,1,1)

      self.mHostnameEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mHostnameEdit.setReadOnly(False)
      self.mHostnameEdit.setObjectName("mHostnameEdit")
      self.gridlayout.addWidget(self.mHostnameEdit,1,1,1,1)

      self.mCurrentOsEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mCurrentOsEdit.setAutoFillBackground(True)
      self.mCurrentOsEdit.setReadOnly(True)
      self.mCurrentOsEdit.setObjectName("mCurrentOsEdit")
      self.gridlayout.addWidget(self.mCurrentOsEdit,3,1,1,1)

      self.mIpAddressLbl = QtGui.QLabel(self.mNodeGroup)
      self.mIpAddressLbl.setObjectName("mIpAddressLbl")
      self.gridlayout.addWidget(self.mIpAddressLbl,2,0,1,1)

      self.mNameEdit = QtGui.QLineEdit(self.mNodeGroup)
      self.mNameEdit.setObjectName("mNameEdit")
      self.gridlayout.addWidget(self.mNameEdit,0,1,1,1)

      self.mCurrentOsLbl = QtGui.QLabel(self.mNodeGroup)
      self.mCurrentOsLbl.setObjectName("mCurrentOsLbl")
      self.gridlayout.addWidget(self.mCurrentOsLbl,3,0,1,1)

      self.mOtherLbl = QtGui.QLabel(self.mNodeGroup)
      self.mOtherLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
      self.mOtherLbl.setObjectName("mOtherLbl")
      self.gridlayout.addWidget(self.mOtherLbl,4,0,1,1)

      self.mSettingsTableView = QtGui.QTableView(self.mNodeGroup)
      self.mSettingsTableView.setObjectName("mSettingsTableView")
      self.gridlayout.addWidget(self.mSettingsTableView,4,1,1,1)
      self.vboxlayout2.addWidget(self.mNodeGroup)
      self.hboxlayout.addLayout(self.vboxlayout2)
      self.vboxlayout.addLayout(self.hboxlayout)
      self.mHostnameLbl.setBuddy(self.mHostnameEdit)
      self.mIpAddressLbl.setBuddy(self.mIpAddressEdit)
      self.mCurrentOsLbl.setBuddy(self.mCurrentOsEdit)

      self.retranslateUi(EnsembleViewBase)
      QtCore.QMetaObject.connectSlotsByName(EnsembleViewBase)
      EnsembleViewBase.setTabOrder(self.mClusterListView,self.mRefreshBtn)
      EnsembleViewBase.setTabOrder(self.mRefreshBtn,self.mAddBtn)
      EnsembleViewBase.setTabOrder(self.mAddBtn,self.mRemoveBtn)
      EnsembleViewBase.setTabOrder(self.mRemoveBtn,self.mNameEdit)
      EnsembleViewBase.setTabOrder(self.mNameEdit,self.mHostnameEdit)
      EnsembleViewBase.setTabOrder(self.mHostnameEdit,self.mIpAddressEdit)
      EnsembleViewBase.setTabOrder(self.mIpAddressEdit,self.mCurrentOsEdit)

   def retranslateUi(self, EnsembleViewBase):
      EnsembleViewBase.setWindowTitle(QtGui.QApplication.translate("EnsembleViewBase", "Ensemble View", None, QtGui.QApplication.UnicodeUTF8))
      self.mTitleLbl.setText(QtGui.QApplication.translate("EnsembleViewBase", "Cluster Management", None, QtGui.QApplication.UnicodeUTF8))
      self.mRefreshBtn.setText(QtGui.QApplication.translate("EnsembleViewBase", "&Refresh", None, QtGui.QApplication.UnicodeUTF8))
      self.mAddBtn.setToolTip(QtGui.QApplication.translate("EnsembleViewBase", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add a cluster node.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
      self.mAddBtn.setWhatsThis(QtGui.QApplication.translate("EnsembleViewBase", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Add a cluster node.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
      self.mAddBtn.setText(QtGui.QApplication.translate("EnsembleViewBase", "Add", None, QtGui.QApplication.UnicodeUTF8))
      self.mRemoveBtn.setToolTip(QtGui.QApplication.translate("EnsembleViewBase", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove selected cluster node.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
      self.mRemoveBtn.setWhatsThis(QtGui.QApplication.translate("EnsembleViewBase", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Sans Serif; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Remove selected cluster node.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
      self.mRemoveBtn.setText(QtGui.QApplication.translate("EnsembleViewBase", "Remove", None, QtGui.QApplication.UnicodeUTF8))
      self.mNodeGroup.setTitle(QtGui.QApplication.translate("EnsembleViewBase", "Node Settings", None, QtGui.QApplication.UnicodeUTF8))
      self.mHostnameLbl.setText(QtGui.QApplication.translate("EnsembleViewBase", "Hostname:", None, QtGui.QApplication.UnicodeUTF8))
      self.mNameLbl.setText(QtGui.QApplication.translate("EnsembleViewBase", "Name:", None, QtGui.QApplication.UnicodeUTF8))
      self.mIpAddressLbl.setText(QtGui.QApplication.translate("EnsembleViewBase", "IP Address:", None, QtGui.QApplication.UnicodeUTF8))
      self.mCurrentOsLbl.setText(QtGui.QApplication.translate("EnsembleViewBase", "Current OS:", None, QtGui.QApplication.UnicodeUTF8))
      self.mOtherLbl.setText(QtGui.QApplication.translate("EnsembleViewBase", "Other:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   EnsembleViewBase = QtGui.QWidget()
   ui = Ui_EnsembleViewBase()
   ui.setupUi(EnsembleViewBase)
   EnsembleViewBase.show()
   sys.exit(app.exec_())