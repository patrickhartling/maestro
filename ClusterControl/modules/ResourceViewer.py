# Copyright (C) Infiscape Corporation 2006

from PyQt4 import QtGui, QtCore
import ResourceViewerBase
import ResourceViewerResource
import Pyro.core

import services.SettingsService

class ResourceViewer(QtGui.QWidget, ResourceViewerBase.Ui_ResourceViewerBase):
   def __init__(self, parent = None):
      QtGui.QWidget.__init__(self, parent)
      self.setupUi(self)
      self.mClusterModel = None

   def setupUi(self, widget):
      """
      Setup all initial gui settings that don't need to know about the cluster configuration.
      """
      ResourceViewerBase.Ui_ResourceViewerBase.setupUi(self, widget)
      self.mTitleLbl.setBackgroundRole(QtGui.QPalette.Mid)
      self.mTitleLbl.setForegroundRole(QtGui.QPalette.Shadow)
      
      delegate = PixelDelegate(self.mResourceTable)
      self.mResourceTable.setItemDelegate(delegate)
      
   def reportCpuUsage(self, ip, val):
      print "RV CPU Usage [%s]: %s" % (ip, val)
      self.mResourceModel.mCpuUsageMap[ip] = val
      self.mResourceTable.reset()

   def reportMemUsage(self, ip, val):
      print "RV Mem Usage [%s]: %s" % (hostname, val)

   def configure(self, clusterModel, daemon):
      """ Configure the user interface with data in cluster configuration. """
      self.mClusterModel = clusterModel

      self.mResourceModel = ResourceModel(self.mClusterModel)
      self.mResourceTable.setModel(self.mResourceModel)
      self.mResourceCallback = services.SettingsService.ResourceCallback()
      self.mResourceCallback.delegateTo(self)
      daemon.connect(self.mResourceCallback)

      for node in self.mClusterModel.mNodes:
         if node.proxy() is not None:
            # Get operating system
            try:
               cpu_usage = node.proxy().getService("Settings").register(self.mResourceCallback.getProxy())
               ip_addr = node.getIpAddress()
               self.mResourceModel.mCpuUsageMap[ip_addr] = 0.0
               self.mResourceModel.mMemUsageMap[ip_addr] = (0.0, 0.0)
            except Exception, ex:
               print "Excepetion: ", ex
         else:
            print "Proxy is None"
      

   def getName():
        return "Resource Viewer"
   getName = staticmethod(getName)

class PixelDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QAbstractItemDelegate.__init__(self,parent)
        self.pixelSize = 12

    def paint(self, painter, option, index):
      if index.column() == 0:
         QtGui.QItemDelegate.paint(self, painter, option, index)
      elif True:
         style = QtGui.QApplication.style()
         pb_opts = QtGui.QStyleOptionProgressBarV2()
         pb_opts.palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0, 0, 255))
         value, ok = index.model().data(index, QtCore.Qt.DisplayRole).toDouble()
         pb_opts.minimum = 0
         pb_opts.maximum = 100
         pb_opts.progress = value
         pb_opts.rect = option.rect
         pb_opts.textVisible = True
         pb_opts.textAlignment = QtCore.Qt.AlignCenter
         pb_opts.orientation = QtCore.Qt.Horizontal
         pb_opts.text = ("%.2f " % value) + "%"
         style.drawControl(QtGui.QStyle.CE_ProgressBar, pb_opts, painter)
    

class ResourceModel(QtCore.QAbstractTableModel):
   def __init__(self, clusterModel, parent=None):
      QtCore.QAbstractTableModel.__init__(self, parent)
      self.mClusterModel = clusterModel
      self.mCpuUsageMap = {}
      self.mMemUsageMap = {}

   def rowCount(self, parent):
      return self.mClusterModel.rowCount()

   def columnCount(self, parent):
      return 4

   def headerData(self, section, orientation, role):
      if orientation == QtCore.Qt.Horizontal:
         if section == 0:
            return QtCore.QVariant("Node")
         elif section == 1:
            return QtCore.QVariant("CPU Usage")
         elif section == 2:
            return QtCore.QVariant("Memory Usage")
         elif section == 3:
            return QtCore.QVariant("Swap Usage")
      return QtCore.QVariant()

   def data(self, index, role):
      if not index.isValid():
         return QtCore.QVariant()
      elif role != QtCore.Qt.DisplayRole:
         return QtCore.QVariant()

      cm_index = self.mClusterModel.createIndex(index.row(), index.column())

      node = self.mClusterModel.data(cm_index, QtCore.Qt.UserRole)
      ip_addr = node.getIpAddress()
      if index.column() == 0:
         return QtCore.QVariant(self.mClusterModel.data(cm_index))
      elif index.column() == 1:
         try:
            return QtCore.QVariant(self.mCpuUsageMap[ip_addr])
         except:
            return QtCore.QVariant(0.0)
      elif index.column() == 2:
         node = self.mClusterModel.data(cm_index, QtCore.Qt.UserRole)
         try:
            return QtCore.QVariant(self.mCpuUsageMap[ip_addr][0])
         except:
            return QtCore.QVariant(0.0)
      elif index.column() == 3:
         node = self.mClusterModel.data(cm_index, QtCore.Qt.UserRole)
         try:
            return QtCore.QVariant(self.mCpuUsageMap[ip_addr][1])
         except:
            return QtCore.QVariant(0.0)
      
      return QtCore.QVariant()

#   def refreshUsage(self):
#      for node in self.mClusterModel.mNodes:
#         if node.proxy() is not None:
#            # Get operating system
#            try:
#               cpu_usage = node.proxy().getService("Settings").getCpuUsage()
#               self.mCpuUsageMap[node] = cpu_usage
#            except Exception, ex:
#               print "Excepetion", ex
#               self.mCpuUsageMap[node] = 0.0
#            try:
#               mem_usage = node.proxy().getService("Settings").getMemUsage()
#               self.mMemUsageMap[node] = mem_usage
#            except Exception, ex:
#               print "Excepetion", ex
#               self.mMemUsageMap[node] = (0.0, 0.0)
#
#         else:
#            print "Proxy is None"
#            self.mCpuUsageMap[node] = 0.0
#            self.mMemUsageMap[node] = (0.0, 0.0)


def getModuleInfo():
   icon = QtGui.QIcon(":/ResourceViewer/images/resources.png")
   return (ResourceViewer, icon)

if __name__ == "__main__":
   app = QtGui.QApplication(sys.argv)
   cs = ResourceViewer()
   cs.show()
   sys.exit(app.exec_())

