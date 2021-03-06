#!/usr/bin/python2.7
#coding=utf-8
#
#Creation Date - 05/12/2018
#Latest update - Pre-Release
#Last Modified - 05/12/2018
#Python Hashcat Automated Password Recovery
#Version 0.1
#Latest mod - N/A
#Currenty working in python 2.7
#Update to python 3 (to do)


#Useful Full commands
#/opt/hashcat/hashcat -a 6 -m 5600 NetNTLMv2.hash -w 3 /opt/wordlists/english-words/english-words/words_first_letter_upper.txt '?a?a?a?a' -O --increment
#/opt/hashcat/hashcat -a 0 -m 5600 NetNTLMv2.hash -w 3 --potfile-path ./mchugh.pot -O /opt/wordlists/rockyou.txt -r /opt/hashcat/rules/password_cracking_rules/OneRuleToRuleThemAll.rule


#Module Imports
import datetime
import os
import platform
import shlex
import subprocess
import sys
import time


#Define Colours
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
def prCyan(prt): print("\033[96m {}\033[00m" .format(prt))
def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))

# python2/3 compatability
try:
    input = raw_input
except NameError:
    pass
    
#Initally Clear the Screen
os.system('clear')

global hashcat_path
hashcat_path = os.path.dirname(os.path.realpath(__file__))


#Banner
def banner():
    prGreen("                                                                             ")
    prGreen("                                                                     ,       ")
    prGreen("                                                        __...eee8888P        ")
    prGreen("                                 .effe.     .e88e....____.e888888.*****`    ,")
    prGreen("                                ^888888b   :88888888888888888888eeee8888888P ")
    prGreen("                                ^8888888b  :****8888888888888888888888****   ")
    prGreen("                                 |`|`8888b.    o  `**8888******888**         ")
    prGreen("                                     `8888b...__.  A.___.e888**'             ")
    prGreen("                                      `8888888P d8888888888'  ,              ")
    prGreen("Welcome to the Automated Hashcat Menu  '***** d88888888P*****'               ")
    prGreen("                                       __..eed8888888888eee..                ")
    prGreen("                              .|,|_.ed88888888***```````**888L               ")
    prGreen("                              `*YY*****'                                     ")
     
#os.system('whoami')
#subprocess.call("while true; do printf '%s\r' "$(date)"; sleep 1; done", shell=True)
#date()
    
#Date
#def date():
#    print("Date: ", datetime.datetime.now())

#Pot File
def pot_file():
    global pot
    pot_name = raw_input("Enter Name for pot file, or Press 1 for same name as filename previously selected" +'\n')
    try:
        if pot_name == "1":
            print(single_hash_file_name)
            pot = single_hash_file_name.lower()
            pot = pot + '.pot '
            pot_create = open(pot, "w+")
            pot_create.close()
            os.chmod(pot, 0o755) #NOT A TYPO- Written in Octel Format
            print("File Created")
            hashcat_command_line_menu()
        else:
            print(pot_name)
            pot = pot_name.lower()
            pot = pot + ".pot "
            os.chmod(pot, 0o755) #NOT A TYPO- Written in Octel Format
            hashcat_command_line_menu()
    except KeyboardInterrupt:
        sys.exit()

    
#Hashcat Command Line Menu
def hashcat_command_line_menu():
    global app
    global attack_mode_brute_force
    global hash_type_NetNTLMv2
    global hash_path_and_name
    global pot_file
    global cmd_defaults
    os.system('clear')
    print("Trying to crack you hash...")
    app = '/opt/hashcat/hashcat '
    attack_mode_brute_force = ' -a 0 ' 
    hash_type_NetNTLMv2 = ' -m 5600 '
    hash_path_and_name = os.path.join(os.getcwd(), single_hash_file_name)
    pot_file = ' --potfile-path ' + pot
    cmd_defaults = ' -w 3 -O '
    print("----Running Hashcat Command")
    print(repr(app))
    print(type(app))
    print(repr(attack_mode_brute_force))
    print(type(attack_mode_brute_force))
    print(repr(hash_type_NetNTLMv2))
    print(type(hash_type_NetNTLMv2))
    print("")
    print(repr(hash_path_and_name))
    print(type(hash_path_and_name))
    print(repr(pot_file))
    print(type(pot_file))
    #print(repr(wordlist))
    #print(type(wordlist))
    print(repr(cmd_defaults))
    print(type(cmd_defaults))
    print("All together Below")
    print(repr(app),(attack_mode_brute_force),(hash_type_NetNTLMv2),(hash_path_and_name),(pot_file),(wordlist),(cmd_defaults))
    input("Press to Continue..")
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + wordlist + cmd_defaults, shell=True)
#subprocess.call("/opt/hashcat/hashcat -a 0 -m 5600 NetNTLMv2.hash -w 3 -O " + wordlist, shell=True)
#print(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + wordlist_split + cmd_defaults)
    #subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + wordlist + cmd_defaults, shell=True)
#subprocess.call("/opt/hashcat/hashcat -a 0 -m 5600 NetNTLMv2.hash -w 3 -O /opt/wordlists/rockyou.txt", shell=True)


#Wordlists - Auto
def auto_wordlists():
    topdir = '/opt/wordlists/less-than-1GB/'
    exten = '.txt'
    for dirpath, dirnames, files in os.walk(topdir):
        for wordlist_filename in files:
            if wordlist_filename.endswith(exten):
                wordlist = (os.path.join(dirpath, wordlist_filename))
                print(repr(app),(attack_mode_brute_force),(hash_type_NetNTLMv2),(hash_path_and_name),(pot_file),(wordlist),(cmd_defaults))
                input("Press to continue")
                subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + wordlist + cmd_defaults, shell=True)
                return wordlist
            
#Rules Menu

#Crack Menu 0
def crack_menu_0(): # - Automated less than <1GB
    str(wordlist) = "/opt/wordlists/less-than-1GB/"
    #listdir = os.listdir(path)
    #listdir = str(listdir)
    #wordlist = os.path.join(path, listdir)
    pot_file()

    
#Crack Menu 1
def crack_menu_1():
    os.system('clear')
    print("")
        
#Crack Menu 2
def crack_menu_2():
    os.system('clear')
        
#Crack Menu 3
def crack_menu_3():
    os.system('clear')
        
#Crack Menu 4
def crack_menu_4():
    os.system('clear')
        
#Crack Menu 5
def crack_menu_5():
    os.system('clear')
        
#Crack Menu 6 - Rockyou-75.txt only
def crack_menu_6():
    global wordlist
    os.system('clear')
    wordlist = " /opt/wordlists/rockyou-75.txt "
    pot_file()
    
#Crack Menu 7
def crack_menu_7():
    os.system('clear')
        
#Crack Menu 8 - Back Crack - go back one stage...
def back_crack():
    os.system('clear')
    main_menu()
        

#Cracking Menu
def crack_menu():
    os.system('clear')
    banner()
    try:
        while 1:
            print("")
            print("Hashcat Cracking Menu")
            print("Only for NTLM or NetNTLM - WPA or WEP to DO")
            print("0) Automated Testing - Try all words lists between <1GB - 1GB")
            print("1) Automated Testing - Try all words lists between 1GB - <2GB")
            print("2) Automated Testing - Try all words lists between 2GB - <3GB")
            print("3) Automated Testing - Try all words lists between 3GB - <4GB")
            print("4) Automated Testing - Try all words lists 4GB+")
            print("5) Automated Testing - Try all words lists between <1GB - 4GB+")
            print("6) Automated Testing - Try rockyou")
            print("7) Automated Testing - Try rockyou with rules - To be added")
            print("8) Back")
            crack_option = {"0": crack_menu_0,
                            "1": crack_menu_1,
                            "2": crack_menu_2,
                            "3": crack_menu_3,
                            "4": crack_menu_4,
                            "5": crack_menu_5,
                            "6": crack_menu_6,
                            "7": crack_menu_7,
                            "8": back_crack
                           }
            try:
                selection = input("\nSelect an Option: ")
                crack_option[selection]()
            except KeyError:
                pass
    except KeyboardInterrupt:
                sys.exit()
                
                  
        
#Hashcat Command Menu
#def hashcat_command_menu(): #hashcat -a 0 -m 1000 /opt/hashcat/ntlm.txt /opt/wordlists/english-words/words-apha-lower.txt -O -w 3

        
#Single Hash Menu
def single_hash_menu():
    global single_hash_file_name
    os.system('clear')
    banner()
    print("BANNER TO DO")
    print("Example NetNTLMv2 Hash")
    print("joe.bloggs::EVILCORP:1122334455667788:1485E4D637D4827A6DA1660DFD6CEFE9:11011000100100001A744106B78CD401252CEEC0FDBD9D0E000000000200060053004D0042000100160053004D0042002D0054004F004F004C004B00490054000400120073006D0062002E006C006F00630061006C000300280073006500720076006500720032003000300033002E0073006D0062002E006C006F00630061006C000500120073006D0062002E006C006F00630061006C0008003000300000000000000000000000002000005387ECE822900E4E5D75F8648229F71008A6E1EFFD5A059A3AA6B066ED75330B0A001000000000000000000000000000000000000900140048005400540050002F00790061006E006E0079000000000000000000" + "\n")
    print("OR" + "\n")
    print("admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030")
    print("")
    print("")
    single_hash = raw_input("Add your hash" + '\n')
    #single_hash_string = [single_hash]
    single_hash_string = str(single_hash)
    print("")
    print("Your Entry was - ") + single_hash_string
    print("OK - Need to put the hash into a File...") # Put hash into a file
    single_hash_file_name = raw_input("Enter a logical filename: ")
    sh = open(single_hash_file_name, "w")
    sh.write(single_hash_string)
    print("File Created")
    sh.close()
    crack_menu()

    
#Hash File Upload Menu - TODO
def hash_from_file():
    print("Work in Progress")
    sys.exit()

#Exit system
def program_exit():
    sys.exit()

    
            
#MainMenu

def main_menu():
    try:
        while 1:
            banner()
            print("\t(0) Input Singluar Hash")
            print("\t(1) Input Hash from File")
            print("\t(2) Exit")
            options = {"0": single_hash_menu,
                       "1": hash_from_file,
                       "2": program_exit,
                      }
            try:
                task = input("\nChoose an Option: ")
                options[task]()
            except KeyError:
                os.system('clear')
                pass
    except KeyboardInterrupt:
                sys.exit()

if __name__ == '__main__':
    main_menu()
