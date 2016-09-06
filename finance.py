#!/usr/bin/python2

# Copyright (c) 2016 Rose (Rose22)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import imp

# Get readline functionality if it's available
try:
    import readline
except ImportError:
    pass

# Load the config
imp.load_source("config", "finance.conf")
import config

# Load all requires classes
from custom_types import FinanceData
from custom_shells import MainShell

# Run the main loop
finance_data = FinanceData(os.path.expanduser(config.path))
shell = MainShell(finance_data)
shell.run_loop()
