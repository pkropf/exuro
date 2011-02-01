# -*- coding: utf-8 -*-

import atexit
import os
import readline
import rlcompleter

historyPath = os.path.expanduser("~/.pyhistory")

def save_history(historyPath=historyPath):
    try:
        import readline
        readline.write_history_file(historyPath)
    except ImportError:
        pass

if os.path.exists(historyPath):
    readline.read_history_file(historyPath)

atexit.register(save_history)
readline.parse_and_bind('tab: complete')
del os, atexit, readline, rlcompleter, save_history, historyPath
