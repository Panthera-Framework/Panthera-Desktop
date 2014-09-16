#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
import os
import time

__author__ = "Damian Kęska"
__license__ = "LGPLv3"
__maintainer__ = "Damian Kęska"
__copyright__ = "Copyleft by Panthera Desktop Team"

# get current working directory to include local files (debugging mode)
t = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "src/"

if os.path.isdir(t):
    sys.path.append(t)
    
import pantheradesktop.kernel

# initialize kernel
kernel = pantheradesktop.kernel.pantheraDesktopApplication()
kernel.coreClasses['gui'] = False
kernel.coreClasses['db'] = False
kernel.initialize(quiet=False)
kernel.main()

threads = {}
functions = ["printA", "printB"]

# first threading function that will work in background
def printA(thread=1):
    while True:
        print("AAAA\n")
        time.sleep(1.5)

# second threading function that will work in background
def printB(thread=1):
    while True:
        print("BBBB\n")
        time.sleep(1)

# let's this example be dynamical and create X number of threads basing on array
for function in functions:
    thread, worker = pantheradesktop.kernel.createThread(eval(function))
    threads[function] = [thread,worker] # we have to save thread and worker object's in memory until they will not finish working

# and main application thread
while True:
    time.sleep(5);
    print("CCCC\n")
