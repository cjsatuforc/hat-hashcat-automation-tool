#!/usr/bin/env python

import subprocess

string = subprocess.call("ls " + "-l" + " /opt/wordlists/less-than-1GB", shell=True)
print string
