import psutil
import os
import sys
import time
import platform

def return_mem():
    mi = psutil.virtual_memory()
    memory_info = format_size(mi.total)+'/'+format_size(mi.available)
    return memory_info

def return_cpu_freq():
    cpu_freq_lst = psutil.cpu_freq()
    cpu_freq = 'Current='+str(cpu_freq_lst[0])+' / Min='+str(cpu_freq_lst[1])+' / Max='+str(cpu_freq_lst[2])
    return cpu_freq

def format_size(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:     #Returns size of bytes in a nice format
        if bytes < 1024:
            return f"{bytes:.1f}{unit}B"
        bytes /= 1024

def return_net_bytes():
    net_np = psutil.net_io_counters() # uses PSUTIL to get bytes sent and bytes received
    net_bytes_sent = format_size(net_np.bytes_sent)  # returns net_np.,bytes_sent,bytes_recv
    net_bytes_recv = format_size(net_np.bytes_recv)  # packes_sent,packets_recv,errin,errout
    net_bytes = 'sent= '+net_bytes_sent+' '+'received= '+net_bytes_recv
    return net_bytes

def return_host_name():
    host_name = os.environ['COMPUTERNAME']
    return host_name

def return_current_time():
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    return current_time  

def return_plat_arch():
    plat_arch = platform.architecture()[0]+' '+platform.architecture()[1]
    return plat_arch

def return_win_ver():
    wv = sys.getwindowsversion() 
    win_ver = str(wv.major)+'.'+str(wv.minor)+' '+'build:'+str(wv.build)
    return win_ver
    
def return_cpu_count():
    cpu_count = str(psutil.cpu_count(logical=False))+' physical '
    cpu_count=cpu_count+str(psutil.cpu_count())+' virtual'
    return cpu_count
    
def sys_info():
    print(" Host Name        : ",return_host_name())
    print(" Current time     : ",return_current_time())
    print(" Boot time        : ",time.ctime(psutil.boot_time()))
    print(" Platform         : ",return_plat_arch())
    print(" OS Version       : ",return_win_ver())
    print(" Proc ID          : ",platform.processor())
    print(" CPU count        : ",return_cpu_count())
    print(" CPU frequency    : ",return_cpu_freq())
    print(" User logged in   : ",os.getlogin())
    print(" Mem tot/avail    : ",return_mem())
    print(' Net Bytes        : ',return_net_bytes())
    

sys_info()
    
