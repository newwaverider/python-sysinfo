# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:54:28 2019
Version 1.0

@author: Mark Carter
"""
import keyboard
import time
import os
import sys
import psutil
import subprocess

#---------------------------------------------------------------------------------------------------
# Reusable Functions ###############################################################################
#---------------------------------------------------------------------------------------------------

### cls() invokes cls to clear the console screen if running windows
###
def cls():
###
    if os.name=='nt':
        subprocess.call(["cmd", "/c", "cls"]) 

### format_size(bytes) receives a number of bytes and returns it as a 
### formatted string with the correct byte abbreviation
def format_size(bytes):
###
    # for each unit in the list ['', 'K', 'M', 'G', 'T', 'P'] check to see if bytes
    # is less than 1024 
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            # return formatted string using current value of units
            return f"{bytes:.1f}{unit}B"
        # divide bytes by 1024 and continue until it is less than 1024
        # bytes/=1024 is equivalent to bytes=bytes/1024
        bytes /= 1024

### use the PSutil library to get our memory in use
def percent_mem_inuse(): 
###   
    # get the virtual memory values
    current_mem = psutil.virtual_memory()
    # extract the value we want
    percent_mem = current_mem.percent
    return percent_mem

### use the PSutil library to get our bytes sent and received since the
### program started
def bytes_sent_receive():
###  
    # use psutil to retrieve the network io counters
    net_np = psutil.net_io_counters()
    # extract current bytes sent
    current_sent = net_np.bytes_sent
    # extract current bytes received
    current_recv = net_np.bytes_recv
    # return the current sent/received 
    return(current_sent, current_recv) # return the current sent/received

### use the PSutil library to get our cpu percent in use
def return_cpu():  
###
    cpu_usg_current = psutil.cpu_percent()
    return cpu_usg_current # return
    
#--------------------------------------------------------------------------------------------------
#    Main Program #################################################################################
#--------------------------------------------------------------------------------------------------

# set windows console mode to a smaller window size
if os.name=='nt':
    subprocess.call(["cmd", "/c", "mode con: cols=13 lines=15"])

# Setting up the windows console text attributes for reverse on and reverse off
rev_on = '\033[7m'
rev_off = '\033[0m'

# retrieve current host time
host_name = os.environ['COMPUTERNAME']

# retrieve current host time
host_time = time.strftime("%a %D %H:%M:%S", time.localtime())

# get the initial values for bytes sent and received
initial_sent, initial_recv = bytes_sent_receive()#get initial values for bytes sent/received

# psutil.getloadavg() returns an initial list of zeros under Windows so we get that 
# out of the way now
load_avg = psutil.getloadavg()

# Starting the loop which waits for a keyboard press
while True:
    current_mem = percent_mem_inuse() # get current % memory used
    current_cpu = psutil.cpu_percent() # get current % cpu used
    current_sent, current_recv = bytes_sent_receive() # get current bytes sent/received
    
    total_sent = current_sent - initial_sent # subtract initial sent values from current sent
    total_recv = current_recv - initial_recv # subtract initial recv values from current received
    total_sent = format_size(total_sent) # format for bytes,kb,mb,gb
    total_recv = format_size(total_recv) # format for bytes,kb,mb,gb    
    
    # calc average cpu load for multiple cpus
    load_avg = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]

    time.sleep(5) # wait 5 seconds

    # build header list and align with the display variables
    perf_list =     [
        [' %mem used ',current_mem],
        [' %cpu_used ',current_cpu],
        [' bytes snt ',total_sent],
        [' bytes rcv ',total_recv],
        [' 1m  load  ', round(load_avg[0],2)],
        [' 5m  load  ', round(load_avg[1],2)],
        [' 15m load  ', round(load_avg[2],2)]
        ]
        
    #clear windows console
    cls()
    
    # Build text to send to console
    screen_string=''
    for info in perf_list:
        screen_string = screen_string+' '+rev_on+info[0]+rev_off+'\n'
        screen_string = screen_string+' '+str(info[1]).center(11)+'\n'
    
    # Send text to console
    print(screen_string,end='')
    
    #write information to the log file
    log_entry='Host Name'+','+host_name+','+'Host Time'+','+host_time+','
    for info in perf_list:
        log_entry=log_entry+info[0]+','+str(info[1])+','
    log_entry=log_entry+'\n'
    with open("perf_history.txt", 'a') as file_handler: # send log entery to logfile
        file_handler.write(log_entry)
    
    # check for escape key press to end program... hold escape key down until next cycle
    if keyboard.is_pressed('esc'): #this is where the imported keyboard module is used
       break
