#!/usr/bin/python2.7
'''
#Creation Date - 05/12/2018
#Latest update - Pre-Release
#Last Modified - 20/12/2018
#Python Hashcat Automated Password Recovery
#Version 0.21
#Latest mod - N/A
#Currenty working in python 2.7
#Update to python 3 (to do)
#Added Functionality for Cewl Lists

#Useful Full commands
/opt/hashcat/hashcat -a 6 -m 5600 NetNTLMv2.hash -w 3 /opt/wordlists/english-words/english-words/words_first_letter_upper.txt '?a?a?a?a' -O --increment
/opt/hashcat/hashcat -a 0 -m 5600 NetNTLMv2.hash -w 3 --potfile-path ./mchugh.pot -O /opt/wordlists/rockyou.txt -r /opt/hashcat/rules/password_cracking_rules/OneRuleToRuleThemAll.rule
'''


#Module Imports
import datetime
import fnmatch
import os
import platform
import shlex
import subprocess
import sys
import time
from os import listdir
from os.path import isfile, join

#Define Colours
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
def prCyan(prt): print("\033[96m {}\033[00m" .format(prt))
def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))

#Python2/3 compatability
try:
    input = raw_input
except NameError:
    pass
    
#Both Values are set to false on program start. This is used to trigger the pot file and hash upload functionality.
#global file_hash_boolean
file_hash_boolean = False
#global single_hash_boolean
single_hash_boolean = False

#Used to allow multiple tests via the menu with the same pot file already selected.
#Note Global pot_boolean resides inside the pot_function() function block. 
pot_boolean = False

#Used for supporting the cewl wordlists if standard wordlists are not getting results
cewl_boolean = False

#Initally Clear the Screen
os.system('clear')

#Declare Paths
hashcat_path = "/opt/hat-hashcat-automation-tool/"
l00t_pot_dir = os.path.join(hashcat_path, 'l00t')
rules_dir = os.path.join(hashcat_path, 'rules')
hash_upload_dir = os.path.join(hashcat_path, 'hash_upload')
cewl_upload_dir = os.path.join(hashcat_path, 'cewl_wordlists')

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
    print("")
     

#Pot File - Create a New Potfile when using a Single wordlist or the File Upload Functionality.
def pot_function():
    global pot_boolean
    global pot_file
    global hash_path_and_name
    global single_hash_file_name
    global hash_abs_path
    global cewl_boolean
    pot_name = input("Enter Name for pot file, or Press 1 for the same name as filename previously selected" +'\n')
#Added Pot Boolean Functionality to allow for multiple tests with the SAME hash and pot settings
#After the first iteration the pot_boolean becomes true and therefore we call on the settings already provided.
    if pot_boolean == True and single_hash_boolean == True and pot_name == '1': #Re-check the value of the hash file and pot name as these may of changed since the last run. Handy to change hashes without exiting the program.       print("")
        pot = hash_input.lower()
        pot = pot + '.pot '
        hash_path_and_name = single_hash_abs_path
        pot_file = ' --potfile-path ' + os.path.join(l00t_pot_dir, pot)
    elif pot_boolean == True and pot_name == '1' and file_hash_boolean == True:
        pot = hash_input.lower()
        pot = pot + '.pot '
        hash_path_and_name = hash_abs_path
        pot_file = ' --potfile-path ' + os.path.join(l00t_pot_dir, pot)
    elif single_hash_boolean == True and pot_name == '1':
        pot = single_hash_file_name.lower()
        pot = pot + '.pot ' #No need to create a file here as hashcat will automajically make one and therefore we will have duplicates
        hash_path_and_name = os.path.join(os.getcwd(), single_hash_file_name)
        pot_file = ' --potfile-path ' + os.path.join(l00t_pot_dir, pot)
        pot_boolean = True
    elif file_hash_boolean == True and pot_name == '1':
        pot = hash_input.lower()
        pot = pot + '.pot '
        hash_path_and_name = hash_abs_path
        pot_file = ' --potfile-path ' + os.path.join(l00t_pot_dir, pot)
        pot_boolean = True
    elif cewl_boolean == True and pot_name == '1':
        pot = hash_input.lower()
        pot = pot + '.pot '
        hash_path_and_name = hash_abs_path
        pot_file = ' --potfile-path ' + os.path.join(l00t_pot_dir, pot)
    else:
        print(pot_name)
        pot = pot_name.lower()
        pot = pot + '.pot '
        hashcat_command_line_menu()
            
    
#Hashcat Command Line Menu
def hashcat_command_line_menu():
    global app
    global attack_mode_brute_force
    global attack_mode_inc_left
    global attack_mode_inc_right
    global cmd_defaults
    global four_numbers
    global five_any_characters
    global hash_type_NetNTLMv2
    global increment
    global increment_min
    global increment_max
    global rule_set_arg
    global three_any_characters
    os.system('clear')
    print("Trying to crack your hash...")
    app = '/opt/hashcat/hashcat '
    attack_mode_brute_force = ' -a 0 ' 
    attack_mode_inc_right = ' -a 6 '
    attack_mode_inc_left = ' -a 7 '
    cmd_defaults = ' -w 3 -O '
    five_any_characters = " \"?a?a?a?a?a\" "
    four_numbers = " ?d?d?d?d "
    hash_type_NetNTLMv2 = ' -m 5600 '
    increment = ' --increment'
    increment_min = ' --increment-min 1 '
    increment_max = ' --increment-max 3 '
    rule_set_arg = ' -r '
    three_any_characters = " ?a?a?a "
    print("----Running Hashcat Command----")


#Straight Wordlist_walk
def wordlist_walk():
    exten = ''
    for dirpath, dirnames, files in os.walk(wordlist_directory):
        for wordlist_filename in files:
            if wordlist_filename.endswith(exten):
                abs_wordlist = (os.path.join(dirpath, wordlist_filename))
                subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + abs_wordlist + cmd_defaults, shell=True)
                os.system('clear')
                

#Rule Set Walk
def rule_set_walk():
    exten = '*.rule'
    for root, dirs, files in os.walk(rule_set_directory):
        for filename in fnmatch.filter(files, exten):
            abs_rule_set = (os.path.join(root, filename))
            subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + cmd_defaults + pot_file + single_wordlist + rule_set_arg + abs_rule_set, shell=True)
            os.system('clear')

            
#Single Wordlist
def singular_wordlist():
    global hash_path_and_name
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + cmd_defaults, shell=True)
    os.system('clear')
    
#Single list for menu 5 - Oxford Dictionary + Starting with UPPER Case + upto 3 ANY Characters on RIGHT SIDE
def hc_command_menu_5():
    #print(app + attack_mode_inc_right + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + wordlist_directory + three_any_characters + cmd_defaults + increment + increment_min + increment_max)
    subprocess.call(app + attack_mode_inc_right + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + three_any_characters + cmd_defaults + increment, shell=True)
    os.system('clear')
    
#Single list for menu 6 - Oxford Dictionary + Starting with UPPER Case + upto 3 ANY Characters on LEFT SIDE
def hc_command_menu_6():
    subprocess.call(app + attack_mode_inc_left + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + three_any_characters + single_wordlist + cmd_defaults + increment, shell=True)
    os.system('clear')
    
#Hashcat Dictionary wordlist with rules - Oxford Dictionary Starting with UPPER Case + {upto 4 Numbers LEFT SIDE, upto 4 numbers RIGHT SIDE}
def hc_command_menu_7():
    #Four Numbers (Left Side)
    subprocess.call(app + attack_mode_inc_left + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + four_numbers + single_wordlist + cmd_defaults + increment, shell=True)
    #Four Numbers (Right Side)
    subprocess.call(app + attack_mode_inc_right + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + four_numbers + cmd_defaults + increment, shell=True)
    os.system('clear')

#Rule set Directory 11 # L33t speak rules (leetspeak.rule + unix-ninja-leetspeak.rule)
def hc_command_menu_11():
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_file_1 + cmd_defaults, shell=True)
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_file_2 + cmd_defaults, shell=True)
    os.system('clear')

#Hashcat with Rule Sets
def singular_wordlist_rule_set():
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_directory + cmd_defaults, shell=True)
    os.system('clear')
    
#Hashcat with Rule Sets - For rule 3 multiple custom Rules
def multiple_wordlist_rule_set():
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_file_1 + cmd_defaults, shell=True)
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_file_2 + cmd_defaults, shell=True)
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_file_3 + cmd_defaults, shell=True)
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_file_4 + cmd_defaults, shell=True)
    subprocess.call(app + attack_mode_brute_force + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + rule_set_arg + rule_set_file_5 + cmd_defaults, shell=True)
    os.system('clear')

#Cewl Menu 17 - {5 ANY Characters RIGHT --> LEFT incrementally} ( could take a while dependant on size of cewl wordlist generated)
def cewl_wordlist_dic():
    #Right Side
    #print(app + attack_mode_inc_right + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + five_any_characters + cmd_defaults + increment + increment_min + increment_max)
    subprocess.call(app + attack_mode_inc_right + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + single_wordlist + five_any_characters + cmd_defaults + increment, shell=True)
    #Left Side
    subprocess.call(app + attack_mode_inc_left + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + five_any_characters + single_wordlist + cmd_defaults + increment, shell=True)
    #print(app + attack_mode_inc_left + hash_type_NetNTLMv2 + hash_path_and_name + pot_file + five_any_characters + single_wordlist + cmd_defaults + increment + increment_min + increment_max)
    os.system('clear')
    
    
#Crack Menu 0 - Try all words lists lessthan <1GB -  Common Credentials
#Updated and merged all smaller wordlists into one file for more effcient testing (find . -name "*.txt" | xargs cat >> ./mergedfile.txt)
def crack_menu_0():
    global single_wordlist
    global default_cewl_file_output
    global cewl_boolean
    global file_hash_boolean
    if cewl_boolean == True and file_hash_boolean == True:
        single_wordlist = default_cewl_file_output
    elif single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    else:
        single_wordlist = "/opt/wordlists/less-than-1GB/merged_file_uniq.txt"
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist()
    
#Crack Menu 1 - Try all words lists between 1GB - <4GB
def crack_menu_1():
    global wordlist_directory
    wordlist_directory = "/opt/wordlists/1GB-4GB/"
    pot_function()
    hashcat_command_line_menu()
    wordlist_walk()
                
#Crack Menu 2 - Try crackstation list (15GB)
def crack_menu_2():
    global single_wordlist
    single_wordlist = "/opt/wordlists/4GB+/crackstation.txt"
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist()
        
#Crack Menu 3 - To add - Auto Quick Rule Test - Best64 -> d3ad0ne -> OneRuleToRuleThemAll oscommerce --> rockyou-3000
def crack_menu_3():
    global single_wordlist
    global rule_set_file_1
    global rule_set_file_2
    global rule_set_file_3
    global rule_set_file_4
    global rule_set_file_5
    global default_cewl_file_output
    global hash_abs_path
    if single_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    rule_set_file_1 = os.path.join(rules_dir, 'best64.rule')
    rule_set_file_2 = os.path.join(rules_dir, 'd3ad0ne.rule')
    rule_set_file_3 = os.path.join(rules_dir, 'OneRuleToRuleThemAll.rule')
    rule_set_file_4 = os.path.join(rules_dir, 'oscommerce.rule')
    rule_set_file_5 = os.path.join(rules_dir, 'rockyou-30000.rule')
    pot_function()
    hashcat_command_line_menu()
    multiple_wordlist_rule_set()
    
#Crack Menu 4 - Try all words lists 4GB+ - (will take a while to cache each wordlist prior to testing)
def crack_menu_4():
    global wordlist_directory
    wordlist_directory = "/opt/wordlists/4GB+/"
    pot_function()
    hashcat_command_line_menu()
    wordlist_walk()

#Crack Menu 5 - Oxford Dic, capital letter, upto 4 characters, incrementally - RIGHT SIDE
def crack_menu_5():
    global single_wordlist
    single_wordlist = "/opt/wordlists/english-words/words.txt"
    pot_function()
    hashcat_command_line_menu()
    hc_command_menu_5()

#Crack Menu 6 - Oxford Dic, capital letter, upto 4 characters, incrementally - LEFT SIDE
def crack_menu_6():
    global single_wordlist
    single_wordlist = "/opt/wordlists/english-words/words_first_letter_upper.txt"
    pot_function()
    hashcat_command_line_menu()
    hc_command_menu_6()
                
#Crack Menu 7 - Try Oxford Dictionary Starting with UPPER Case + {upto 4 Numbers LEFT SIDE, upto 4 numbers RIGHT SIDE}
def crack_menu_7():
    global single_wordlist
    single_wordlist = "/opt/wordlists/english-words/words_first_letter_upper.txt"
    pot_function()
    hashcat_command_line_menu()
    hc_command_menu_7()

#Crack Menu 8 - Rockyou with rule - Best64
def crack_menu_8():
    global single_wordlist
    global single_hash_boolean
    global file_hash_boolean
    global rule_set_directory
    if single_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    rule_set_directory = "/opt/hashcat/rules/best64.rule"
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist_rule_set()

#Crack Menu 9 - Rockyou with rule - d3ad0ne
def crack_menu_9():
    global single_wordlist
    global single_hash_boolean
    global file_hash_boolean
    global rule_set_directory
    if single_hash_boolean == True and cewl_boolean == False:
            single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
            single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
            single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
            single_wordlist = default_cewl_file_output
    rule_set_directory = "/opt/hashcat/rules/d3ad0ne.rule"
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist_rule_set()
    
#Crack Menu 10 - Rockyou with rule - OneRuleToRuleThemAll
def crack_menu_10():
    global single_wordlist
    global single_hash_boolean
    global file_hash_boolean
    global rule_set_directory
    if single_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    rule_set_directory = "/opt/hashcat/rules/password_cracking_rules/OneRuleToRuleThemAll.rule"
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist_rule_set()

#Crack Menu 11 - Rockyou with rule - # Changed to add leet speak rules. KoreLogicRules were ineffective and took too long..
def crack_menu_11():
    global single_wordlist
    global rule_set_file_1
    global rule_set_file_2
    global rule_set_file_3
    global rule_set_file_4
    global rule_set_file_5
    global default_cewl_file_output
    global hash_abs_path
    if single_hash_boolean == True and cewl_boolean == False:
            single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
            single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
            single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
            single_wordlist = default_cewl_file_output
    rule_set_file_1 = os.path.join(rules_dir, 'leetspeak.rule')
    rule_set_file_2 = os.path.join(rules_dir, 'unix-ninja-leetspeak.rule')
    pot_function()
    hashcat_command_line_menu()
    hc_command_menu_11()

#Crack Menu 12 - Rockyou with rule - oscommerce
def crack_menu_12():
    global single_wordlist
    global single_hash_boolean
    global file_hash_boolean
    global rule_set_directory
    if single_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    rule_set_directory = "/opt/hat-hashcat-automation-tool/rules/oscommerce.rule"
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist_rule_set()

#Crack Menu 13 - Rockyou with rule - rockyou-30000
def crack_menu_13():
    global single_wordlist
    global single_hash_boolean
    global file_hash_boolean
    global rule_set_directory
    if single_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    rule_set_directory = "/opt/hat-hashcat-automation-tool/rules/rockyou-30000.rule"
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist_rule_set()

#Crack Menu 14 - Rockyou with Hob0Rules -> Quick Test {hob064.rule} -> Comprehensive Test {d3adhob0.rule}
def crack_menu_14():
    global single_wordlist
    global single_hash_boolean
    global file_hash_boolean
    global rule_set_directory
    if single_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt " # Space added for correct argument spacing
    elif single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == False:
        single_wordlist = "/opt/wordlists/rockyou.txt "
    elif file_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    rule_set_directory = "/opt/hat-hashcat-automation-tool/rules/hob0Rules/"
    pot_function()
    hashcat_command_line_menu()
    rule_set_walk()

#Cewl menu
def cewl_menu_15():
    global hash_input
    global wordlist_directory
    global cewl_boolean
    global default_cewl_file_output
    global single_hash_abs_path
    global cewl_wordlist_size
    cewl_boolean = True
    os.system('clear')
    banner()
    print(" We will now make a wordlist based on the given website address")
    cewl_url_input = input(" Specify the website for collecting the wordlist in full including protocols and ports numbers if non standard: ")
    cewl_app = "/usr/bin/cewl "
    cewl_write = "-w "
    cewl_verbose = " -v "
    default_depth = "--depth 2 "
    default_min_word_length = "--min_word_length 7 "
    if single_hash_boolean == True:
        hash_input = single_hash_abs_path + '.cewl-wordlist.txt'
    elif file_hash_boolean == True:
        hash_input = hash_input + '.cewl-wordlist.txt' 
    default_cewl_file_output = os.path.join(cewl_upload_dir, hash_input)
    print(hash_input)
    #print(cewl_app + default_depth + default_min_word_length + cewl_url_input + cewl_verbose + cewl_write + default_cewl_file_output)
    subprocess.call(cewl_app + default_depth + default_min_word_length + cewl_url_input + cewl_verbose + cewl_write + default_cewl_file_output, shell=True)
    cewl_wordlist_size = os.popen('wc -l ' + default_cewl_file_output).read()
    os.system('clear')

#Run straight Cewl Wordlist.
def cewl_menu_16():
    global single_wordlist
    global default_cewl_file_output
    global cewl_boolean
    global file_hash_boolean
    if cewl_boolean == True and file_hash_boolean == True:
        single_wordlist = default_cewl_file_output
    elif cewl_boolean == True and single_hash_boolean == True:
        single_wordlist = default_cewl_file_output
    else:
        input("Cewl Wordlist not ran yet!, run cewl first, (Option 15)")
        crack_menu()
    pot_function()
    hashcat_command_line_menu()
    singular_wordlist()

#Automated Cewl wordlist - {5 ANY Characters RIGHT --> LEFT incrementally} (could take a while dependant on size of cewl wordlist generated)
def cewl_menu_17():
    global single_wordlist
    global default_cewl_file_output
    global cewl_boolean
    global file_hash_boolean
    if single_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    elif file_hash_boolean == True and cewl_boolean == True:
        single_wordlist = default_cewl_file_output
    else:
        input("Cewl Wordlist not ran yet!, run cewl first, (Option 15)")
        crack_menu()
    pot_function()
    hashcat_command_line_menu()
    cewl_wordlist_dic()
                    
#Crack Menu (Back Crack) - go back one stage...
def back_crack():
    global cewl_boolean
    global single_hash_boolean
    global file_hash_boolean
    os.system('clear')
    cewl_boolean = False # Needed to reset for new menu settings to be applied
    single_hash_boolean = False # Needed to reset for new menu settings to be applied
    file_hash_boolean = False # Needed to reset for new menu settings to be applied
    main_menu()
                                    


#Cracking Menu
def crack_menu():
    global file_hash_boolean
    global single_hash_boolean
    global single_hash_abs_path
    global hash_abs_path
    global default_cewl_file_output
    global cewl_boolean
    global cewl_wordlist_size
    os.system('clear')
    try:
        while 1:
            if single_hash_boolean == True and not cewl_boolean == True:
                banner()
                print("")
                prPurple("--==Hashcat Single Hash Cracking Menu==--")
                print("")
                print("")
                print(" Hash file created:")
                prYellow(single_hash_abs_path)
            elif single_hash_boolean == True and cewl_boolean == True:
                banner()
                print("")
                prPurple("--==Hashcat Single Hash Cewl Cracking Menu==--")
                print("")
                print("")
                print(" Single Hash file in Use:")
                prYellow(single_hash_abs_path)
                print(" Cewl Wordlist in Use:")
                prYellow(default_cewl_file_output)
            elif file_hash_boolean == True and not cewl_boolean:
                banner() # Currently display duplicates first time round, second time round it only shows one banner.. 
                print("")
                prPurple("--==Hashcat Multi Hash Cracking Menu==--")
                print("")
                print("")
                print(" Hash file selected for cracking is: ")
                prYellow(hash_abs_path)
            elif file_hash_boolean == True and cewl_boolean == True:
                banner() # Added after the call as still in the loop for aesthtics.
                print("")
                prPurple("--==Hashcat Multi Hash Cewl Cracking Menu==--")
                print("")
                print("")
                print(" Hash file in use:")
                prYellow(hash_abs_path)
                print("")
                print(" Amount of Cewl words written + Absolute Path: ")
                prYellow(cewl_wordlist_size)
            print("")
            prLightGray("Currently Only for NetNTLMv2 Hashes AKA (NTLMv2) {NTLM / WPA / WEP to do}")
            prCyan("0) Automated Testing - Custom Common Credentials - includes rockyou, hashkiller - {Corporate Scan}")
            prLightPurple("1) Automated Testing - All words lists between 1GB - <4GB - {Comprehensive Scan}")
            prCyan("2) Automated Testing - Crackstation list (15GB) - (Runtime ~2min 5sec) - {General Scan}")
            prLightPurple("3) Auto Quick Rule Test - Best64 -> d3ad0ne -> OneRuleToRuleThemAll oscommerce --> rockyou-3000 - {Corporate Scan}")
            prCyan("4) Automated Testing - All words lists 4GB+ - (will take a while to cache each wordlist prior to testing) - {Comprehensive Scan}")
            prLightPurple("5) Automated Testing - Oxford Dictionary(>=8chars) + Starting with UPPER Case + upto 3 ANY Characters on RIGHT SIDE - {Corporate Scan}")
            prCyan("6) Automated Testing - Oxford Dictionary(>=8chars) + Starting with UPPER Case + upto 3 ANY Characters on LEFT SIDE {Corporate Scan}")
            prLightPurple("7) Automated Testing - Oxford Dictionary Starting with UPPER Case + (upto 4 Numbers LEFT SIDE, upto 4 numbers RIGHT SIDE) - {Corporate Scan}")
            prCyan("8) Rule Based - Rockyou or cewl - Best64 - (Runtime ~20sec)")
            prLightPurple("9) Rule Based - Rockyou or cewl - d3ad0ne -(Runtime ~1hr 43sec)")
            prCyan("10) Rule Based - Rockyou or cewl - OneRuleToRuleThemAll - (Runtime ~2hr 30sec)")
            prLightPurple("11) Rule Based - Rockyou or cewl - L33t speak rules (leetspeak.rule + unix-ninja-leetspeak.rule)")
            prCyan("12) Rule Based - Rockyou or cewl - oscommerce - (Runtime ~1sec)")
            prLightPurple("13) Rule Based - Rockyou or cewl - rockyou-30000 - (Runtime ~1sec)")
            prCyan("14) Rule Based - Rockyou or cewl -> Quick Test {hob064.rule} -> Comprehensive Test {d3adhob0.rule}")
            prLightPurple("15) Cewl wordlist")
            prCyan("16) Run straight Cewl wordlist (Run option 15 first to activate)")
            prLightPurple("17) Automated Cewl wordlist - {5 ANY Characters RIGHT --> LEFT incrementally} - (Could take a while dependant on size of cewl wordlist generated)")
            prRed("b) Back to Main Menu")
            crack_option = {"0": crack_menu_0,
                            "1": crack_menu_1,
                            "2": crack_menu_2,
                            "3": crack_menu_3,
                            "4": crack_menu_4,
                            "5": crack_menu_5,
                            "6": crack_menu_6,
                            "7": crack_menu_7,
                            "8": crack_menu_8,
                            "9": crack_menu_9,
                            "10": crack_menu_10,
                            "11": crack_menu_11,
                            "12": crack_menu_12,
                            "13": crack_menu_13,
                            "14": crack_menu_14,
                            "15": cewl_menu_15,
                            "16": cewl_menu_16,
                            "17": cewl_menu_17,
                            "b": back_crack
                           }
            try:
                selection = input("\n Select an Option: ")
                crack_option[selection]()
            except KeyError:
                os.system('clear')
                banner()
                pass
    except KeyboardInterrupt:
                sys.exit()
                
                  
#Single Hash Menu
def single_hash_menu():
    global single_hash_file_name
    global single_hash_boolean
    global single_hash_abs_path
    single_hash_boolean = True
    os.system('clear')
    banner()
    print("Example NetNTLMv2 Hash")
    print("NIGEL.BOYCE::MLTD:1122334455667788:1880e4d532d4825a6da1c60dfd3cefe9:01010000000000001a744106b78cd401252ceec0fdbd9d0e000000000200060053004d0042000100160053004d0042002d0054004f004f004c004b00490054000400120073006d0062002e006c006f00630061006c000300280073006500720076006500720032003000300033002e0073006d0062002e006c006f00630061006c000500120073006d0062002e006c006f00630061006c0008003000300000000000000000000000002000005387ece822900e4e5d75f8648229f71008a6e1effd5a059a3aa6b066ed75330b0a001000000000000000000000000000000000000900140048005400540050002f00790061006e006e0079000000000000000000")
    print("Password - Amber123")
    print("\n")
    print("admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030")
    print("Password - hashcat")
    print("")
    single_hash = input(" Add your hash" + '\n')
    single_hash_string = str(single_hash)
    print("")
    print(" You entered : " + '\n') + single_hash_string
    print(" OK - Need to put the hash into a File...") # Put hash into a file
    single_hash_file_name = input("Enter a logical filename: ")
    single_hash_abs_path = (os.path.join(hash_upload_dir, single_hash_file_name))
    os.chdir(hash_upload_dir)
    sh = open(single_hash_file_name, "w+")
    sh.write(single_hash_string)
    print("File Created")
    sh.close()
    crack_menu()

    
#Hash File Upload Menu
def hash_from_file():
    global hash_abs_path
    global hash_input
    global file_hash_boolean
    global hash_upload_dir
    file_hash_boolean = True
    os.system('clear')
    banner()
    print(" Add the hash file into hash_upload directory show below: ")
    prCyan(hash_upload_dir)
    print(" Below are the files currently available in the file uploads directory.. (Hit Enter to Refresh)")
    print("")
#Used for removing emacs created backup files ending with a tilde
    ignore = '~'
    for root, dirs, files in os.walk(hash_upload_dir):
        for file in files:
            if not file.endswith(ignore):
                print(os.path.join(root, file))
    print("")
    hash_input = input(" Select the filename from the above list to be uploaded: ")
    os.chdir(hash_upload_dir)
    try:
        if (os.path.isfile(hash_input)):
            print(" Hash File %s found and accepted..." % hash_input)
            hash_abs_path = (os.path.join(hash_upload_dir, hash_input))
            print(" Absolute Path of hash file is: \n") + hash_abs_path
            crack_menu()
        else:
            print(" Error: %s file not found" % hash_input)
            os.system('clear')
            hash_from_file()
    except KeyError:
        os.system('clear')
        pass
    

#Exit system
def program_exit():
    sys.exit()

#MainMenu
def main_menu():
    try:
        while 1:
            banner()
            prCyan("\t(0) Input Singluar Hash")
            prLightPurple("\t(1) Input Hash from File")
            prRed("\t(2) Exit")
            options = {"0": single_hash_menu,
                       "1": hash_from_file,
                       "2": program_exit,
                      }
            try:
                task = input("\n Choose an Option: ")
                options[task]()
            except KeyError:
                os.system('clear')
                pass
    except KeyboardInterrupt:
                sys.exit()

if __name__ == '__main__':
    main_menu()
