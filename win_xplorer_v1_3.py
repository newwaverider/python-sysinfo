# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:54:28 2019
Version 1.0

@author: Mark Carter
"""
## Imports ############################################################################################
import psutil
import time
import os
import sys
import subprocess
import platform
from os.path import exists


## Re-useable Functions ###################################################################################

# Function to clear the windows console screen
def cls():    # this os command shout also work with linux but not yet tested fully
    os.system('cls' if os.name=='nt' else 'clear')

# Function to format a number of bytes into the easier to read
# number of MB, KB, GB, TB or PB
def get_size(bytes):
    # The for loop divides the bytes by 1024 until the number left
    # is less than 1024... the unit list advances each time
    # a division by 1024 takes place so the correct abbreviation
    # can be used
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:   
        if bytes < 1024:
            return f"{bytes:.1f}{unit}B"
        bytes /= 1024

# Function to read memory information from the current system
# using the correct PSUTIL libeary command and return it for 
# use by another function
def return_mem():
    memory_info = psutil.virtual_memory()
    return memory_info

# Function to read cpu percent used from the current system
# using the correct PSUTIL libeary command and return it for 
# use by another function
def return_cpu_percent():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

# Function to track average cpu load from the current system
# using the correct PSUTIL libeary command and return it for 
# use by another function... first time called returns zero...
# Returns 1,5,15 minute averages... for obvious reasons 5 and 15
# minute averages take 5 and 15 minutes to generate
def return_load_avg():
    load_average = psutil.getloadavg()
    return load_average

# Function to accept a number of dots to write to the console
# 
def progress_indicator(dots):
    if dots%10 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()

# Function to generate a log stamp specifically for the current
# system that is unique for each log entry
def return_log_id():
    host_name = os.environ['COMPUTERNAME']
    log_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    log_stamp = 'logstamp '+host_name+' - '+log_time+' '
    return log_stamp

def get_cpu_freq():
    cpu_freq_lst = psutil.cpu_freq()
    cpu_freq = 'Current='+str(cpu_freq_lst[0])+' / Min='+str(cpu_freq_lst[1])+' / Max='+str(cpu_freq_lst[2])
    return cpu_freq

def transform_list_allstrs(old_list):
    new_list = []
    for line in old_list:
        map_iterator = map(str,line)
        line_str = list(map_iterator)
        new_list.append(line_str)
    return new_list

def get_widest_col_vals(curr_list,curr_hdr):
        widest_item = 0
        col_w=[]
        counter = 0
        while counter < len(curr_list[0]):

            for line in curr_list:
                if len(str(line[counter])) > widest_item:
                    widest_item = len(str(line[counter]))
                    
            if len(curr_hdr[counter]) > widest_item:
                widest_item = len(curr_hdr[counter])

            col_w.append(widest_item)

            counter +=1
            widest_item = 0
        return(col_w)

def put_list_in_logfile(list_name,file_name):
    log_stamp = return_log_id()
    with open(file_name, 'a') as file_handler:
        file_handler.write('\n'+'-'*70+'\n')
        file_handler.write(log_stamp+'\n')
        file_handler.write('-'*70+'\n')
        for line in list_name:
            file_handler.write(str(line)+'\n')

def display_screen_hdr(message,width,justify):
    print(' '+rev_on,end='')
    if justify == 'center':
        pf = "{:^"+str(width)+"}"
    elif justify == 'right':
        pf = "{:>"+str(width)+"}"
    else:        
        pf = "{:<"+str(width)+"}"
    print(pf.format(message))
    print(rev_off,end='') 


def enter_to_continue(width,justify):
    print(' '+rev_on,end='')
    if justify == 'center':
        pf = "{:^"+str(width)+"}"
    elif justify == 'right':
        pf = "{:>"+str(width)+"}"
    else:        
        pf = "{:<"+str(width)+"}"
    print(pf.format(' <enter> to continue ',end=''))
    print(rev_off,end='') 
    to_continue = input('')  

def view_list(col_names,col_fmt,page_length,list_name,log_file,col_w,menu_option):
    cls()
    line_counter = 1
    page_counter = 1
    counter = 1
    sort_by = 0
    i_c = 0
    pid_queried = 'N'
    
    for item in col_names:
        str_screen = rev_on+' '+str(counter)+'='+item+' '+rev_off+' '
        print(str_screen,end='')
        counter+=1

    print()
    print(rev_on+'Enter Field#+A\D:[5D] '+rev_off+'',end='')

    sort_by = input()
    
    if sort_by == '' or sort_by == ' ':
        sort_by = '1D'

    try:
        sb_num = int(sort_by[0])
        sb_num = sb_num-1
    except:
        sb_num = 1

    if sb_num <1 or sb_num > 8:
        sb_num = 1
    
    try:
        ad_order = sort_by[1]
    except:
        ad_order = 'D'

    for i in range(21):
        print(' '*80)

    cls()

    if ad_order == 'A' or ad_order =='a':
        list_name = sorted(list_name, key=lambda x: x[sb_num])
    else:
        list_name = sorted(list_name, key=lambda x: x[sb_num],reverse = True)
    
   
    for item in range(len(col_names)):  # prints column names
        item_fmt = '{:'+str(col_w[item])+'}'
        print(rev_on,end='')
        print(item_fmt.format(col_names[item]),end='')
        print(rev_off,end=' ')
    print()

    for item in range(len(col_names)):  # prints dashed line under column names
        item_fmt = '{:'+str(col_w[item])+'}'
        print(item_fmt.format('-'*col_w[item]),end=' ')
    print()

    # iterate through the list
    record_num = 0
    list_name = transform_list_allstrs(list_name) 
        
    while record_num < len(list_name): #for line in list_name:
        line=list_name[record_num]
        for item in range(len(col_names)):
            item_fmt = '{:'+str(col_w[item])+'}'
            print(item_fmt.format(line[item]),end=' ')

        record_num+=1    
        print()
        
        if line_counter == page_length or record_num == len(list_name):
            if menu_option == 'P' or menu_option == 'p':
                print(rev_on,end="")
                print('<ENTER> continue (S) to Stop (I)nfo to query item:',end='')
                print(rev_off,end="")
                to_continue = input('')
            else:
                print(rev_on,end="")
                print('<ENTER> continue (S) to Stop:',end='')
                print(rev_off,end="")
                to_continue = input('')
            
            if to_continue == 'I' or to_continue =='i':
                if menu_option == 'P' or menu_option == 'p':
                    cpid = input('Enter process ID:')
                    specific_proc_view(cpid)
                    cls()
                    pid_queried = 'Y'
                else:
                    pid_queried='Y'
            
            if to_continue == 'S' or to_continue == 's':
                put_list_in_logfile(list_name,log_file)
                print(rev_on,'Again Y/N [N]: ',rev_off,end='')
                again = input('')
                if again =='' or again == 'N' or again =='n':
                    again = 'N'
                    return again  
                else:
                    cls()
                    again = 'Y'
                    return again
 
            cls()
            
            item_num = 0
            for item in col_names: # prints column names as header
                item_fmt = '{:'+str(col_w[item_num])+'}'
                print(rev_on,end='')
                print(item_fmt.format(col_names[item_num]),end='')
                print(rev_off,end='')
                print(' ',end='')
                item_num +=1
            print()
            
            item_num = 0
            for item in col_names: # prints dashed line under column names
                item_fmt = '{:'+str(col_w[item_num])+'}'
                print(item_fmt.format('-'*col_w[item_num]),end=' ')
                item_num +=1
            print()
            
            if pid_queried=='Y':
                record_num=record_num-page_length
                pid_queried='N'
                cls()
                for item in range(len(col_names)):  # prints column names
                    item_fmt = '{:'+str(col_w[item])+'}'
                    print(rev_on,end='')
                    print(item_fmt.format(col_names[item]),end='')
                    print(rev_off,end=' ')
                print()

                for item in range(len(col_names)):  # prints dashed line under column names
                    item_fmt = '{:'+str(col_w[item])+'}'
                    print(item_fmt.format('-'*col_w[item]),end=' ')
                print()           
            
            line_counter = 0
            page_counter = page_counter + 1
        line_counter+=1
    put_list_in_logfile(list_name,log_file)
    
        

def sys_header():
    display_screen_hdr(' System Xplorer v1.3 ',76,'left')
    log_stamp = return_log_id()    # Host Name and Current Time
    print(" Hostname/Time    : ",log_stamp[9:])
    print(" Boot time        : ",time.ctime(psutil.boot_time()))  # System Boot Time
    print(" Platform         : ",platform.architecture()[0],platform.architecture()[1])  # Platform Information
    wv = sys.getwindowsversion()    # get_windows_version()
    print(" OS Version       : ",str(wv.major)+'.'+str(wv.minor),'build:',wv.build)
    print(" Proc ID          : ",platform.processor())  # Processor identification
    print(" CPU count        : ", str(psutil.cpu_count(logical=False))+' physical '+str(psutil.cpu_count())+' virtual') # CPU count physical/virtual
    cpu_freq = get_cpu_freq()    # CPU Frequency
    print(" CPU frequency    : ",cpu_freq)    # CPU Frequency
    print(" User logged in   : ", os.getlogin())    # User Logged In
    memory_info=return_mem()    # Memory Info class instance contains total,available,percent,free,used
    print(" Mem tot/avail    : ",get_size(memory_info.total),'/',get_size(memory_info.available))
    ret_val = return_net_inout_stats()    # Total Network Bytes send and received
    print(' Net Bytes        : ','sent= ',get_size(ret_val[0]),'received= ',get_size(ret_val[1]))

def find_disk_information():
    display_screen_hdr(' ',78,'center')
    disk_usage = psutil.disk_usage('/')

    print(" Disk Usage : ",'Tot=',get_size(disk_usage[0]),\
    'Used=',get_size(disk_usage[1]),'Free=',get_size(disk_usage[2]),\
    '%Used=',str(disk_usage[3])+'%')

    disk_io = psutil.disk_io_counters(perdisk=True)
    for key,val in disk_io.items():
        if key[0:13]=='PhysicalDrive':
            pt2 = key[13:]
            key = 'PhysDrv'+pt2
        print(' '+key+'   :  ',end='')
        print('R/W Cnt=',str(val[0])+'/'+str(val[1]),\
        'Bytes=',get_size(val[2])+'/'+get_size(val[3]),\
        'Time=',str(val[4])+'/'+str(val[5]))

    disk_parts = psutil.disk_partitions()
    num_disk_parts = len(disk_parts)
    print(" #Partitions: ",num_disk_parts)

    for parts in disk_parts:
        device = parts[0]
        mount = parts[1]
        file_sys = parts[2]
        type_disk = parts[3]
        print(' '*14,end='')
        if len(device) == 0:
            device='NA'
        if len(mount) == 0:
            mount='NA'
        if len(file_sys) == 0:
            file_sys='NA'
        if len(type_disk) == 0:
            type_disk='NA'
        print(' Dev= '+device,' MP= '+mount,' FS= '+file_sys,' Type= '+type_disk)

    print()
    enter_to_continue(76,'left')

def return_net_inout_stats():
    net_np = psutil.net_io_counters() # uses PSUTIL to get bytes sent and bytes received
    net_bytes_sent = get_size(net_np.bytes_sent)  # returns net_np.,bytes_sent,bytes_recv
    net_bytes_recv = get_size(net_np.bytes_recv)  # packes_sent,packets_recv,errin,errout
    return net_np.bytes_sent, net_np.bytes_recv   # dropin,dropout

## Functions specific to this program ###########################################################################
def initialize_psutil():
    sys.stdout.write('Initializing')
    sys.stdout.flush()
    dots = 0
    for proc in psutil.process_iter():
        dots+=1
        progress_indicator(dots)
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'status','create_time','io_counters','memory_info'])

        except (psutil.NoSuchProcess,psutil.ZombieProcess,psutil.AccessDenied,psutil.TimeoutExpired) as error:
           pass
    cls()
    num_procs = dots
    return num_procs

def run_query(cmd_to_run):
    try:
       cp = subprocess.run(cmd_to_run, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        pass
    if cp.returncode==0:
        output_list = cp.stdout.splitlines()
    else:
        print("error when executing - "+cmd_to_run+" - "+str(cp.stderr))
    return output_list
    
def verify_mgmt_service(fn_for_output,cmd_to_run,line_to_test,word_to_match):
    try:
        cp = subprocess.run(cmd_to_run, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        pass
    if cp.returncode ==0:
        output_list = cp.stdout.splitlines()
        work_state = output_list[line_to_test].strip()
        x = len(word_to_match) 
        if work_state[:x] == word_to_match:
            work_state = "working"
            print(fn_for_output+" - "+work_state)
        else:
            work_state = "not working"
            print(fn_for_output+" - "+work_state)
        
        with open(fn_for_output, 'w') as filehandle:
            for line in output_list:
                filehandle.write(line+'\n')
    else:
        print("error when executing - "+cmd_to_run+" - "+str(cp.stderr))
    return work_state    
    
def find_win_drivers():    
    driverquery_state = verify_mgmt_service('driverquery.tst',"driverquery /V",1,"Module Name")    
    if driverquery_state == "working":
        driver_list = run_query("driverquery /V")
        driver_lol=[]
        for driver in driver_list:
            one_driver = []
            one_driver = [driver[0:12],driver[13:35],driver[73:82],driver[84:93],driver[95:105],\
            driver[195:242]]
            driver_lol.append(one_driver)
    driver_lol_srt = sorted(driver_lol, key = lambda x: x[3])
    driver_lol_srt_str = transform_list_allstrs(driver_lol_srt)
    del driver_lol_srt_str[0:2]
    return driver_lol_srt_str

def find_win_services(): 
    win_services = list(psutil.win_service_iter())
    services = []
    for num in range(len(win_services)):
        one_service = []
        service_all_inf = psutil.win_service_get(win_services[num].name())
        service_dict = service_all_inf.as_dict()
        one_service = [service_dict['pid'],service_dict['name'][:30],service_dict['status'],service_dict['description'][:50]]
        services.append(one_service)
    services_srt = sorted(services, key = lambda x: x[2])
    #services_srt_str = transform_list_allstrs(services_srt)
    return services_srt
      
def find_net_connections():
    conns = []
    for conn in psutil.net_connections():
        fd = conn[1]
        conn_type = conn[2]
        laddr = conn[3]
        raddr = conn[4]
        status = conn[5]
        cpid = conn[6]
        proc = psutil.Process(cpid)
        proc_name = proc.name()

        if len(laddr)>0:
            laddr_address = laddr[0]
            laddr_port = laddr[1]
        else:
            laddr_address = 'NA'
            laddr_port = 'NA'

        if len(raddr) > 0:
            raddr_address = raddr[0]
            raddr_port = raddr[1]
        else:
            raddr_address = 'NA'
            raddr_port = 'NA'

        one_conn = [laddr_address,laddr_port,raddr_address,raddr_port,status,cpid,proc_name]
        conns.append(one_conn)

    conns_srt = sorted(conns, key = lambda x: x[5])
    return conns_srt
    
def find_processes():
    processes = []
    
    for proc in psutil.process_iter():
        counter = 0
        one_process = []
        try:
            pinfo = proc.as_dict(attrs=['name','status','connections','exe','num_threads','cpu_percent','pid','memory_info'])
            pid = pinfo['pid']
            name = pinfo['name']
            status = pinfo["status"]
            memory_info = pinfo["memory_info"]
            peak_wset  = memory_info[4]
            peak_wset = peak_wset
            wset = memory_info[5]
            wset = wset
            nthreads = pinfo['num_threads']
            connections = pinfo['connections']
            num_connections = len(connections)
            cpu_percent = pinfo['cpu_percent']

        except (psutil.NoSuchProcess,psutil.ZombieProcess,\
                psutil.AccessDenied,psutil.TimeoutExpired) as error:
           pass

        else:
            one_process = [pid,name,status,peak_wset,wset,nthreads,num_connections,cpu_percent]
            processes.append(one_process)
        
    processes_srt = sorted(processes, key = lambda x: x[5])
    return processes_srt


def find_process_exe_cmd():
    processes = []
    
    for proc in psutil.process_iter():
        counter = 0
        one_process = []
        try:
            pinfo = proc.as_dict(attrs=['exe','cmdline'])
            exe = pinfo['exe']
            cmd = pinfo['cmdline']
            

        except (psutil.NoSuchProcess,psutil.ZombieProcess,\
                psutil.AccessDenied,psutil.TimeoutExpired) as error:
           pass

        else:
            one_process = [exe,cmd]
            processes.append(one_process)
        
    #processes_srt = sorted(processes, key = lambda x: x[5])
    return processes   


def specific_proc_view(pid):
    # invoke psutil process module for a single process id
    p = psutil.Process(int(pid))

    # use the psutil as_dict method to get the information we need on the one process
    # assign value as 'NA' if there is a permissions or other retrieval issue
    one_process = p.as_dict(attrs=['pid', 'name', 'username','exe','create_time','status','num_threads',\
    'num_ctx_switches','connections','num_handles','memory_info','memory_percent',\
    'memory_maps','username','ppid','io_counters','nice','ionice','cpu_times',\
    'cpu_percent','cpu_affinity','cmdline'],ad_value='NA')

    # since the as_dict method will not handle parent, parents and children we
    # use the below code to get that information
    try:
        r_open_files = p.open_files()
    except:
        r_open_files = 'NA'
    try:
        r_children = p.children()
    except:
        r_children = 'NA'
    try:
        r_parent = p.parent()
    except:
        r_parent = 'NA'
    try:
        r_parents = p.parents()
    except:
        r_parents = 'NA'
    try:
        r_cmdline = p.cmdline()
    except:
        r_cmdline = 'NA'
    try:
        r_exe = p.exe()
    except:
        r_exe = 'NA'
    
    # now we format the information obtained for display purposes
    # show voluntary / involuntary context switches
    r_num_ctx_switches = str(one_process['num_ctx_switches'][0])+'/'+str(one_process['num_ctx_switches'][1])
    # show memory working set / peak working set / and % memory used
    r_memory_info = get_size(one_process['memory_info'].wset)+'/'+ get_size(one_process['memory_info'].peak_wset)+'/'+\
    str(one_process['memory_percent'])[0:4]+' '
    # show length of memory maps but do not display maps
    r_len_mem_maps = len(one_process['memory_maps'])
    # show number of open files by using the length of the open files list
    if r_open_files != 'NA':
        r_open_files = str(len(r_open_files))
    else:
        r_open_files = 'NA'
    # show parent process id / name / status / create_time
    if r_parent == None:
        r_ppid = 'NA'
    else:
        r_ppid = str(r_parent.pid)+'/'+r_parent.name()+'/'+r_parent.status()+'/'+str(time.ctime(r_parent.create_time()))

    # show io counts read / write / other
    r_io_count = str(one_process['io_counters'].read_count)+'/'+str(one_process['io_counters'].write_count)+'/'+str(one_process['io_counters'].other_count)+' '
    # show io bytes read / write / other
    r_io_bytes = str(get_size(one_process['io_counters'].read_bytes))+'/'+str(get_size(one_process['io_counters'].write_bytes))+'/'+str(get_size(one_process['io_counters'].other_bytes))+' '
    # get number of connections from connections list
    r_num_connections = len(one_process['connections'])
    # show num of parents and children by measuring the length of the lists
    if r_parents != 'NA':
        r_num_parents = len(r_parents)
    if r_children != 'NA':
        r_num_children = len(r_children)
    
    
    # now set up the labels to be used in a list
    pid_display = \
    [[' PID ',pid],\
    [' Name ',one_process['name']],\
    [' Started ',time.ctime(one_process['create_time'])],\
    [' Status ',one_process['status']],\
    [' #Threads ',one_process['num_threads']],\
    [' CTX Switches VOL\INV ',r_num_ctx_switches,one_process['connections']],\
    [' #Connections ',r_num_connections],\
    [' #Handles ',one_process['num_handles']],\
    [' Memory -> Wset/Pwset/%Used ',r_memory_info],\
    [' Length of Mem_Maps ',r_len_mem_maps],\
    [' Username ',one_process['username']],\
    [' #Parents ',r_num_parents],\
    [' #Children ',r_num_children],\
    [' #Open Files ',r_open_files],\
    [' PPID ',r_ppid],\
    [' IO Count R/W/O ',r_io_count],\
    [' IO Bytes R/W/O ',r_io_bytes],\
    [' NICE ',one_process['nice']],\
    [' IONICE ',one_process['ionice']],\
    [' CMDLINE ', r_cmdline],\
    [' EXE ', r_exe]]    
    #[' CPU Affinity ',one_process['cpu_affinity']]]

    cls()
    counter = 0
    for line in pid_display:
        label = line[0]
        label_val = line[1]
        pad=28-len(label)
        str_screen = ' '*pad+rev_on+label+':'+rev_off+str(label_val)
        print(str_screen)
        counter +=1

    to_continue = input('         <ENTER> to continue: ')


def entry_screen():
    menu_items = ['(P)rocesses ','(N)et Conns ','(D)isk ','(C)puMemNet ',' D(r)ivers  ',
              '(W)in Svces ','(Q)uit ']

    sys_header()
    print(' '+'-'*76)
    print(' ',end='')
    for num in range(len(menu_items)):
        # for item in menu_items:
        str_screen = rev_on+str(menu_items[num])+rev_off+' '
        if num ==5:
            str_screen = str_screen+'\n'+' '
        print(str_screen,end='')

    str_screen = rev_on+'Select P/N/D/L/Q:'+rev_off
    answer = input('')

    return answer

def launch_cpu_mem_net():
    subprocess.Popen(["python","win_perf_watch.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

def launch_win_drivers():
    col_w = [12,22,10,10,10,48]
    drq_hdr = ['Module Name','Display Name','Start Mode','State ','Status','Path']
    col_fmt = "{:<"+str(col_w[0])+"} {:<"+str(col_w[1])+"} {:<"+str(col_w[2])+"} {:<"+str(col_w[3])+\
    "} {:<"+str(col_w[4])+"} {:<"+str(col_w[5])+"}"
    driver_lol_srt_str = find_win_drivers()  
    again = view_list(drq_hdr,col_fmt,20,driver_lol_srt_str,'drivery_query.txt',col_w,answer)         
    if again == 'Y':
        launch_win_drivers()
        
def launch_win_services():
    services_srt = find_win_services()
    service_hdr = ['PID','Name','Status','Description']
    col_w = get_widest_col_vals(services_srt,service_hdr) 
    col_fmt = "{:<"+str(col_w[0])+"} {:<"+str(col_w[1])+"} {:<"+str(col_w[2])+"} {:<"+str(col_w[3])+"}"
    again = view_list(service_hdr,col_fmt,20,services_srt,'services_query.txt',col_w,answer)
    if again == 'Y':
        launch_win_services()

def launch_net_conns():
    conns_srt = find_net_connections()
    conn_hdr = ['Local IP','Local Port','Remote IP','Remote Port','Status','PID','Name']
    col_w = get_widest_col_vals(conns_srt,conn_hdr)
    col_fmt = "{:<"+str(col_w[0])+"} {:<"+str(col_w[1])+"} {:<"+str(col_w[2])+"} {:<"+str(col_w[3])\
    +"} {:<"+str(col_w[4])+"} {:<"+str(col_w[5])+"} {:<"+str(col_w[6])+"}"
    again = view_list(conn_hdr,col_fmt,20,conns_srt,'net_conn_history.txt',col_w,answer)
    if again == 'Y':
        launch_net_conns()

def launch_win_processes():
    processes_srt = find_processes()
    processes_hdr = ['PID','Name','Stat','Peak','Wset','threads','NumConn','CpuPct']
    col_w = get_widest_col_vals(processes_srt,processes_hdr)
    col_fmt = "{:<"+str(col_w[0])+"} {:<"+str(col_w[1])+"} {:<"+str(col_w[2])+"} {:<"+str(col_w[3])\
    +"} {:<"+str(col_w[4])+"} {:<"+str(col_w[5])+"} {:<"+str(col_w[6])+"}"
    again = view_list(processes_hdr,col_fmt,20,processes_srt,'processes_history.txt',col_w,answer)
    if again == 'Y':
        launch_win_processes()
        
#================================================================================================================
## Main Menu Routine ###########################################################################################
#================================================================================================================
os.system('mode con: cols=130 lines=25')
rev_on = '\033[7m'
rev_off = '\033[0m'

num_procs = initialize_psutil()
running = "Y"

while running == "Y":
    cls()
    answer = entry_screen()
    if answer == "P" or answer =="p":
        launch_win_processes()

    elif answer == "N" or answer == "n":
        launch_net_conns()
    
    elif answer == "W" or answer == "w":
        launch_win_services()

    elif answer == 'R' or answer == 'r':
        launch_win_drivers()
    
    elif answer =="D" or answer == "d":
        cls()
        find_disk_information()
        cls()

    elif answer =="C" or answer == "c":
        cls()
        launch_cpu_mem_net()
        cls()

    elif answer =="Q" or answer == "q":
        exit()

   