#!/usr/bin/python2

# Finance Manager by Rose22

# MAIN PROGRAM

import os

from custom_types import FinanceData
from custom_shells import MainShell

finance_data = FinanceData(os.path.expanduser("~/.financialmanager.p"))
shell = MainShell(finance_data)
shell.run_loop()
