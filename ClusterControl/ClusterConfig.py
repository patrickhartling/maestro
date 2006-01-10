import elementtree.ElementTree as ET
from xml.dom.minidom import parseString
import Pyro.core
from Pyro.protocol import getHostname
from threading import Thread
import time, types, re, sys

global daemon

class PyroServer(Thread):
   def __init__(self):
      Thread.__init__(self)
      self.setDaemon(1)
      self.ready=0
   def run(self):
      global daemon
      Pyro.core.initServer()
      print "Creating Pyro server objects and Pyro Daemon"
      daemon = Pyro.core.Daemon()
      self.mOutputLogger = OutputLogger()
      daemon.connect(self.mOutputLogger)  # callback object
      self.ready=1
      print "PYRO SERVER ACTIVATED"
      daemon.requestLoop()

class OutputLogger(Pyro.core.CallbackObjBase):
   def __init__(self):
      Pyro.core.ObjBase.__init__(self)
      self.subscribersMatch={}

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

   def publish(self, subjects, message):
      if not subjects: return
      # publish a message. Subjects must be exact strings
      for subject in self._mksequence(subjects):
         # process the subject patterns
         for (m,subs) in self.subscribersMatch.items():
            if m.match(subject):
               # send event to all subscribers
               for cb in subs:
                  cb(message)

class ClusterConfig:
   def __init__(self, xmlTree):
      self.mElement = xmlTree.getroot()
      assert self.mElement.tag == "cluster_config"

      self.mNodes = []

      for nodeElt in self.mElement.findall("./cluster_node"):
         self.mNodes.append(ClusterNode(nodeElt))
         print "Cluster Node: ", ClusterNode(nodeElt).getName()

      Pyro.core.initClient()
      self.mPyroServer = PyroServer()
      self.mPyroServer.start()
      while not self.mPyroServer.ready:
         time.sleep(1)

      # Simple callback to print all output to stdout
      def debugCallback(message):
         sys.stdout.write("DEBUG: " + message)

      # Register debug callback
      self.mPyroServer.mOutputLogger.subscribeMatch(".*", debugCallback)

   def refresh(self):
      """Try to connect to all nodes."""
      for n in self.mNodes:
         n.disconnect()
         n.connect()

   def runRemoteCommand(self, masterCommand, slaveCommand):
      """Run commands on cluster."""
      for n in self.mNodes:
         n.runRemoteCommand(masterCommand, self.mPyroServer.mOutputLogger.getProxy())
         

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

   def getHostname(self):
      return self.mElement.get("hostname")

   def connect(self):
      if None == self.mProxy:
         try:
            self.mProxy = Pyro.core.getProxyForURI("PYROLOC://" + self.getHostname() + ":7766/cluster_server")
         except:
            self.mProxy = None
            print "Error connecting proxy to [%s]" % (self.getHostname())
      else:
         print "Cluster node [%s] already has an active proxy." % (self.getName())

   def proxy(self):
      return self.mProxy

   def runRemoteCommand(self, command, callback):
      global daemon
      if not None == self.mProxy:
         self.mProxy.runCommand(command, callback, str(self.getHostname()))
      else:
         print "Cluster node [%s] is not connected." % (self.getName())

   def disconnect(self):
      if not None == self.mProxy:
         del self.mProxy
         self.mProxy = None
