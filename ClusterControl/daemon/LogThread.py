import threading

class LogThread(threading.Thread):
   """
   Handles reading output from a running command so that the main GUI
   thread can display it.
   """
   def __init__(self, stdout, callback, subject):
      threading.Thread.__init__(self)

      self.mStdout   = stdout
      self.mKeepRunning = False
      self.mCallback = callback
      self.mSubject = subject

   def run(self):
      self.mKeepRunning = True

      count = 0
      while self.mKeepRunning and not self.mStdout.closed:
         
         # This blocks until there is output to read.  Since we know
         # from the select() call above there is something to read,
         # this should never block.
         l = self.mStdout.readline()

         # If nothing was read, the thread can exit.
         if l == "":
            self.mKeepRunning = False
         else:
            self.mCallback.publish(self.mSubject, l)
            print "DEBUG %d: %s" % (count, l),
            count += 1

      # This will cause the running application to exit.
      self.mStdout.close()

      print "Thread Done"

   def abort(self):
      """
      Tells this thread to stop reading from the command.

      At this time, this method does not know how to kill the spawned process
      that is generating the output.
      """
      self.mKeepRunning = False
