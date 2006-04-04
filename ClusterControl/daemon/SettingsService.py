import sys, os, types, platform
#import essf
#import rvp
import Pyro.core
import Pyro.naming
import popen2
import re
import time
import string

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

TIMEFORMAT = "%m/%d/%y %H:%M:%S"

PAT_STAT_CPU = re.compile(r"cpu +([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+)", re.I)
PAT_MEMINFO = re.compile(r"([a-zA-Z0-9]+): *([0-9]+)", re.I)
PAT_MEMINFO_MEMFREE = re.compile(r"memfree: *([0-9]+)", re.I)
PAT_MEMINFO_BUFF = re.compile(r"buffers: *([0-9]+)", re.I)
PAT_MEMINFO_CACHED = re.compile(r"cached: *([0-9]+)", re.I)
PAT_MEMINFO_SWAPTOTAL = re.compile(r"swaptotal: *([0-9]+)", re.I)
PAT_MEMINFO_SWAPFREE = re.compile(r"swapfree: *([0-9]+)", re.I)
PAT_MEMINFO_ACTIVE = re.compile(r"active: *([0-9]+)", re.I)
PAT_MEMINFO_INACTIVE = re.compile(r"inactive: *([0-9]+)", re.I)

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

      if os.name != 'nt':
         self.mLastCPUTime = [0,0,0,0]

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


   def getCpuUsage(self):
      if os.name == 'nt':
         return 0.0
      else:
         statFile = file("/proc/stat", "r")
         for line in statFile.readlines():
            m = PAT_STAT_CPU.match(line)
            if m:
               current_time = map(long, m.groups())
               diff_time = [0,0,0,0]
               for i in xrange(4):
                  diff_time[i] = current_time[i] - self.mLastCPUTime[i]
               self.mLastCPUTime = current_time
               (tuser, tnice, tsys, tidle) = diff_time
               #print "User [%s] nice [%s] sys [%s] idle [%s]" % (tuser, tnice, tsys, tidle)
               cpu_usage = 100.00 - 100.00 * (float(diff_time[3]) / sum(diff_time))
               print cpu_usage
               return cpu_usage
            else:
               return 0.0

   def getMemUsage(self):
      # mpused, mpswaped, mpactive, mpinactive
      fp = open("/proc/meminfo")
      dic = {}
      for line in fp.readlines():
         m = PAT_MEMINFO.match(line)
         if m:
            dic[string.lower(m.group(1))] = long(m.group(2))
      fp.close()
      mtotal = dic.get('memtotal', 1)
      mfree = dic.get('memfree', 0) + dic.get('buffers',0) + dic.get('cached',0)
      mem_usage = float(mtotal-mfree)/mtotal
      swap_usage = float(dic.get('swaptotal',0) - dic.get('swapfree',0))/mtotal
      return (mem_usage * 100.0, swap_usage * 100.0)
      
   def getTime(self):
      return time.strftime(TIMEFORMAT)


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
