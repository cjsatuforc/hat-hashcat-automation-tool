#!/usr/bin/python2.7
'''
#Creation Date - 05/12/2018
#Latest update - Pre-Release
#Last Modified - 05/12/2018
#Python Hashcat Automated Password Recovery
#Version 0.1
#Latest mod - N/A
#Currenty working in python 2.7
#Update to python 3 (to do)

#Useful Full commands
/opt/hashcat/hashcat -a 6 -m 5600 NetNTLMv2.hash -w 3 /opt/wordlists/english-words/english-words/words_first_letter_upper.txt '?a?a?a?a' -O --increment
/opt/hashcat/hashcat -a 0 -m 5600 NetNTLMv2.hash -w 3 --potfile-path ./mchugh.pot -O /opt/wordlists/rockyou.txt -r /opt/hashcat/rules/password_cracking_rules/OneRuleToRuleThemAll.rule
'''


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
            #hashcat_command_line_menu()
            return pot
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
    global attack_mode_inc_left
    global attack_mode_inc_right
    global cmd_defaults
    global four_any_characters
    global hash_type_NetNTLMv2
    global hash_path_and_name
    global increment
    global pot_file
    os.system('clear')
    print("Trying to crack you hash...")
    app = '/opt/hashcat/hashcat '
    attack_mode_brute_force = ' -a 0 ' 
    attack_mode_inc_right = ' -a 6 '
    attack_mode_inc_left = ' -a 7 '
    increment = ' --increment '
    hash_type_NetNTLMv2 = ' -m 5600 '
    hash_path_and_name = os.path.join(os.getcwd(), single_hash_file_name)
    pot_file = ' --potfile-path ' + pot
    cmd_defaults = ' -w 3 -O '
    four_any_characters = " ?a?a?a?a "
    print("----Running Hashcat Command")
'''
    print(repr(pot_file))
    print(type(pot_file))
    print(repr(cmd_defaults))
    print(type(cmd_defaults))
    print("All together Below")
'''

#Straight Wordlist_walk
def wordlist_walk():
    exten = '.txt'
    for dirpath, dirnames, files in os.walk(wordlist_directory):
        for wordlist_filename in files:
            if wordlist_filename.endswith(exten):
                abs_wordlist = (os.path.join(dirpath, wordlist_filename))
                subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + abs_wordlist + cmd_defaults, shell=True)
                                                                            


#Single Wordlist Testing                    
def singular_wordlist():
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + cmd_defaults, shell=True)

#Single list for menu 5 - Oxford Dictionary + Starting with UPPER Case + upto 4 ANY Characters on RIGHT SIDE
def hc_command_menu_5():
    subprocess.call(app + attack_mode_inc_right + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + wordlist_directory + four_any_characters + cmd_defaults + increment, shell=True)

#Single list for menu 6 - Oxford Dictionary + Starting with UPPER Case + upto 4 ANY Characters on LEFT SIDE
def hc_command_menu_6():
    subprocess.call(app + attack_mode_inc_left + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + four_any_characters + wordlist_directory + cmd_defaults + increment, shell=True)
    



#Crack Menu 0
def crack_menu_0(): # - Automated less than <1GB
    global wordlist_directory
    wordlist_directory = "/opt/wordlists/less-than-1GB/"
    pot_file()
    hashcat_command_line_menu()
    wordlist_walk()

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
        
#Crack Menu 5 - Oxfor Dic, capital letter, upto 4 characters, incrementally - RIGHT SIDE
def crack_menu_5():
    global wordlist_directory
    wordlist_directory = "/opt/wordlists/english-words/english-words/words_first_letter_upper.txt"
    pot_file()
    hashcat_command_line_menu()
    hc_command_menu_5()

#Crack Menu 6 - Oxfor Dic, capital letter, upto 4 characters, incrementally - LEFT SIDE
def crack_menu_6():
    global wordlist_directory
    wordlist_directory = "/opt/wordlists/english-words/english-words/words_first_letter_upper.txt"
    pot_file()
    hashcat_command_line_menu()
    hc_command_menu_6()
                
    
#Crack Menu 7 - rockyou.txt only 
def crack_menu_7():
    global single_wordlist
    single_wordlist = "/opt/wordlists/rockyou.txt"
    pot_file()
    hashcat_command_line_menu()
    singular_wordlist()
                        

    
        
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
            print("0) Automated Testing - Try all words lists between <1GB - 1GB - Common Credentials")
            print("1) Automated Testing - Try all words lists between 1GB - <2GB")
            print("2) Automated Testing - Try all words lists between 2GB - <3GB")
            print("3) Automated Testing - Try all words lists between 3GB - <4GB")
            print("4) Automated Testing - Try all words lists 4GB+ - (will take a while to cache each wordlist priot to testing)")
            print("5) Automated Testing - Try Oxford Dictionary + Starting with UPPER Case + upto 4 ANY Characters on RIGHT SIDE")
            print("6) Automated Testing - Try Oxford Dictionary + Starting with UPPER Case + upto 4 ANY Characters on LEFT SIDE")
            print("7) Automated Testing - Try rockyou")
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
    print("Example NetNTLMv2 Hash")
    print("NIGEL.BOYCE::MLTD:1122334455667788:1880e4d532d4825a6da1c60dfd3cefe9:01010000000000001a744106b78cd401252ceec0fdbd9d0e000000000200060053004d0042000100160053004d0042002d0054004f004f004c004b00490054000400120073006d0062002e006c006f00630061006c000300280073006500720076006500720032003000300033002e0073006d0062002e006c006f00630061006c000500120073006d0062002e006c006f00630061006c0008003000300000000000000000000000002000005387ece822900e4e5d75f8648229f71008a6e1effd5a059a3aa6b066ed75330b0a001000000000000000000000000000000000000900140048005400540050002f00790061006e006e0079000000000000000000" + "\n")
    print("OR" + "\n")
    print("admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030")
    print("")
    print("")
    single_hash = raw_input("Add your hash" + '\n')
    single_hash_string = str(single_hash)
    print("")
    print("Your Entry was" + '\n') + single_hash_string
    print("OK - Need to put the hash into a File...") # Put hash into a file
    single_hash_file_name = raw_input("Enter a logical filename: ")
    sh = open(single_hash_file_name, "w+")
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
