#!/usr/bin/env python

import subprocess

#working 1
#string = subprocess.call("ls " + "-l" + " /opt/wordlists/less-than-1GB", shell=True)
#print string

#working 2
#string = subprocess.call("find /home/awer -type f -iname '*hashcat*'", shell=True)
#print string

file = "hashcat-dev-1.py"
string = subprocess.call("find /home/awer -type f -iname " + file, shell=True)
print string

