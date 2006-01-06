# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClusterControlBase.ui'
#
# Created: Fri Jan  6 13:59:48 2006
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

class Ui_ClusterControlBase(object):
   def setupUi(self, ClusterControlBase):
      ClusterControlBase.setObjectName("ClusterControlBase")
      ClusterControlBase.resize(QtCore.QSize(QtCore.QRect(0,0,778,702).size()).expandedTo(ClusterControlBase.minimumSizeHint()))
      
      self.centralwidget = QtGui.QWidget(ClusterControlBase)
      self.centralwidget.setObjectName("centralwidget")
      
      self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
      self.vboxlayout.setMargin(9)
      self.vboxlayout.setSpacing(6)
      self.vboxlayout.setObjectName("vboxlayout")
      
      self.hboxlayout = QtGui.QHBoxLayout()
      self.hboxlayout.setMargin(0)
      self.hboxlayout.setSpacing(6)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.mToolbox = QtGui.QFrame(self.centralwidget)
      self.mToolbox.setFrameShape(QtGui.QFrame.StyledPanel)
      self.mToolbox.setFrameShadow(QtGui.QFrame.Raised)
      self.mToolbox.setObjectName("mToolbox")
      
      self.vboxlayout1 = QtGui.QVBoxLayout(self.mToolbox)
      self.vboxlayout1.setMargin(9)
      self.vboxlayout1.setSpacing(6)
      self.vboxlayout1.setObjectName("vboxlayout1")
      self.hboxlayout.addWidget(self.mToolbox)
      
      self.mStack = QtGui.QStackedWidget(self.centralwidget)
      self.mStack.setObjectName("mStack")
      
      self.page = QtGui.QWidget()
      self.page.setObjectName("page")
      self.mStack.addWidget(self.page)
      self.hboxlayout.addWidget(self.mStack)
      self.vboxlayout.addLayout(self.hboxlayout)
      ClusterControlBase.setCentralWidget(self.centralwidget)
      
      self.menubar = QtGui.QMenuBar(ClusterControlBase)
      self.menubar.setGeometry(QtCore.QRect(0,0,778,29))
      self.menubar.setObjectName("menubar")
      
      self.menuHelp = QtGui.QMenu(self.menubar)
      self.menuHelp.setObjectName("menuHelp")
      
      self.menuFile = QtGui.QMenu(self.menubar)
      self.menuFile.setObjectName("menuFile")
      ClusterControlBase.setMenuBar(self.menubar)
      
      self.statusbar = QtGui.QStatusBar(ClusterControlBase)
      self.statusbar.setGeometry(QtCore.QRect(0,680,778,22))
      self.statusbar.setObjectName("statusbar")
      ClusterControlBase.setStatusBar(self.statusbar)
      
      self.toolBar = QtGui.QToolBar(ClusterControlBase)
      self.toolBar.setOrientation(QtCore.Qt.Horizontal)
      self.toolBar.setObjectName("toolBar")
      ClusterControlBase.addToolBar(self.toolBar)
      
      self.mStatusWindow = QtGui.QDockWidget(ClusterControlBase)
      self.mStatusWindow.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
      self.mStatusWindow.setObjectName("mStatusWindow")
      
      self.dockWidgetContents = QtGui.QWidget(self.mStatusWindow)
      self.dockWidgetContents.setObjectName("dockWidgetContents")
      
      self.vboxlayout2 = QtGui.QVBoxLayout(self.dockWidgetContents)
      self.vboxlayout2.setMargin(9)
      self.vboxlayout2.setSpacing(6)
      self.vboxlayout2.setObjectName("vboxlayout2")
      
      self.tabWidget = QtGui.QTabWidget(self.dockWidgetContents)
      self.tabWidget.setObjectName("tabWidget")
      
      self.tab = QtGui.QWidget()
      self.tab.setObjectName("tab")
      self.tabWidget.addTab(self.tab, "")
      
      self.tab_2 = QtGui.QWidget()
      self.tab_2.setObjectName("tab_2")
      self.tabWidget.addTab(self.tab_2, "")
      self.vboxlayout2.addWidget(self.tabWidget)
      self.mStatusWindow.setWidget(self.dockWidgetContents)
      
      self.actionReload = QtGui.QAction(ClusterControlBase)
      self.actionReload.setObjectName("actionReload")
      
      self.actionNew = QtGui.QAction(ClusterControlBase)
      self.actionNew.setObjectName("actionNew")
      
      self.actionOpen = QtGui.QAction(ClusterControlBase)
      self.actionOpen.setObjectName("actionOpen")
      
      self.actionSave = QtGui.QAction(ClusterControlBase)
      self.actionSave.setObjectName("actionSave")
      
      self.actionSave_As = QtGui.QAction(ClusterControlBase)
      self.actionSave_As.setObjectName("actionSave_As")
      
      self.action_Exit = QtGui.QAction(ClusterControlBase)
      self.action_Exit.setObjectName("action_Exit")
      
      self.action_About = QtGui.QAction(ClusterControlBase)
      self.action_About.setObjectName("action_About")
      self.menuHelp.addAction(self.action_About)
      self.menuFile.addAction(self.actionReload)
      self.menuFile.addAction(self.actionNew)
      self.menuFile.addAction(self.actionOpen)
      self.menuFile.addAction(self.actionSave)
      self.menuFile.addAction(self.actionSave_As)
      self.menuFile.addSeparator()
      self.menuFile.addAction(self.action_Exit)
      self.menubar.addAction(self.menuFile.menuAction())
      self.menubar.addAction(self.menuHelp.menuAction())
      self.toolBar.addAction(self.actionReload)
      self.toolBar.addAction(self.actionNew)
      
      self.retranslateUi(ClusterControlBase)

   
   def tr(self, string):
      return QtGui.QApplication.translate("ClusterControlBase", string, None, QtGui.QApplication.UnicodeUTF8)
   
   def retranslateUi(self, ClusterControlBase):
      ClusterControlBase.setWindowTitle(self.tr("Infiscape Cluster Control"))
      self.menuHelp.setTitle(self.tr("&Help"))
      self.menuFile.setTitle(self.tr("&File"))
      self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), self.tr("Tab 1"))
      self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), self.tr("Tab 2"))
      self.actionReload.setText(self.tr("&Reload"))
      self.actionNew.setText(self.tr("&New"))
      self.actionOpen.setText(self.tr("&Open"))
      self.actionSave.setText(self.tr("&Save"))
      self.actionSave_As.setText(self.tr("Save &As..."))
      self.action_Exit.setText(self.tr("&Exit"))
      self.action_About.setText(self.tr("&About"))

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   ClusterControlBase = QtGui.QMainWindow()
   ui = Ui_ClusterControlBase()
   ui.setupUi(ClusterControlBase)
   ClusterControlBase.show()
   sys.exit(app.exec_())

