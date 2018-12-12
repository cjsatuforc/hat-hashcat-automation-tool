
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

#less_than_1_GB_wordlists = "/opt/wordlists/less_than_1_GB"
#wordlist = os.walk(less_than_1_GB_wordlists)
#print wordlist

#for files in os.walk("/opt/wordlists/less-than-1GB"):
#    print "bytes in", len(files), "non-directory files"



#To Do for next stage of testing###
#subprocess.call("/opt/hashcat/hashcat -a 6 -m 5600 NetNTLMv2.hash -w 3 \?a\?a\?a\?a -O --increment " + name, shell=True)

# The top argument for walk
topdir = '/opt/wordlists/less-than-1GB/'

# The extension to search for
exten = '.txt'


for dirpath, dirnames, files in os.walk(topdir):
    for name in files:
        if name.endswith(exten):
            #print(os.path.join(dirpath, name))
            name = (os.path.join(dirpath, name))
            #print(name)
            subprocess.call("/opt/hashcat/hashcat -a 0 -m 5600 NetNTLMv2.hash -w 3 -O " + name, shell=True)
            

