import os
import select
import threading

class LogThread(threading.Thread):
   """
   Handles reading output from a running command so that the main GUI
   thread can display it.
   """
   def __init__(self, cmdStdout, owner):
      threading.Thread.__init__(self)

      self.cmdStdout   = cmdStdout
      self.owner       = owner
      self.keepRunning = False

   def run(self):
      self.keepRunning = True

      count = 0
      while self.keepRunning and not self.cmdStdout.closed:
         
         # This blocks until there is output to read.  Since we know
         # from the select() call above there is something to read,
         # this should never block.
         l = self.cmdStdout.readline()
               

         # If nothing was read, the thread can exit.
         if l == "":
            self.keepRunning = False
         else:
            print "DEBUG %d: %s" % (count, l),
            count += 1

      # This will cause the running application to exit.
      self.cmdStdout.close()

      # Tell our owner that we're closing down the shop.
      #self.owner.threadFinished(self)
      print "Thread Done"

   def abort(self):
      """
      Tells this thread to stop reading from the command.

      At this time, this method does not know how to kill the spawned process
      that is generating the output.
      """
      self.keepRunning = False
