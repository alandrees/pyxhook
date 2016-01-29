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
 Implements an application frontend for the HookExecutor class

Dependencies:
 sys
 hookexecute
"""


import sys
import hookexecute


if __name__ == "__main__":
    if len(sys.argv) == 3:
        with hookexecute.HookExecutor(sys.argv[1], sys.argv[2]) as x:
            x.get_executables()
            x.run_executables()
    else:
        print("Not enough arguments.")
        print("python-hook-execute.py <directory_name> <logfile_name>")
