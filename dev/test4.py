
#!/usr/bin/env python

import subprocess
import os

#working 1
#string = subprocess.call("ls " + "-l" + " /opt/wordlists/less-than-1GB", shell=True)
#print string

#working 2
#string = subprocess.call("find /home/awer -type f -iname '*hashcat*'", shell=True)
#print string

#file = "hashcat-dev-1.py"
#string = subprocess.call("find /home/awer -type f -iname " + file, shell=True)
#print string

global foo
global bar
foo = False
bar = True

global power
power = 'on'


def test1():
    global foo
    foo = True
    test2()

    
def test2():
   if foo == True and power == 'on':
       print("foo True, power on")
   elif foo == False and power == 'on':
       print("foo == False, power on")

test1()
