# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestSettingsBase.ui'
#
# Created: Fri Jan  6 12:05:09 2006
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

import ClusterSettingsResource

class Ui_Form(object):
   def setupUi(self, Form):
      Form.setObjectName("Form")
      Form.resize(QtCore.QSize(QtCore.QRect(0,0,599,478).size()).expandedTo(Form.minimumSizeHint()))
      
      self.hboxlayout = QtGui.QHBoxLayout(Form)
      self.hboxlayout.setMargin(9)
      self.hboxlayout.setSpacing(6)
      self.hboxlayout.setObjectName("hboxlayout")
      
      self.splitter = QtGui.QSplitter(Form)
      self.splitter.setOrientation(QtCore.Qt.Horizontal)
      self.splitter.setObjectName("splitter")
      
      self.listView = QtGui.QListView(self.splitter)
      self.listView.setObjectName("listView")
      
      self.layoutWidget = QtGui.QWidget(self.splitter)
      self.layoutWidget.setObjectName("layoutWidget")
      
      self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
      self.vboxlayout.setMargin(0)
      self.vboxlayout.setSpacing(6)
      self.vboxlayout.setObjectName("vboxlayout")
      
      self.retranslateUi(Form)

   
   def tr(self, string):
      return QtGui.QApplication.translate("Form", string, None, QtGui.QApplication.UnicodeUTF8)
   
   def retranslateUi(self, Form):
      Form.setWindowTitle(self.tr("Form"))

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   Form = QtGui.QWidget()
   ui = Ui_Form()
   ui.setupUi(Form)
   Form.show()
   sys.exit(app.exec_())

