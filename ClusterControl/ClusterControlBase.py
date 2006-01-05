# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClusterControlBase.ui'
#
# Created: Thu Jan 5 14:07:27 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
    "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
    "\x99\x49\x44\x41\x54\x38\x8d\xed\x94\x41\x0e\x85" \
    "\x20\x0c\x44\x5f\x89\xc7\x36\x7f\x61\xbc\x77\x5d" \
    "\x28\x48\xa4\x28\x60\xff\xce\xd9\x54\x8b\xbe\x8e" \
    "\x13\x04\x3e\x1d\x92\x81\x77\xf4\x81\xa1\x23\xdc" \
    "\x2b\x34\xf6\xf4\x7a\x3d\xe2\xb8\x65\xa8\x84\x3f" \
    "\x40\x01\x98\x2a\x0b\x3d\x5f\x62\xc5\x83\x00\xaa" \
    "\x1a\xd7\x05\x50\x44\x9a\xb9\xd5\x07\xa7\x73\xa8" \
    "\xa4\xba\x4f\x92\xa2\xdf\x33\x3c\x64\xc6\x3b\xeb" \
    "\xbd\x82\xe5\xb8\xad\xde\xcb\xcc\x78\x20\xeb\x42" \
    "\x66\xc6\x39\x74\x5d\xfa\x80\xf3\x6f\xaf\x66\xc6" \
    "\x6f\xa1\x9c\x3f\x88\x2f\xb4\x70\xec\x05\xcd\xc0" \
    "\xbe\xd0\x78\x93\xf6\x8e\x17\x14\x92\x63\x5f\x68" \
    "\x6c\x3e\xef\xf6\xba\x3c\x8f\xdd\x36\x6d\xc4\xc0" \
    "\x45\x2c\x87\x81\xf8\x08\x00\x00\x00\x00\x49\x45" \
    "\x4e\x44\xae\x42\x60\x82"
image1_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
    "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
    "\x74\x49\x44\x41\x54\x38\x8d\xed\xd5\xc1\x09\xc0" \
    "\x20\x0c\x05\xd0\x6f\xe9\x36\x81\x2c\x10\xb2\xff" \
    "\xdd\x85\xd2\x53\x85\xb6\xa9\x91\x48\x0f\x05\x3f" \
    "\x08\x1a\xf0\x29\x12\x10\xf8\x28\xc5\xa9\xd9\xc4" \
    "\xde\x96\xcd\x2b\x9a\xd9\xeb\x00\x00\x66\x0e\x2f" \
    "\xe0\xc2\x51\x98\x39\xc4\xf7\x0c\x4c\x44\x6d\x5e" \
    "\x6b\x35\x38\xcf\x92\x82\x45\xe4\xb2\xf6\xf0\x14" \
    "\xac\xaa\x8f\xda\x1d\x4f\xc1\xa5\x74\x1b\x22\x07" \
    "\x9f\x9d\x11\x1d\x96\xea\x8a\x91\x2c\x78\xc1\x0b" \
    "\xee\x64\xe6\x07\x19\xf5\x7e\x92\x03\xad\x45\x2a" \
    "\x04\xcc\x4e\x50\x20\x00\x00\x00\x00\x49\x45\x4e" \
    "\x44\xae\x42\x60\x82"
image2_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
    "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
    "\xa0\x49\x44\x41\x54\x38\x8d\xd5\x95\x4d\x0a\x80" \
    "\x20\x10\x85\x9f\xd1\x46\x68\xe1\x8d\xe6\x62\xd2" \
    "\x22\xbc\x98\x37\x6a\x21\xb4\xac\x45\x19\x92\xc6" \
    "\x64\x69\xe0\xb7\xf1\x87\xf1\xf1\x1c\x47\x05\x2a" \
    "\x21\x8e\x76\x2d\xad\xdb\xfb\x9e\x99\xf6\x56\x8f" \
    "\x80\xb5\x36\x4b\x85\x88\xce\x35\x44\x04\x00\xe8" \
    "\x0a\x39\x8c\xe8\xf9\x90\x34\xd2\x29\x2c\xc3\x7c" \
    "\x8e\xbd\x53\x0f\xeb\x58\x3a\x05\xe9\x54\x34\x1f" \
    "\x8a\x02\x7b\x2a\x7d\x3a\x1f\x09\xbf\x85\x4d\xc5" \
    "\xd5\xd9\x53\xaa\x39\x6e\x4f\x38\xca\xb1\x99\xe2" \
    "\xd2\xe1\x08\xab\xe1\x56\xf8\x2e\x30\x97\x7f\xcb" \
    "\x4d\x8f\xf9\x42\xd7\x5d\xbe\xbe\xd2\xe1\x43\x95" \
    "\x3a\x93\xf6\xca\xad\x3d\x61\x11\xf4\x4b\x7d\x4f" \
    "\x82\x0f\xf9\xc0\x06\x9b\xb5\x1e\xcd\xed\x31\x8c" \
    "\x5c\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60" \
    "\x82"

class ClusterControlBase(QMainWindow):
    def __init__(self,parent = None,name = None,fl = 0):
        QMainWindow.__init__(self,parent,name,fl)
        self.statusBar()

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        self.image1 = QPixmap()
        self.image1.loadFromData(image1_data,"PNG")
        self.image2 = QPixmap()
        self.image2.loadFromData(image2_data,"PNG")
        if not name:
            self.setName("ClusterControlBase")


        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        ClusterControlBaseLayout = QHBoxLayout(self.centralWidget(),11,6,"ClusterControlBaseLayout")

        self.mToolbox = QButtonGroup(self.centralWidget(),"mToolbox")
        self.mToolbox.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.mToolbox.sizePolicy().hasHeightForWidth()))
        self.mToolbox.setFrameShape(QButtonGroup.Panel)
        self.mToolbox.setFrameShadow(QButtonGroup.Sunken)
        self.mToolbox.setExclusive(1)
        self.mToolbox.setColumnLayout(0,Qt.Vertical)
        self.mToolbox.layout().setSpacing(6)
        self.mToolbox.layout().setMargin(11)
        mToolboxLayout = QVBoxLayout(self.mToolbox.layout())
        mToolboxLayout.setAlignment(Qt.AlignTop)
        ClusterControlBaseLayout.addWidget(self.mToolbox)

        self.mStack = QWidgetStack(self.centralWidget(),"mStack")
        self.mStack.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred,0,0,self.mStack.sizePolicy().hasHeightForWidth()))
        self.mStack.setFrameShape(QWidgetStack.GroupBoxPanel)
        self.mStack.setFrameShadow(QWidgetStack.Sunken)
        self.mStack.setLineWidth(1)
        ClusterControlBaseLayout.addWidget(self.mStack)

        self.fileReloadAction = QAction(self,"fileReloadAction")
        self.fileReloadAction.setIconSet(QIconSet(self.image0))
        self.fileNewAction = QAction(self,"fileNewAction")
        self.fileNewAction.setIconSet(QIconSet(self.image1))
        self.fileOpenAction = QAction(self,"fileOpenAction")
        self.fileOpenAction.setIconSet(QIconSet(self.image0))
        self.fileSaveAction = QAction(self,"fileSaveAction")
        self.fileSaveAction.setIconSet(QIconSet(self.image2))
        self.fileSaveAsAction = QAction(self,"fileSaveAsAction")
        self.fileExitAction = QAction(self,"fileExitAction")
        self.helpContentsAction = QAction(self,"helpContentsAction")
        self.helpIndexAction = QAction(self,"helpIndexAction")
        self.helpAboutAction = QAction(self,"helpAboutAction")


        self.toolBar = QToolBar(QString(""),self,Qt.DockTop)

        self.fileReloadAction.addTo(self.toolBar)
        self.fileNewAction.addTo(self.toolBar)
        self.fileOpenAction.addTo(self.toolBar)
        self.fileSaveAction.addTo(self.toolBar)
        self.fileSaveAsAction.addTo(self.toolBar)
        self.fileExitAction.addTo(self.toolBar)
        self.helpIndexAction.addTo(self.toolBar)
        self.helpAboutAction.addTo(self.toolBar)


        self.MenuBar = QMenuBar(self,"MenuBar")


        self.fileMenu = QPopupMenu(self)
        self.fileReloadAction.addTo(self.fileMenu)
        self.fileNewAction.addTo(self.fileMenu)
        self.fileOpenAction.addTo(self.fileMenu)
        self.fileSaveAction.addTo(self.fileMenu)
        self.fileSaveAsAction.addTo(self.fileMenu)
        self.fileMenu.insertSeparator()
        self.fileMenu.insertSeparator()
        self.fileExitAction.addTo(self.fileMenu)
        self.MenuBar.insertItem(QString(""),self.fileMenu,1)

        self.helpMenu = QPopupMenu(self)
        self.helpContentsAction.addTo(self.helpMenu)
        self.helpIndexAction.addTo(self.helpMenu)
        self.helpMenu.insertSeparator()
        self.helpAboutAction.addTo(self.helpMenu)
        self.MenuBar.insertItem(QString(""),self.helpMenu,2)


        #self.languageChange()

        self.resize(QSize(645,563).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.fileReloadAction,SIGNAL("activated()"),self.reloadModules)
        self.connect(self.fileNewAction,SIGNAL("activated()"),self.fileNew)
        self.connect(self.fileOpenAction,SIGNAL("activated()"),self.fileOpen)
        self.connect(self.fileSaveAction,SIGNAL("activated()"),self.fileSave)
        self.connect(self.fileSaveAsAction,SIGNAL("activated()"),self.fileSaveAs)
        self.connect(self.fileExitAction,SIGNAL("activated()"),self.fileExit)
        self.connect(self.helpIndexAction,SIGNAL("activated()"),self.helpIndex)
        self.connect(self.helpContentsAction,SIGNAL("activated()"),self.helpContents)
        self.connect(self.helpAboutAction,SIGNAL("activated()"),self.helpAbout)
        self.connect(self.mToolbox,SIGNAL("clicked(int)"),self.mStack.raiseWidget)


    def languageChange(self):
        self.setCaption(self.__tr("Infiscape Cluster Utility"))
        self.mToolbox.setTitle(QString.null)
        self.fileReloadAction.setText(self.__tr("Reload"))
        self.fileReloadAction.setMenuText(self.__tr("&Reload..."))
        self.fileReloadAction.setAccel(self.__tr("Ctrl+R"))
        self.fileNewAction.setText(self.__tr("New"))
        self.fileNewAction.setMenuText(self.__tr("&New"))
        self.fileNewAction.setAccel(self.__tr("Ctrl+N"))
        self.fileOpenAction.setText(self.__tr("Open"))
        self.fileOpenAction.setMenuText(self.__tr("&Open..."))
        self.fileOpenAction.setAccel(self.__tr("Ctrl+O"))
        self.fileSaveAction.setText(self.__tr("Save"))
        self.fileSaveAction.setMenuText(self.__tr("&Save"))
        self.fileSaveAction.setAccel(self.__tr("Ctrl+S"))
        self.fileSaveAsAction.setText(self.__tr("Save As"))
        self.fileSaveAsAction.setMenuText(self.__tr("Save &As..."))
        self.fileSaveAsAction.setAccel(QString.null)
        self.fileExitAction.setText(self.__tr("Exit"))
        self.fileExitAction.setMenuText(self.__tr("E&xit"))
        self.fileExitAction.setAccel(QString.null)
        self.helpContentsAction.setText(self.__tr("Contents"))
        self.helpContentsAction.setMenuText(self.__tr("&Contents..."))
        self.helpContentsAction.setAccel(QString.null)
        self.helpIndexAction.setText(self.__tr("Index"))
        self.helpIndexAction.setMenuText(self.__tr("&Index..."))
        self.helpIndexAction.setAccel(QString.null)
        self.helpAboutAction.setText(self.__tr("About"))
        self.helpAboutAction.setMenuText(self.__tr("&About"))
        self.helpAboutAction.setAccel(QString.null)
        self.toolBar.setLabel(self.__tr("Tools"))
        if self.MenuBar.findItem(1):
            self.MenuBar.findItem(1).setText(self.__tr("&File"))
        if self.MenuBar.findItem(2):
            self.MenuBar.findItem(2).setText(self.__tr("&Help"))


    def fileNew(self):
        print "ClusterControlBase.fileNew(): Not implemented yet"

    def fileOpen(self):
        print "ClusterControlBase.fileOpen(): Not implemented yet"

    def fileSave(self):
        print "ClusterControlBase.fileSave(): Not implemented yet"

    def fileSaveAs(self):
        print "ClusterControlBase.fileSaveAs(): Not implemented yet"

    def filePrint(self):
        print "ClusterControlBase.filePrint(): Not implemented yet"

    def fileExit(self):
        print "ClusterControlBase.fileExit(): Not implemented yet"

    def helpIndex(self):
        print "ClusterControlBase.helpIndex(): Not implemented yet"

    def helpContents(self):
        print "ClusterControlBase.helpContents(): Not implemented yet"

    def helpAbout(self):
        print "ClusterControlBase.helpAbout(): Not implemented yet"

    def reloadModules(self):
        print "ClusterControlBase.reloadModules(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ClusterControlBase",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ClusterControlBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
