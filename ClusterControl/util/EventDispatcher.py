import types
import Pyro.core

class EventDispatcher(object):
   """ Class to capture and handle event processing in the system.
       TODO:
         - Add culling of null references
   """
   def __init__(self, hostName, callback=None):
      """ Initialize the event dispatcher. """
      # Connections is a map of:
      #     node_guid: {signam, (slot callables,)}
      self.mConnections = {}
      self.mHostname = hostName
      self.mCallback = callback

   def register(self, nodeId, obj):
      """ Register object to recieve callback events for the given node."""
      if self.mConnections.has_key(nodeId):
         raise AttributeError("EventDispatcher.connect: already connected to [%s]" % (nodeId))

      self.mConnections[nodeId] = obj

   def connect(self, nodeId):
      """ Connect to the given nodes event manager.
          nodeId - IP/hostname of the node to connect to
      """
      if not isinstance(nodeId, types.StringType):
         raise TypeError("EventDispatcher.connect: nodeId of non-string type passed")
      
      # Make sure tables exist
      if self.mConnections.has_key(nodeId):
         raise AttributeError("EventDispatcher.connect: already connected to [%s]" % (nodeId))

      try:
         print "Trying to connect to: PYROLOC://%s:7766/cluster_server" % (nodeId)
         proxy = Pyro.core.getProxyForURI("PYROLOC://" + nodeId + ":7766/cluster_server")
         print "Connected to [%s] [%s]" % (nodeId, proxy.GUID())
         self.mConnections[nodeId] = proxy
         proxy.register(self.mHostname, self.mCallback)
      except Exception, ex:
         print "Error connecting proxy to [%s]" % (nodeId)
         print ex
         return False
      return True

   def disconnect(self, nodeId):
      """ Disconnect a signal from a slot (callable). 
         Removes *all* found slots matching nodeId, sigName, slotCallable.
      """
      if not isinstance(nodeId, types.StringType):
         raise TypeError("EventDispatcher.connect: nodeId of non-string type passed")
      
      if self.mConnections.has_key(nodeId):
         del self.mConnections[nodeId]
   
      
   def emit(self, nodeId, sigName, argsTuple=()):
      """ Emit the named signal on the given node.
          If there are no registered slots, just do nothing.
      """
      if not isinstance(nodeId, types.StringType):
         raise TypeError("EventDispatcher.connect: nodeId of non-string type passed")
      if not isinstance(sigName, types.StringType):
         raise TypeError("EventDispatcher.connect: sigName of non-string type passed")
      if not isinstance(argsTuple, types.TupleType):
         raise TypeError("EventDispatcher.connect: argsTuple not of tuple type passed.")
      
      # Append out hostname to distinguish where messages are coming from.
      ip_address = Pyro.protocol.getIPAddress(self.mHostname)
      argsTuple = (ip_address,) + argsTuple

      if nodeId == "*":
         for k, v in self.mConnections.iteritems():
            try:
               v.emit(nodeId, sigName, argsTuple)
            except Pyro.errors.ConnectionClosedError, x:
               del self.mConnections[k]
               print 'Removed dead connection', k
      # If there are slots, loop over them and call
      elif self.mConnections.has_key(nodeId):
         try:
            self.mConnections[nodeId].emit(nodeId, sigName, argsTuple)
         except Pyro.errors.ConnectionClosedError, x:
            # connection dropped, remove the listener if it's still there
            # check for existence because other thread may have killed it already
            if self.mConnections.has_key(nodeId):
               del self.mConnections[nodeId]
               print 'Removed dead connection', nodeId

   def isConnected(self, nodeId):
      return self.mConnections.has_key(nodeId)
      
   def _getConnections(self):
      return self.mConnections
