#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
import os

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
kernel.initialize(quiet=False)
kernel.main()

# SQL Test
query = kernel.db.query('SELECT * FROM `lnx_config_overlay` WHERE `key` = :key', {'key': 'autoloader'})
query.indexColumn = 'key'

print(query.fetchAll())

