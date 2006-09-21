import sys, os, platform

import services.LaunchService
import services.SettingsService
import services.ResourceService
import util.EventManager
import datetime
import time
import socket

from twisted.spread import pb
from util import pboverssl
from twisted.cred import checkers, credentials, portal, error
from zope.interface import implements
from twisted.conch.checkers import UNIXPasswordDatabase
from twisted.internet import ssl, defer
from twisted.python import failure

import PAM

def callIntoPAM(service, user, conv):
   """A testing hook.
   """
   pam = PAM.pam()
   pam.start(service)
   pam.set_item(PAM.PAM_USER, user)
   pam.set_item(PAM.PAM_CONV, conv)
   gid = os.getegid()
   uid = os.geteuid()
   os.setegid(0)
   os.seteuid(0)
   try:
      pam.authenticate() # these will raise
      pam.acct_mgmt()
      print 'PAM Authentication Succeeded!'
      os.setegid(gid)
      os.seteuid(uid)
      return True
   except PAM.error, resp:
      print 'PAM Authentication Failed!'
      print 'Go away! (%s)' % resp
   except Exception, ex:
      print 'PAM Authentication Failed!'
      print 'Internal error: (%s)' % ex

   os.setegid(gid)
   os.seteuid(uid)
   return False

def makeConv(d):
   def conv(auth, query_list, userData):
      return [(d[t], 0) for q, t in query_list]
   return conv

class PAMChecker:
   implements(checkers.ICredentialsChecker)
   credentialInterfaces = credentials.IPluggableAuthenticationModules,
   #service = 'Twisted'
   service = 'passwd'

   def makeConv(self, d):
      def conv(auth, query_list, userData):
         return [(d[t], 0) for q, t in query_list]
      return conv

   def requestAvatarId(self, credentials):
      d = defer.maybeDeferred(callIntoPAM, self.service, credentials.username, credentials.pamConversion)
      d.addCallback(self._cbPasswordMatch, credentials.username)
      return d

   def _cbPasswordMatch(self, matched, username):
      if matched:
         return username
      else:
         return failure.Failure(error.UnauthorizedLogin("Incorrect password for user [%s]!" % (username)))