# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClusterControlBase.ui'
#
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

class Ui_ClusterControlBase(object):
   def setupUi(self, ClusterControlBase):
      ClusterControlBase.setObjectName("ClusterControlBase")
      ClusterControlBase.resize(QtCore.QSize(QtCore.QRect(0,0,788,711).size()).expandedTo(ClusterControlBase.minimumSizeHint()))
      
      self.centralwidget = QtGui.QWidget(ClusterControlBase)
      self.centralwidget.setObjectName("centralwidget")
      
      self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
      self.hboxlayout.setMargin(9)
      self.hboxlayout.setSpacing(6)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.hboxlayout1 = QtGui.QHBoxLayout()
      self.hboxlayout1.setMargin(0)
      self.hboxlayout1.setSpacing(6)
      self.hboxlayout1.setObjectName("hboxlayout1")
      
      self.mToolbox = QtGui.QFrame(self.centralwidget)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(1))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.mToolbox.sizePolicy().hasHeightForWidth())
      self.mToolbox.setSizePolicy(sizePolicy)
      self.mToolbox.setFrameShape(QtGui.QFrame.StyledPanel)
      self.mToolbox.setFrameShadow(QtGui.QFrame.Sunken)
      self.mToolbox.setLineWidth(3)
      self.mToolbox.setObjectName("mToolbox")
      
      self.vboxlayout = QtGui.QVBoxLayout(self.mToolbox)
      self.vboxlayout.setMargin(9)
      self.vboxlayout.setSpacing(6)
      self.vboxlayout.setObjectName("vboxlayout")
      self.hboxlayout1.addWidget(self.mToolbox)
      
      self.mStack = QtGui.QStackedWidget(self.centralwidget)
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(1))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.mStack.sizePolicy().hasHeightForWidth())
      self.mStack.setSizePolicy(sizePolicy)
      self.mStack.setObjectName("mStack")
      
      self.page = QtGui.QWidget()
      
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
      self.page.setSizePolicy(sizePolicy)
      self.page.setObjectName("page")
      
      self.vboxlayout1 = QtGui.QVBoxLayout(self.page)
      self.vboxlayout1.setMargin(9)
      self.vboxlayout1.setSpacing(6)
      self.vboxlayout1.setObjectName("vboxlayout1")
      
      self.splitter = QtGui.QSplitter(self.page)
      self.splitter.setOrientation(QtCore.Qt.Horizontal)
      self.splitter.setObjectName("splitter")
      
      self.pushButton = QtGui.QPushButton(self.splitter)
      self.pushButton.setObjectName("pushButton")
      
      self.widget = QtGui.QWidget(self.splitter)
      self.widget.setObjectName("widget")
      
      self.vboxlayout2 = QtGui.QVBoxLayout(self.widget)
      self.vboxlayout2.setMargin(0)
      self.vboxlayout2.setSpacing(6)
      self.vboxlayout2.setObjectName("vboxlayout2")
      
      self.pushButton_3 = QtGui.QPushButton(self.widget)
      self.pushButton_3.setObjectName("pushButton_3")
      self.vboxlayout2.addWidget(self.pushButton_3)
      
      self.pushButton_2 = QtGui.QPushButton(self.widget)
      self.pushButton_2.setObjectName("pushButton_2")
      self.vboxlayout2.addWidget(self.pushButton_2)
      self.vboxlayout1.addWidget(self.splitter)
      self.mStack.addWidget(self.page)
      self.hboxlayout1.addWidget(self.mStack)
      self.hboxlayout.addLayout(self.hboxlayout1)
      ClusterControlBase.setCentralWidget(self.centralwidget)
      
      self.menubar = QtGui.QMenuBar(ClusterControlBase)
      self.menubar.setGeometry(QtCore.QRect(0,0,788,29))
      self.menubar.setObjectName("menubar")
      
      self.menuFile = QtGui.QMenu(self.menubar)
      self.menuFile.setObjectName("menuFile")
      
      self.menuHelp = QtGui.QMenu(self.menubar)
      self.menuHelp.setObjectName("menuHelp")
      ClusterControlBase.setMenuBar(self.menubar)
      
      self.statusbar = QtGui.QStatusBar(ClusterControlBase)
      self.statusbar.setGeometry(QtCore.QRect(0,689,788,22))
      self.statusbar.setObjectName("statusbar")
      ClusterControlBase.setStatusBar(self.statusbar)
      
      self.toolBar = QtGui.QToolBar(ClusterControlBase)
      self.toolBar.setMovable(True)
      self.toolBar.setOrientation(QtCore.Qt.Horizontal)
      self.toolBar.setObjectName("toolBar")
      ClusterControlBase.addToolBar(self.toolBar)
      
      self.mStatusWindow = QtGui.QDockWidget(ClusterControlBase)
      self.mStatusWindow.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
      self.mStatusWindow.setObjectName("mStatusWindow")
      
      self.dockWidgetContents = QtGui.QWidget(self.mStatusWindow)
      self.dockWidgetContents.setObjectName("dockWidgetContents")
      
      self.vboxlayout3 = QtGui.QVBoxLayout(self.dockWidgetContents)
      self.vboxlayout3.setMargin(9)
      self.vboxlayout3.setSpacing(6)
      self.vboxlayout3.setObjectName("vboxlayout3")
      
      self.tabWidget = QtGui.QTabWidget(self.dockWidgetContents)
      self.tabWidget.setObjectName("tabWidget")
      
      self.tab = QtGui.QWidget()
      self.tab.setObjectName("tab")
      
      self.hboxlayout2 = QtGui.QHBoxLayout(self.tab)
      self.hboxlayout2.setMargin(9)
      self.hboxlayout2.setSpacing(6)
      self.hboxlayout2.setObjectName("hboxlayout2")
      
      self.mTextEdit = QtGui.QTextEdit(self.tab)
      self.mTextEdit.setObjectName("mTextEdit")
      self.hboxlayout2.addWidget(self.mTextEdit)
      self.tabWidget.addTab(self.tab, "")
      
      self.tab_2 = QtGui.QWidget()
      self.tab_2.setObjectName("tab_2")
      
      self.hboxlayout3 = QtGui.QHBoxLayout(self.tab_2)
      self.hboxlayout3.setMargin(9)
      self.hboxlayout3.setSpacing(6)
      self.hboxlayout3.setObjectName("hboxlayout3")
      
      self.textBrowser_2 = QtGui.QTextBrowser(self.tab_2)
      self.textBrowser_2.setObjectName("textBrowser_2")
      self.hboxlayout3.addWidget(self.textBrowser_2)
      self.tabWidget.addTab(self.tab_2, "")
      self.vboxlayout3.addWidget(self.tabWidget)
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
      self.menuFile.addAction(self.actionReload)
      self.menuFile.addAction(self.actionNew)
      self.menuFile.addAction(self.actionOpen)
      self.menuFile.addAction(self.actionSave)
      self.menuFile.addAction(self.actionSave_As)
      self.menuFile.addSeparator()
      self.menuFile.addAction(self.action_Exit)
      self.menuHelp.addAction(self.action_About)
      self.menubar.addAction(self.menuFile.menuAction())
      self.menubar.addAction(self.menuHelp.menuAction())
      self.toolBar.addAction(self.actionReload)
      self.toolBar.addAction(self.actionNew)
      self.toolBar.addAction(self.actionOpen)
      self.toolBar.addAction(self.actionSave)
      
      self.retranslateUi(ClusterControlBase)

   
   def tr(self, string):
      return QtGui.QApplication.translate("ClusterControlBase", string, None, QtGui.QApplication.UnicodeUTF8)
   
   def retranslateUi(self, ClusterControlBase):
      ClusterControlBase.setWindowTitle(self.tr("Infiscape Cluster Control"))
      self.pushButton.setText(self.tr("PushButton"))
      self.pushButton_3.setText(self.tr("PushButton"))
      self.pushButton_2.setText(self.tr("PushButton"))
      self.menuFile.setTitle(self.tr("&File"))
      self.menuHelp.setTitle(self.tr("&Help"))
      self.toolBar.setWindowTitle(self.tr("Toolbar"))
      self.mStatusWindow.setWindowTitle(self.tr("Status Window"))
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

