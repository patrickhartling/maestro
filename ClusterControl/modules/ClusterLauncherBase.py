# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules/ClusterLauncherBase.ui'
#
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

class Ui_ClusterLauncherBase(object):
   def setupUi(self, ClusterLauncherBase):
      ClusterLauncherBase.setObjectName("ClusterLauncherBase")
      ClusterLauncherBase.resize(QtCore.QSize(QtCore.QRect(0,0,635,563).size()).expandedTo(ClusterLauncherBase.minimumSizeHint()))
      
      self.vboxlayout = QtGui.QVBoxLayout(ClusterLauncherBase)
      self.vboxlayout.setMargin(9)
      self.vboxlayout.setSpacing(6)
      self.vboxlayout.setObjectName("vboxlayout")
      
      self.mTitleLbl = QtGui.QLabel(ClusterLauncherBase)
      
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
      self.mTitleLbl.setLineWidth(2)
      self.mTitleLbl.setObjectName("mTitleLbl")
      self.vboxlayout.addWidget(self.mTitleLbl)
      
      self.mAppFrame = QtGui.QFrame(ClusterLauncherBase)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(1)
      sizePolicy.setHeightForWidth(self.mAppFrame.sizePolicy().hasHeightForWidth())
      self.mAppFrame.setSizePolicy(sizePolicy)
      self.mAppFrame.setFrameShape(QtGui.QFrame.StyledPanel)
      self.mAppFrame.setFrameShadow(QtGui.QFrame.Raised)
      self.mAppFrame.setObjectName("mAppFrame")
      
      self.vboxlayout1 = QtGui.QVBoxLayout(self.mAppFrame)
      self.vboxlayout1.setMargin(9)
      self.vboxlayout1.setSpacing(6)
      self.vboxlayout1.setObjectName("vboxlayout1")
      
      self.appComboBox = QtGui.QComboBox(self.mAppFrame)
      self.appComboBox.setObjectName("appComboBox")
      self.vboxlayout1.addWidget(self.appComboBox)
      
      spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
      self.vboxlayout1.addItem(spacerItem)
      self.vboxlayout.addWidget(self.mAppFrame)
      
      self.cmdFrame = QtGui.QFrame(ClusterLauncherBase)
      self.cmdFrame.setFrameShape(QtGui.QFrame.StyledPanel)
      self.cmdFrame.setFrameShadow(QtGui.QFrame.Raised)
      self.cmdFrame.setObjectName("cmdFrame")
      
      self.hboxlayout = QtGui.QHBoxLayout(self.cmdFrame)
      self.hboxlayout.setMargin(9)
      self.hboxlayout.setSpacing(6)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.launchButton = QtGui.QPushButton(self.cmdFrame)
      self.launchButton.setObjectName("launchButton")
      self.hboxlayout.addWidget(self.launchButton)
      
      self.killButton = QtGui.QPushButton(self.cmdFrame)
      self.killButton.setEnabled(True)
      self.killButton.setObjectName("killButton")
      self.hboxlayout.addWidget(self.killButton)
      
      self.helpButton = QtGui.QPushButton(self.cmdFrame)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
      self.helpButton.setSizePolicy(sizePolicy)
      self.helpButton.setObjectName("helpButton")
      self.hboxlayout.addWidget(self.helpButton)
      
      spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
      self.hboxlayout.addItem(spacerItem1)
      self.vboxlayout.addWidget(self.cmdFrame)
      
      self.retranslateUi(ClusterLauncherBase)

   
   def tr(self, string):
      return QtGui.QApplication.translate("ClusterLauncherBase", string, None, QtGui.QApplication.UnicodeUTF8)
   
   def retranslateUi(self, ClusterLauncherBase):
      ClusterLauncherBase.setWindowTitle(self.tr("Form"))
      self.mTitleLbl.setText(self.tr("Application Launcher"))
      self.launchButton.setText(self.tr("&Launch"))
      self.killButton.setText(self.tr("&Kill Application"))
      self.helpButton.setText(self.tr("&Help"))

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   ClusterLauncherBase = QtGui.QWidget()
   ui = Ui_ClusterLauncherBase()
   ui.setupUi(ClusterLauncherBase)
   ClusterLauncherBase.show()
   sys.exit(app.exec_())

