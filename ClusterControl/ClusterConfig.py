import elementtree.ElementTree as ET
from xml.dom.minidom import parseString
import Pyro.core
from Pyro.protocol import getHostname
import threading
import time, types, re, sys

from PyQt4 import QtCore
from Queue import Queue

import copy

class ClusterConfig(QtCore.QObject):
   def __init__(self, xmlTree):
      QtCore.QObject.__init__(self)
      # Store cluster XML element
      self.mElement = xmlTree.getroot()
      assert self.mElement.tag == "cluster_config"

      # Parse all node settings
      self.mNodes = []
      for nodeElt in self.mElement.findall("./cluster_node"):
         self.mNodes.append(ClusterNode(nodeElt))
         print "Cluster Node: ", ClusterNode(nodeElt).getName()

      #Pyro.core.initClient()

      # Output logger to manage all output coming over the network
      self.mOutputLogger = OutputLogger()

      # Timer to refresh Qt controls that have registered to recieve output.
      self.outputLoggerTimer = QtCore.QTimer()
      self.outputLoggerTimer.setInterval(100)
      self.outputLoggerTimer.start()
      QtCore.QObject.connect(self.outputLoggerTimer, QtCore.SIGNAL("timeout()"), self.refreshOutputLogger)
      
      # Timer to refresh pyro connections to nodes.
      self.refreshTimer = QtCore.QTimer()
      self.refreshTimer.setInterval(2000)
      self.refreshTimer.start()
      QtCore.QObject.connect(self.refreshTimer, QtCore.SIGNAL("timeout()"), self.refreshConnections)


      # Simple callback to print all output to stdout
      def debugCallback(message):
         sys.stdout.write("DEBUG: " + message)

   def removeNode(self, node):
      assert not None == node

      # Remove node's element from XML tree.
      self.mElement.remove(node.mElement)
      # Remove node data structure
      self.mNodes.remove(node)
      self.emit(QtCore.SIGNAL("nodeRemoved()"), node)

   def addNode(self):
      new_element = ET.SubElement(self.mElement, "cluster_node", name="NewNode", hostname="NewNode")
      new_node = ClusterNode(new_element)
      self.mNodes.append(new_node)
      self.refreshConnections()
      self.emit(QtCore.SIGNAL("nodeAdded()"), new_node)
      return new_node

   def refreshOutputLogger(self):
      self.mOutputLogger.publishEvents()
        
   def getOutputLogger(self):
      return self.mOutputLogger

   def refreshConnections(self):
      """Try to connect to all nodes."""

      new_connections = False

      for n in self.mNodes:
         if None == n.mProxy:
            if n.connect():
               new_connections = True

      if new_connections:
         self.emit(QtCore.SIGNAL("newConnections()"))

   def runRemoteCommand(self, masterCommand, slaveCommand):
      """Run commands on cluster."""
      for n in self.mNodes:
         n.runCommand(masterCommand, self.mOutputLogger)
         
class ClusterNode:
   def __init__(self, xmlElt):
      assert xmlElt.tag == "cluster_node"
      self.mElement = xmlElt
      #print "Name:", self.mElement.get("name")
      #print "HostName:", self.mElement.get("hostname")
      self.mProxy = None
      self.mName = self.mElement.get("name")
      self.mHostname = self.mElement.get("hostname")

   def getName(self):
      return self.mElement.get("name")

   def setName(self, newName):
      return self.mElement.set("name", newName)

   def getHostname(self):
      return self.mElement.get("hostname")

   def setHostname(self, newHostname):
      return self.mElement.set("hostname", newHostname)

   def connect(self):
      if None == self.mProxy:
         try:
            self.mProxy = Pyro.core.getProxyForURI("PYROLOC://" + self.getHostname() + ":7766/cluster_server")
            print "Connected to [%s]" % (self.getName())
            return True
         except:
            self.mProxy = None
            print "Error connecting proxy to [%s]" % (self.getHostname())
      else:
         print "Cluster node [%s] already has an active proxy." % (self.getName())
      return False

   def proxy(self):
      return self.mProxy

   def runCommand(self, command, outputLogger):
      if not None == self.mProxy:
         self.mProxy.runCommand(command)
         ot = OutputThread(copy.copy(self.mProxy), self.getName(), outputLogger)
         ot.start()
      else:
         print "Cluster node [%s] is not connected." % (self.getName())

   def disconnect(self):
      if not None == self.mProxy:
         del self.mProxy
         self.mProxy = None

class OutputThread(threading.Thread):
   def __init__(self, proxy, subject, outputLogger):
      threading.Thread.__init__(self)
      self.mProxy = proxy
      self.mSubject = subject
      self.mOutputLogger = outputLogger

   def run(self):
      line = self.mProxy.getOutput()
      while not "" == line:
         # Strip the trailing newline char
         self.mOutputLogger.output(self.mSubject, line[:-1])
         line = self.mProxy.getOutput()
      print "Done running command."

class OutputLogger(QtCore.QObject):
   def __init__(self):
      QtCore.QObject.__init__(self)
      self.subscribersMatch={}
      self.mQueue = Queue()

   def _mksequence(self, seq):
      if not (type(seq) in (types.TupleType,types.ListType)):
         return (seq,)
      return seq

   def subscribeMatch(self, subjects, callback):
      if not subjects: return
      # Subscribe into a dictionary; this way; somebody can subscribe
      # only once to this subject. Subjects are regex patterns.
      for subject in self._mksequence(subjects):
         matcher = re.compile(subject, re.IGNORECASE)
         self.subscribersMatch.setdefault(matcher, []).append(callback)

   def unsubscribe(self, subjects, callback):
      if not subjects: return
      for subject in self._mksequence(subjects):
         try:
            m = re.compile(subject,re.IGNORECASE)
            self.subscribersMatch[m].remove(callback)
         except ValueError, x:
            pass

   def output(self, subjects, message):
      self.mQueue.put((subjects, message))
      
   def publishEvents(self):
      try:
         # Run a maximum up 100 times.
         for x in xrange(100):
            (subjects, message) = self.mQueue.get(block=False)
            if not subjects: return
            # publish a message. Subjects must be exact strings
            for subject in self._mksequence(subjects):
               # process the subject patterns
               for (m,subs) in self.subscribersMatch.items():
                  if m.match(subject):
                     # send event to all subscribers
                     for cb in subs:
                        cb(message)
      except:
         pass
