from twisted.spread import pb
from twisted.spread.flavors import Referenceable
from twisted.internet import defer, protocol
from zope.interface import implements
from twisted.cred import credentials
from twisted.spread.interfaces import IJellyable, IUnjellyable

class PortalRoot:
    """Root object, used to login to portal."""

    implements(pb.IPBRoot)

    def __init__(self, portal):
        self.portal = portal

    def rootObject(self, broker):
        return _PortalWrapper(self.portal, broker)

class _PortalWrapper(Referenceable):
   """Root Referenceable object, used to login to portal."""

   implements(credentials.IUsernamePassword)

   def __init__(self, portal, broker):
      self.portal = portal
      self.broker = broker

   # Have to return two rhings
   def remote_login(self, username, password, mind):
      """Start of username/password login."""
      self.mUPCred = credentials.UsernamePassword(username, password)        
      try:
         import pamchecker
         conv = pamchecker.makeConv({1:password, 2:username, 3:''})
         self.mPAMCred = credentials.PluggableAuthenticationModules(username, conv)
      except Exception, ex:
         print ex
         pass

      self.username = username
      self.password = password
      d = self.portal.login(self.mUPCred, mind, pb.IPerspective)
      d.addCallback(self._loggedIn).addErrback(self.tryNext, mind)
      return d

   def tryNext(self, oldDeffered, mind):
      d = self.portal.login(self.mPAMCred, mind, pb.IPerspective)
      d.addCallback(self._loggedIn)
      return d

   # credentials.IUsernamePassword:
   def checkPassword(self, password):
      print "Checking password: ", password
      return self.password == password

   def _loggedIn(self, (interface, perspective, logout)):
      print "Log-in successful."
      if not IJellyable.providedBy(perspective):
         perspective = pb.AsReferenceable(perspective, "perspective")
      self.broker.notifyOnDisconnect(logout)
      return perspective

class PBClientFactory(pb.PBClientFactory):
    def _cbSendUsername(self, root, username, password, client):
        return root.callRemote("login", username, password, client)

    def login(self, credentials, client=None):
        """Login and get perspective from remote PB server.

        Currently only credentials implementing
        L{twisted.cred.credentials.IUsernamePassword} are supported.

        @return: Deferred of RemoteReference to the perspective.
        """
        d = self.getRootObject()
        d.addCallback(self._cbSendUsername, credentials.username, credentials.password, client)
        return d


class PBServerFactory(protocol.ServerFactory):
    """Server factory for perspective broker.

    Login is done using a Portal object, whose realm is expected to return
    avatars implementing pb.IPerspective. The credential checkers in the portal
    should accept IUsernameHashedPassword or IUsernameMD5Password.

    Alternatively, any object implementing or adaptable to IPBRoot can
    be used instead of a portal to provide the root object of the PB
    server.
    """

    unsafeTracebacks = 0

    # object broker factory
    protocol = pb.Broker

    def __init__(self, root, unsafeTracebacks=False):
        self.root = root
        self.unsafeTracebacks = unsafeTracebacks

    def buildProtocol(self, addr):
        """Return a Broker attached to me (as the service provider).
        """
        proto = self.protocol(0)
        proto.factory = self
        proto.setNameForLocal("root", self.root.rootObject(proto))
        return proto

    def clientConnectionMade(self, protocol):
        pass