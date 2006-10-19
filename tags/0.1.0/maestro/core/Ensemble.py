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

import logging
import elementtree.ElementTree as ET
from xml.dom.minidom import parseString
from PyQt4 import QtCore, QtGui

import maestro
import maestro.core
const = maestro.core.const
import socket, types

def makeEnsemble(file):
   tree = ET.ElementTree(file=file)
   ensemble = Ensemble.Ensemble(tree)

class Ensemble(QtCore.QObject):
   """ Contains information about a cluster of nodes. """
   def __init__(self, file, parent=None):
      QtCore.QObject.__init__(self, parent)

      # Store filename to save to later.
      self.mFilename = file

      # Parse XML file.
      self.mElementTree = ET.ElementTree(file=file)

      # Store cluster XML element
      self.mElement = self.mElementTree.getroot()
      assert self.mElement.tag == "ensemble"

      self.mLogger = logging.getLogger("maestro.Ensemble")

      # Parse all node settings
      self.mNodes = []
      for nodeElt in self.mElement.findall("./cluster_node"):
         self.mNodes.append(ClusterNode(nodeElt))
         print "Cluster Node: ", ClusterNode(nodeElt).getName()

      # XXX: Should we manage this signal on a per node basis? We would have
      #      to make each node generate a signal when it's OS changed and
      #      listen for it here anyway.
      # Register to receive signals from all nodes about their current os.
      env = maestro.core.Environment()
      env.mEventManager.connect("*", "ensemble.report_os", self.onReportOs)
      env.mEventManager.connect("*", "lostConnection", self.onLostConnection)

   def save(self, file=None):
      if file is None:
         file = self.mFilename

   def disconnectFromEventManager(self):
      # Unregister to receive signals from all nodes about their current os.
      env = maestro.core.Environment()
      env.mEventManager.disconnect("*", "ensemble.report_os", self.onReportOs)
      env.mEventManager.disconnect("*", "lostConnection", self.onLostConnection)

   def getNode(self, index):
      """ Return the node at the given index. Returns None if index is out of range.

          @param index: The index of the node to return.
      """
      if index < 0 or index >= len(self.mNodes):
         return None
      return self.mNodes[index]

   def getNodeById(self, id):
      """ Return the node with the given ID.

          @param id: ID of the requested node.
      """
      for node in self.mNodes:
         if node.getId() == id:
            return node
      return None

   def getNumNodes(self):
      """ Returns the number of nodes in Ensemble. """
      return len(self.mNodes)

   def onReportOs(self, nodeId, os):
      """ Slot that gets called when a node reports it's operating system.

          @param nodeId: The ID of the node that is reporting its OS.
          @param os: Operating system integer constant.
      """
      assert(type(os) == types.IntType)
      try:
         print "onReportOs [%s] [%s]" % (nodeId, os)
         for node in self.mNodes:
            if node.getIpAddress() == nodeId:
               if os != node.mPlatform:
                  node.setPlatform(os)
                  self.emit(QtCore.SIGNAL("nodeChanged(QString)"), nodeId)

      except Exception, ex:
         print "ERROR: ", ex

   def lookupIpAddrs(self):
      for node in self.mNodes:
         node.lookupIpAddress()

   def refreshConnections(self):
      """Try to connect to all nodes."""

      env = maestro.core.Environment()
      new_connections = False

      # Iterate over nodes and try to connect to nodes that are not connected.
      for node in self.mNodes:
         try:
            # Attempt to get the IP address from the hostname.
            ip_address = node.getIpAddress()
            # If node is not connected, attempt to connect.
            if not env.mEventManager.isConnected(ip_address):
               deferred = env.mEventManager.connectToNode(ip_address)
               deferred.addCallback(self.onConnection, ip_address)
               deferred.addErrback(self.onConnectError, ip_address)
         except Exception, ex:
            print "WARNING: Could not connect to [%s] [%s]" % (node.getHostname(), ex)

   def onConnection(self, result, nodeId):
      # Tell the new node to report its os.
      env = maestro.core.Environment()
      self.mLogger.info("We are now connected to %s" % nodeId)
      # Could this signal also include nodeId?
      self.emit(QtCore.SIGNAL("ensembleChanged()"))

      return result

   def onConnectError(self, failure, nodeId):
      self.mLogger.error("Failed to connect to %s: %s" % \
                            (nodeId, str(failure.value)))

   def onLostConnection(self, msgFrom, nodeId):
      """ Slot that is called when a connection is lost to a node.

          @param msgFrom: Source of signal, in this case always '*'.
          @param nodeId: ID of the node that lost it's connection.
      """
      for node in self.mNodes:
         if node.getId() == nodeId:
            node.lostConnection()

      # Refresh all views of the Ensemble.
      self.emit(QtCore.SIGNAL("ensembleChanged()"))

   def createNode(self, name="NewNode", hostname="NewNode", node_class=""):
      new_element = ET.SubElement(self.mElement, "cluster_node", name=name, hostname=hostname)
      new_element.set('class', node_class)

      new_node = ClusterNode(new_element)
      self.mNodes.append(new_node)
      self.emit(QtCore.SIGNAL("ensembleChanged()"))
      new_index = len(self.mNodes) - 1
      self.emit(QtCore.SIGNAL("nodeAdded"), new_index, new_node)
      return new_node

   def addNode(self, node, index=-1):
      if -1 == index:
         index = len(self.mNodes)
      self.mNodes.insert(index, node)
      self.mElement.insert(index, node.mElement)
      self.emit(QtCore.SIGNAL("ensembleChanged()"))
      self.emit(QtCore.SIGNAL("nodeAdded"), index, node)

   def removeNode(self, nodeOrIndexOrId):
      node = None
      if isinstance(nodeOrIndexOrId, ClusterNode):
         node = nodeOrIndexOrId
      if types.IntType == type(nodeOrIndexOrId):
         node = self.mNodes[node]
      elif types.StringType == type(nodeOrIndexOrId):
         for n in self.mNodes[:]:
            if n.getId() == node.getId():
               node = n
               break

      if node is None:
         print "WARNING: Node could not be removed: %s", nodeOrIndexOrId
      elif self.mNodes.count(node) > 0:
         old_index = self.mNodes.index(node)
         self.mNodes.remove(node)
         self.mElement.remove(node.mElement)
         env = maestro.core.Environment()
         env.mEventManager.disconnectFromNode(node.getId())
         self.emit(QtCore.SIGNAL("ensembleChanged()"))
         self.emit(QtCore.SIGNAL("nodeRemoved"), old_index, node)
 
class ClusterNode(QtCore.QObject):
   """ Represents a node in the active cluster configuration. Most of this
       information is loaded from the configuration file. But things like
       the current OS are retrieved from the remote object.
   """
   def __init__(self, xmlElt, parent=None):
      QtCore.QObject.__init__(self, parent)
      assert xmlElt.tag == "cluster_node"
      self.mElement = xmlElt
      #print "Name:", self.mElement.get("name")
      #print "HostName:", self.mElement.get("hostname")
      self.mName = self.mElement.get('name', '')
      self.mHostname = self.mElement.get('hostname', '')
      self.mClass = self.mElement.get('class', '')
      self.mPlatform = const.ERROR
      self.mIpAddress = '0.0.0.0'
      self.lookupIpAddress()

   def lostConnection(self):
      """ Slot that is called when the connection to this node is lost. All
          cached data should be cleared and set to it's inital state.
      """
      self.mPlatform = const.ERROR 

   def getName(self):
      return self.mElement.get('name', 'Unknown')

   def setName(self, newName):
      return self.mElement.set('name', newName)

   def getClass(self):
      return self.mElement.get('class', '')

   def setClass(self, newClass):
      self.mElement.set('class', newClass)

   def getHostname(self):
      return self.mElement.get('hostname', 'Unknown')

   def lookupIpAddress(self):
      try:
         self.mIpAddress = socket.gethostbyname(self.getHostname())
      except:
         self.mIpAddress = '0.0.0.0'
      
   def setHostname(self, newHostname):
      self.mPlatform = const.ERROR
      self.mElement.set('hostname', newHostname)
      self.lookupIpAddress()

   def getId(self):
      return self.getIpAddress()

   def getIpAddress(self):
      return self.mIpAddress

   def setPlatform(self, os):
      self.mPlatform = os
      self.emit(QtCore.SIGNAL("platformChanged(int)"), self.mPlatform)

   def getPlatformName(self):
      return const.OsNameMap[self.mPlatform]

   def getClassList(self):
      class_list = [c.strip() for c in self.mClass.split(",") if c != ""]
      platform = self.getPlatformName()
      if platform > 0:
         class_list.insert(0, platform)
      return class_list