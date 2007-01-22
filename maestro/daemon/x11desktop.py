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

import os
import os.path
import popen2
import pwd
import re

import maestro.util


def getUserXauthFile(userName):
   pw_entry = pwd.getpwnam(userName)
   user_home = pw_entry[5]
   return os.path.join(user_home, '.Xauthority')

def addAuthority(user, xauthCmd, xauthFile):
   '''
   Pulls the X authority key from the named file and adds it to the named
   user's .Xauthority file if necessary. A tuple containing the the display
   name (suitable for use as the value of the DISPLAY environment variable)
   and a boolean value indicating whether the user's .Xauthority file had to
   be updated is returned. If this boolean value is True, then it should be
   assumed that the user is logged on to the local workstation, and the
   authority should not be removed later using removeAuthority().
   '''
   (temp_stdout, temp_stdin) = popen2.popen2('/bin/hostname')

   # Read the output from /bin/hostname. Protect against EINTR just in case.
   hostname = maestro.util.readlineRetryOnEINTR(temp_stdout).strip()
   temp_stdout.close()
   temp_stdin.close()

   host_str = '%s/unix' % hostname

   # Pull out the system X authority key. It will be the first line of the
   # output from running 'xauth list'.
   (child_stdout, child_stdin) = \
      popen2.popen2('%s -f %s list' % (xauthCmd, xauthFile))

   # Read the output from running the above xauth command. Protect against
   # EINTR just in case.
   line = maestro.util.readlineRetryOnEINTR(child_stdout)
   child_stdout.close()
   child_stdin.close()

   key_str = re.sub('#ffff##', host_str, line)
   display_key_re = re.compile(r'\s*(\S+)\s+(\S+)\s+(\S+)\s*')
   key_match = display_key_re.match(key_str)
   key = (key_match.group(1), key_match.group(2), key_match.group(3))
   print key

   # The next step is to determine if the user's Xauthority file already has
   # the key that we just found. This has to be run as the authenticated user
   # since the owner of the maestrod process may not have access to that
   # user's files.

   # Start by opening a pipe so that the child process can communicate the
   # results of its examination of the user's Xauthority file.
   (child_read, child_write) = os.pipe()

   # Create the child process.
   pid = os.fork()
   if pid == 0:
      # The child process does not need to read from the pipe.
      os.close(child_read)

      # Run this process as the authenticated user.
      maestro.util.changeToUserName(user)

      # Run the xauth(1) command as the authenticated user (the new owner of
      # this child process).
      (child_stdout, child_stdin) = \
         popen2.popen2('%s -f %s list' % (xauthCmd, getUserXauthFile(user)))

      # Read the contents of the user's X authority file. This is not done
      # using readlines() because that could fail due to an interrupted system
      # call. Instead, we read lines one at a time and handle EINTR if an when
      # it occurs.
      lines = maestro.util.readlinesRetryOnEINTR(child_stdout)
      child_stdout.close()
      child_stdin.close()

      has_key = 0

      # Determine if the user's Xauthority file already has the key.
      for l in lines:
         key_match = display_key_re.match(l)
         user_key = (key_match.group(1), key_match.group(2),
                     key_match.group(3))
         if user_key == key:
            has_key = 1
            break

      # Tell the parent process about the results of examining the user's
      # Xauthority file.
      os.write(child_write, str(has_key))

      # And that's it for us! It is critical that os._exit() be used here
      # rather than sys.exit() in order to prevent a SystemExit exception from
      # being thrown.
      os._exit(0)

   # In the parent parocess, we close the write end of the pipe since we will
   # not be sending anything to the child process.
   os.close(child_write)

   # Then, we wait on the child process to send us the yay or nay result.
   result = os.read(child_read, 1)

   # Finally, we are done with the child process, so we close our read end of
   # the pipe and wait on the process to exit.
   os.close(child_read)
   maestro.util.waitpidRetryOnEINTR(pid, 0)

   has_key = result == '1'

   # If the user's Xauthority file does not have the key, then we add it.
   if not has_key:
      pid = os.fork()
      if pid == 0:
         # Run the xauth(1) command as the user.
         maestro.util.changeToUserName(user)
         os.execl(xauthCmd, xauthCmd, '-f', getUserXauthFile(user), 'add',
                  key[0], key[1], key[2])

      # Wait on the child to complete.
      maestro.util.waitpidRetryOnEINTR(pid, 0)

   return (key[0], has_key)

def removeAuthority(user, xauthCmd, displayName):
   '''
   Removes the named display from the given user's .Xauthority file.

   NOTE: This relies upon the user running maestrod to have write access to
         the named user's .Xauthority file.
   '''
   pid = os.fork()
   if pid == 0:
      # Run the xauth(1) command as the named user.
      maestro.util.changeToUserName(user)
      os.execl(xauthCmd, xauthCmd, '-f', getUserXauthFile(user), 'remove',
               displayName)

   # Wait on the child to complete.
   maestro.util.waitpidRetryOnEINTR(pid, 0)
