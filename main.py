#!/usr/bin/env python
import sys
import os

# get current working directory to include local files (debugging mode)
t = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "src/"

if os.path.isdir(t):
    sys.path.append(t)
    
import pantheradesktop.kernel

# initialize kernel
kernel = pantheradesktop.kernel.pantheraDesktopApplication()
