# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestSettingsBase.ui'
#
# Created: Wed Jan 4 19:08:16 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class TestSettingsBase(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("TestSettingsBase")


        TestSettingsBaseLayout = QHBoxLayout(self,11,6,"TestSettingsBaseLayout")

        self.splitter2 = QSplitter(self,"splitter2")
        self.splitter2.setOrientation(QSplitter.Horizontal)

        self.listView2 = QListView(self.splitter2,"listView2")
        self.listView2.addColumn(self.__tr("Column 1"))

        LayoutWidget = QWidget(self.splitter2,"layout2")
        layout2 = QVBoxLayout(LayoutWidget,11,6,"layout2")

#        self.mClusterGroup = QGroupBox(LayoutWidget,"mClusterGroup")
#        layout2.addWidget(self.mClusterGroup)

#        self.mNodeGroup = QGroupBox(LayoutWidget,"mNodeGroup")
#        layout2.addWidget(self.mNodeGroup)
        TestSettingsBaseLayout.addWidget(self.splitter2)

        self.languageChange()

        self.resize(QSize(600,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Cluster Settings"))
        self.listView2.header().setLabel(0,self.__tr("Column 1"))
        self.listView2.clear()
        item = QListViewItem(self.listView2,None)
        item.setText(0,self.__tr("New Item"))

#        self.mClusterGroup.setTitle(self.__tr("Cluster Settings"))
#        self.mNodeGroup.setTitle(self.__tr("Node Settings"))


    def __tr(self,s,c = None):
        return qApp.translate("TestSettingsBase",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = TestSettingsBase()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
