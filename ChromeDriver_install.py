#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 11:32:47 2021

@author: mouchen
"""
import os, platform, sys, threading, time, subprocess 

_OS = platform.system()

SUPPORT_OS = ["Linux", "Windows"]

dest_path = "./"

SUDO_EN = False

if _OS == "Linux":
    CMD_GOOGLE_CHROME_CHECK = "google-chrome --version | awk '{print $NF}'"
    CMD_GOOGLE_CHROME_INSTALL_1 = "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
    CMD_GOOGLE_CHROME_INSTALL_2 = "sudo apt install ./google-chrome-stable_current_amd64.deb"
    CMD_GOOGLE_DRIVER_INSTALL = "wget -P "+dest_path+" https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip"
elif _OS == "Windows":
    CMD_GOOGLE_CHROME_CHECK = 'dir /B/AD "C:\Program Files (x86)\Google\Chrome\Application\"|findstr /R /C:"^[0-9].*\..*[0-9]$" '
    CMD_GOOGLE_CHROME_INSTALL = ""
    CMD_GOOGLE_DRIVER_INSTALL = ""

global flag, TERMINATE_FLAG
WDT_LIMIT = 180

def Thread_Watchdog():
    global flag, WDT_LIMIT, TERMINATE_FLAG
    
    print("[WDT] Activate Watchdog timer thread...")
    while(1):
        if TERMINATE_FLAG:
            break
        
        if flag == 1:
            print("\n[WDT] Start timer...")
            START_TIME = time.time()
            while(1):
                CUR_TIME = time.time()
                
                if TERMINATE_FLAG:
                    break
                
                if not CUR_TIME % 10:
                    print("[WDT] Current time: ", round(CUR_TIME, 2))
                    
                if (CUR_TIME - START_TIME) > WDT_LIMIT:
                    print("\n[WDT] Time out!")
                    print("\n[ERROR] Watchdog timeout... ")
                    if _OS == "Linux":
                        os._exit(1)
                    elif _OS == "Windows":
                        sys._exit(1)
                
                if flag == 2:
                    DUR_TIME = CUR_TIME - START_TIME
                    print("\n[WDT] Stop timer with time cost ", round(DUR_TIME,2), " s")
                    flag = 0
                    break
    
    
flag = 0   
TERMINATE_FLAG = 0    

t = threading.Thread(target = Thread_Watchdog, args = ())
t.start()

print("[INFO] STEP1. Check whether local OS supported by script.")
for i in range(len(SUPPORT_OS)):
    if SUPPORT_OS[i] == _OS:
        print("--> "+_OS+" support!")
        break
    if i == len(SUPPORT_OS)-1:
        print("[ERROR] None support OS ", _OS)
        sys.exit(0)

# Install Google-Chrome
print("[INFO] STEP2. Check whether Google Chrome existed.")

GC_ver = subprocess.check_output(CMD_GOOGLE_CHROME_CHECK, shell=True).decode("utf-8")
if "command not found" in GC_ver:
    print("--> Need to install google-chrome!")
    
    flag = 1
    cmd_res = os.system(CMD_GOOGLE_CHROME_INSTALL_1)
    if not cmd_res:
        print("[INFO] Command Pass!")
        flag = 2
    else:
        print("[ERROR] Command abnormal!")
        sys.exit(1)
    flag = 1
    cmd_res = os.system(CMD_GOOGLE_CHROME_INSTALL_2)
    if not cmd_res:
        print("[INFO] Command Pass!")
        flag = 2
    else:
        print("[ERROR] Command abnormal!")
        sys.exit(1)
        
else:
    print("--> Google chrome existed, go install google chrome driver!")
    

print("[INFO] STEP3. Install Chrome Driver.")
flag = 1
cmd_res = os.system(CMD_GOOGLE_DRIVER_INSTALL)
if not cmd_res:
    print("[INFO] Command Pass!")
    flag = 2
else:
    print("[ERROR] Command abnormal!")
    sys.exit(1)


TERMINATE_FLAG = 1

t.join()
print("[INFO] Task complete, Please check google-chrome and chrome-driver existence!!")
sys.exit(0)
