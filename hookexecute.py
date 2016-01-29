"""
Copyright (C) 2015-2016 Alan Drees

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

Purpose:
 Simple python-based hook calling mechnaism, called in order of filename

Dependencies:
 os
 sys
 stat
 subprocess
 time
"""
import os
import sys
import stat
import subprocess
import time

class HookExecutor:
    """
    This class implements the logic required to execute the directory of
    arbitrary executables
    """

    executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH

    def __init__(self, hook_directory, logfile):
        """
        Constructor

        @param self (object) object reference
        @param hook_directory (string) path to the hook directory to execute the hooks from
        @param logfile (string) path to the logfile to be created and/or appended to

        @returns None
        """

        if os.path.isdir(hook_directory):
            self.hook_directory = hook_directory
        else:
            print("Path doesn't exist. Exiting")
            exit();

        self.hooks = list()

        if not os.path.isfile(logfile):
            with open(logfile, "w") as outfile:
                outfile.write("")

        self.log_filename = logfile

        self.log_buffer = ""

        return None

    def __enter__(self):
        """
        Enter function to facilitate python's with statement requirements

        @param self object (object) reference

        @returns self
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Exit function to facilitate python's with statement requirements

        @param self (object) object reference
        @param type (string) type value
        @param value (???) ???
        @param traceback (???) ???

        @returns None
        """

        if self.log_buffer == "":
            self.log_buffer = time.strftime("%Y--%m %H:%M:%S") + " execution ok!\n"

        with open(self.log_filename, "a") as outfile:
            outfile.write(self.log_buffer)
        pass

    def get_executables(self):
        """
        Gets the executables in the specified directory

        @param None

        @returns None
        """

        for filename in os.listdir(self.hook_directory):
            if os.path.isfile(self.hook_directory + '/' + filename):
                st   = os.stat(self.hook_directory + '/' + filename)
                mode = st.st_mode
                uid  = st.st_uid
                if (mode & HookExecutor.executable) and (uid == os.geteuid()):
                    self.hooks.append(self.hook_directory + '/' + filename)

        self.hooks.sort()
        return None

    def run_executables(self):
        """
        Execute the executables in the specified hook_directory

        @param None

        @returns None
        """

        for executable in self.hooks:
            try:
                subprocess.call(executable)
            except OSError:
                self.log_buffer += time.strftime("%d-%m-%Y %H:%M:%S") + " -- " + executable + ": " + "not executed\n"
