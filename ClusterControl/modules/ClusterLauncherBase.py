# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClusterLauncher.ui'
#
# Created: Mon Jan  9 14:16:40 2006
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

class Ui_ClusterLauncherBase(object):
    def setupUi(self, ClusterLauncherBase):
        ClusterLauncherBase.setObjectName("ClusterLauncherBase")
        ClusterLauncherBase.resize(QtCore.QSize(QtCore.QRect(0,0,290,368).size()).expandedTo(ClusterLauncherBase.minimumSizeHint()))
        
        self.vboxlayout = QtGui.QVBoxLayout(ClusterLauncherBase)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        
        self.appFrame = QtGui.QFrame(ClusterLauncherBase)
        self.appFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.appFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.appFrame.setObjectName("appFrame")
        
        self.vboxlayout1 = QtGui.QVBoxLayout(self.appFrame)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        
        self.appComboBox = QtGui.QComboBox(self.appFrame)
        self.appComboBox.setObjectName("appComboBox")
        self.vboxlayout1.addWidget(self.appComboBox)
        
        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.vboxlayout.addWidget(self.appFrame)
        
        self.cmdFrame = QtGui.QFrame(ClusterLauncherBase)
        self.cmdFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.cmdFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.cmdFrame.setObjectName("cmdFrame")
        
        self.vboxlayout2 = QtGui.QVBoxLayout(self.cmdFrame)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")
        
        self.launchButton = QtGui.QPushButton(self.cmdFrame)
        self.launchButton.setObjectName("launchButton")
        self.vboxlayout2.addWidget(self.launchButton)
        
        self.killButton = QtGui.QPushButton(self.cmdFrame)
        self.killButton.setEnabled(False)
        self.killButton.setObjectName("killButton")
        self.vboxlayout2.addWidget(self.killButton)
        
        self.helpButton = QtGui.QPushButton(self.cmdFrame)
        self.helpButton.setObjectName("helpButton")
        self.vboxlayout2.addWidget(self.helpButton)
        
        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem1)
        self.vboxlayout.addWidget(self.cmdFrame)
        
        self.retranslateUi(ClusterLauncherBase)

    
    def tr(self, string):
        return QtGui.QApplication.translate("ClusterLauncherBase", string, None, QtGui.QApplication.UnicodeUTF8)
    
    def retranslateUi(self, ClusterLauncherBase):
        ClusterLauncherBase.setWindowTitle(self.tr("Form"))
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

