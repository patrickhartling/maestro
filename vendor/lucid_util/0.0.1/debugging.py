# Utility methods for debugging.
#
#
import sys, traceback, linecache

def qualified_class_name(cls):
   """ Get name of class with full namespace. """
   return "%s.%s"%(cls.__module__,cls.__name__)


def get_frame_scope_name(frame):
   if frame.f_locals.has_key('self'):
      me = frame.f_locals['self']
      if hasattr(me, '__class__'):
         name = qualified_class_name(me.__class__)
      else:
         name = qualified_class_name(type(me))         
      return '%s : %s' % (name, frame.f_code.co_name)
   else:
      return '%s : %s' % (frame.f_code.co_filename, frame.f_code.co_name )
   
def scope_dump(frame, s, ignored):
   """ Trace function for sys.settrace. """      
   print get_frame_scope_name(frame)
   return None

def full_dump(frame, event, arg):
   """ Trace function for sys.settrace. """   
   
   if "call" == event:
      print "call: ", get_frame_scope_name(frame)      
   elif "return" == event:
      print "[%s] return: %s"%(get_frame_scope_name(frame), arg)
   #elif "exception" == event:
   #   print "[%s:%s] exception: "%(get_frame_scope_name(frame), frame.f_lineno)
   #   traceback.print_exception(*arg)
   elif "line" == event:
      lineno = frame.f_lineno
      filename = frame.f_code.co_filename
      line = linecache.getline(filename, lineno)
      print "%s:%s %s"%(get_frame_scope_name(frame), lineno, line),

   return full_dump


def hookScopeTrace():
   sys.settrace(trace_dump)

def hookFullTrace():
   sys.settrace(full_dump)
   
def removeTrace():
   sys.settrace(None)
   

   
