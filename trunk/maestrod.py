#! /usr/bin/env python

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

import sys, os, platform

import services.LaunchService
import services.ProcessManagementService
import services.RebootService
import services.ResourceService
import services.SettingsService

import util.EventManager
import datetime
import time
import socket
import logging
import logging.handlers

from twisted.spread import pb
from util import pboverssl
from twisted.cred import checkers, credentials, portal, error
from zope.interface import implements
from twisted.internet import ssl
from twisted.python import failure

if os.name == 'nt':
    import win32api, win32event, win32serviceutil, win32service, win32security, ntsecuritycon

if os.name == 'nt':
    def AdjustPrivilege(priv, enable):
        htoken = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY)
        id = win32security.LookupPrivilegeValue(None, priv)
        if enable:
            newPrivileges = [(id, ntsecuritycon.SE_PRIVILEGE_ENABLED)]
        else:
            newPrivileges = [(id, 0)]
        win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)

class MaestroServer:
   def __init__(self):
      ip_address = socket.gethostbyname(socket.gethostname())
      self.mEventManager = util.EventManager.EventManager(ip_address)
      self.mServices = []

   def remote_test(self, val):
      logging.getLogger('maestrod.MaestroServer').debug('Testing: ' + val)
      return "Test complete"

   def registerInitialServices(self):
      # Register initial services
      settings = services.SettingsService.SettingsService()
      settings.init(self.mEventManager)
      self.mServices.append(settings)

      resource = services.ResourceService.ResourceService()
      resource.init(self.mEventManager)
      self.mServices.append(resource)

      pm = services.ProcessManagementService.ProcessManagementService()
      pm.init(self.mEventManager)
      self.mServices.append(pm)

      reboot_service = services.RebootService.RebootService()
      reboot_service.init(self.mEventManager)
      self.mServices.append(reboot_service)
      
      launch_service = services.LaunchService.LaunchService()
      launch_service.init(self.mEventManager)
      self.mServices.append(launch_service)

      # Register callbacks to send info to clients
      #self.mEventManager.timers().createTimer(settings.update, 2.0)
      #self.mEventManager.timers().createTimer(resource.update, 2.0)
      self.mEventManager.timers().createTimer(launch_service.update, 0)

   def update(self):
      """ Give the event manager time to handle it's timers. """
      self.mEventManager.update()

if os.name == 'nt':
   class vrjclusterserver(win32serviceutil.ServiceFramework):
      _svc_name_ = "MaestroService"
      _svc_display_name_ = "Maestro Server"

      def __init__(self, args):
         win32serviceutil.ServiceFramework.__init__(self, args)
         self.mNtEvent = logging.handlers.NTEventLogHandler(self._svc_name_)
         log_file = os.path.join(os.environ['SystemRoot'], 'system32',
                                 'maestrod.log')
         self.mFileLog = logging.handlers.RotatingFileHandler(log_file, 'a',
                                                              50000, 10)

      def SvcStop(self):
         import servicemanager
         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

         logger = logging.getLogger('')
         logger.info('Stopped')
         logging.shutdown()

         # Shutdown Server
         #self.sfcServer.server_close()
         self.ReportServiceStatus(win32service.SERVICE_STOPPED)

      def SvcDoRun(self):
         import servicemanager

         formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
         self.mNtEvent.setLevel(logging.INFO)
         self.mNtEvent.setFormatter(formatter)
         self.mFileLog.setLevel(logging.DEBUG)
         self.mFileLog.setFormatter(formatter)

         logger = logging.getLogger('')
         logger.addHandler(self.mNtEvent)
         logger.addHandler(self.mFileLog)

         logger.info('Started')

         # Log a 'started' message to the event log.
         servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                               servicemanager.PYS_SERVICE_STARTED,
                               (self._svc_display_name_, ''))

         try:
            RunServer(installSH=False)
         except Exception, ex:
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                               servicemanager.PYS_SERVICE_STARTED,
                               (self._svc_display_name_, 'error' + str(ex)))

class UserPerspective(pb.Avatar):
   def __init__(self, eventMgr, avatarId):
      """ Constructs a UserPerspective used to access the event manager.
          @param eventMgr: A reference to the event manager to use.
          @param avatarId: Handle to the user's authentication.
          @note avatarId is a username on UNIX and a handle on win32.
      """
      self.mEventManager = eventMgr
      self.mAvatarId = avatarId
      self.mCredentials = {}

   def perspective_registerCallback(self, nodeId, obj):
      self.mEventManager.remote_registerCallback(nodeId, obj)

   def perspective_emit(self, nodeId, sigName, argsTuple=()):
      self.mEventManager.remote_emit(nodeId, sigName, (self,) + argsTuple)

   def setCredentials(self, creds):
      self.mCredentials = creds

   def getCredentials(self):
      return self.mCredentials

   def logout(self, nodeId):
      logger = logging.getLogger('maestrod.UserPerspective')
      logger.info("Logging out client: " + str(nodeId))
      self.mEventManager.unregisterProxy(nodeId)


class TestRealm(object):
   implements(portal.IRealm)

   def __init__(self, eventMgr):
      self.mEventManager = eventMgr

   def requestAvatar(self, avatarId, mind, *interfaces):
      """ mind is nodeId
      """
      if not pb.IPerspective in interfaces:
         raise NotImplementedError, "No supported avatar interface."
      else:
         avatar = UserPerspective(self.mEventManager, avatarId)
         return pb.IPerspective, avatar, lambda: avatar.logout(mind)

def RunServer(installSH=True):
   logger = logging.getLogger('maestrod.RunServer')
   try:
      cluster_server = MaestroServer()
      cluster_server.registerInitialServices()
      from twisted.internet import reactor
      from twisted.internet import task

      #reactor.listenTCP(8789, pb.PBServerFactory(cluster_server.mEventManager))
      p = portal.Portal(TestRealm(cluster_server.mEventManager))
      pb_portal = pboverssl.PortalRoot(p)
      #factory = pb.PBServerFactory(p)
      factory = pboverssl.PBServerFactory(pb_portal)

      p.registerChecker(
         checkers.InMemoryUsernamePasswordDatabaseDontUse(aronb="aronb"))
      try:
         from util.pamchecker import PAMChecker
         p.registerChecker(PAMChecker())
      except:
         pass
      try:
         from util.winchecker import WindowsChecker
         p.registerChecker(WindowsChecker())
      except:
         pass
      #reactor.listenTCP(8789, factory)
      pk_path = os.path.join(os.path.dirname(__file__), 'server.pem')
      cert_path = os.path.join(os.path.dirname(__file__), 'server.pem')
      logger.info("Cert: " + cert_path)
      reactor.listenSSL(8789, factory,
         ssl.DefaultOpenSSLContextFactory(pk_path, cert_path))

      looping_call = task.LoopingCall(cluster_server.update)
      looping_call.start(0.1)
      reactor.run(installSignalHandlers=installSH)
   except Exception, ex:
      logger.error(ex)
      raise


def daemonize (stdin='/dev/null', stdout='/dev/null', stderr=None, pidfile=None):
   """This forks the current process into a daemon. The stdin, stdout,
   and stderr arguments are file names that will be opened and be used
   to replace the standard file descriptors in sys.stdin, sys.stdout,
   and sys.stderr. These arguments are optional and default to /dev/null.
   Note that stderr is opened unbuffered, so if it shares a file with
   stdout then interleaved output may not appear in the order that you
   expect.
   """
   # Do first fork.
   try:
      pid = os.fork()
      if pid > 0:
         sys.exit(0) # Exit first parent.
   except OSError, e:
      sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
      sys.exit(1)

   # Decouple from parent environment.
   os.chdir("/")
   os.umask(0)
   os.setsid()

   # Do second fork.
   try:
      pid = os.fork()
      if pid > 0:
         sys.exit(0) # Exit second parent.
   except OSError, e:
      sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
      sys.exit(1)

   # Process is now a daemon!

   # Open file descriptors
   if not stderr:
      stderr = stdout
   si = file(stdin, 'r')
   so = file(stdout, 'a+')
   se = file(stderr, 'a+', 0)

   # Redirect standard file descriptors.
   os.dup2(si.fileno(), sys.stdin.fileno())
   os.dup2(so.fileno(), sys.stdout.fileno())
   os.dup2(se.fileno(), sys.stderr.fileno())

   print "\n\nStarted Maestro on [%s]\n" % (str(datetime.datetime.today()))

   if pidfile:
      pf = file(pidfile, 'w+')
      pf.write('%d\n' % os.getpid())
      pf.close()

if __name__ == '__main__':
   # Set up logging to sys.stderr.
   logging.basicConfig(level = logging.DEBUG,
                       format = '%(name)-12s %(levelname)-8s %(message)s',
                       datefmt = '%m-%d %H:%M')

   if '-debug' in sys.argv:
      # For debugging, it is handy to be able to run the servers
      # without being a service on Windows or a daemon on Linux.
      RunServer()
   elif os.name == 'nt':
      # Install as a Windows Service on NT
      win32serviceutil.HandleCommandLine(vrjclusterserver)
   elif platform.system() == 'Linux':
      if '-log' in sys.argv:
         log = '/var/log/maestrod.log'
         print "Using log file: ", log
      else:
         log = '/dev/null'

      # Run as a daemon on Linux
      daemonize(pidfile='/var/run/maestrod.pid', stdout=log)

      # Now that we've successfully forked as a daemon, run the server
      RunServer()