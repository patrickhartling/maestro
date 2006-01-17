import sys, os, types, platform
#import essf
#import rvp
import Pyro.core
import Pyro.naming
import popen2

from Queue import Queue

#platform.system()
#os.uname()
#sys.platform
ERROR = 0
LINUX = 1
WIN = 2
WINXP = 3
MACOS = 4
MACOSX = 5
HPUX = 6
AIX = 7
SOLARIS = 8

OsNameMap = {ERROR  : 'Error',
             LINUX  : 'Linux',
             WIN    : 'Windows',
             WINXP  : 'Windows XP',
             MACOS  : 'MacOS',
             MACOSX : 'MacOS X',
             HPUX   : 'HP UX',
             AIX    : 'AIX',
             SOLARIS : 'Solaris'}

if os.name == 'nt':
    import win32api, win32event, win32serviceutil, win32service, win32security, ntsecuritycon

class SettingsService(Pyro.core.ObjBase):
   def __init__(self):
      Pyro.core.ObjBase.__init__(self)
      self.mQueue = Queue()

   def getPlatform(self):
      """Returns tuple with error code and platform code.
         1 is Linux, 2 is Windows, and 0 is unknown."""
      if platform.system() == 'Linux':
         return LINUX
      elif os.name == 'nt':
         return WINXP
      else:
         return ERROR

   def getPlatformName(self):
      try:
         return OsNameMap[self.getPlatform()]
      except:
         return 'Unknown'

   def rebootSystem(self):
      if os.name == 'nt':
         AdjustPrivilege(ntsecuritycon.SE_SHUTDOWN_NAME, 1)
         message = 'The system is rebooting now'
         try:
            win32api.InitiateSystemShutdown(None, message, 0, 1, 1)
         finally:
            AdjustPrivilege(ntsecuritycon.SE_SHUTDOWN_NAME, 0)
      else:
         os.system('shutdown -r now')
      return 0

   def shutdownSystem(self):
      if os.name == 'nt':
         AdjustPrivilege(ntsecuritycon.SE_SHUTDOWN_NAME, 1)
         message = 'The system is rebooting now'
         try:
            win32api.InitiateSystemShutdown(None, message, 0, 1, 0)
         finally:
            AdjustPrivilege(ntsecuritycon.SE_SHUTDOWN_NAME, 0)
      else:
         os.system('shutdown -h now')
      return 0
