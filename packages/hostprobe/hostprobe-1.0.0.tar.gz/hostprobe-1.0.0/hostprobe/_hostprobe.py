import ipaddress
import socket
import time
import errno
import platform
import threading
import os
import psutil
from queue import Queue
from colorama import init as _init
from ._constants import DEFAULTTHRESHOLD, MINTHRESHOLD
from .exceptions import InvalidIp, ThresholdError
from .utils import mebibyte

opsys = platform.system()
process = psutil.Process(os.getpid())
reachedthreshold = False

#CRCSV: connection refused: cross system version
if opsys == "Windows":
    CRCSV = errno.WSAECONNREFUSED
    _init()
elif opsys == "Darwin" or opsys == "Linux":
    CRCSV = errno.ECONNREFUSED
else:
    raise Exception(f"platform \"{opsys}\" is not supported by nettest")

def check_host(host, port=80, timeout=1, result_queue:Queue=None) -> bool | int:
    """check host to see if its online! \n
    (good for threading: built in result queue!)"""
    try:
        socket.create_connection((host, port), timeout)
        if result_queue:
            result_queue.put((host, True))
        else:
            print(f"{host} is online")
    except Exception as e:
        if e.args[0] == "timed out":
            if result_queue:
                result_queue.put((host, 2))
            else:
                print(f"{host} is offline")
        elif e.args[0] == errno.EHOSTUNREACH:
            if result_queue:
                result_queue.put((host, 2))
            else:
                print(f"{host} is offline")
        elif e.args[0] == CRCSV:
            if result_queue:
                result_queue.put((host, True))
            else:
                print(f"{host} is online")
        else:
            raise Exception(f"An error has occured while checking {host}. If this is an accident, please create an issue on my github page: https://github.com/malachi196/hostprobe/issues/new/choose")
    except KeyboardInterrupt:
        result_queue.put((host, 0))

def _finalinfo(online):
    print("\n\n","\r"+"-"*20)
    print(f"Online Found: {online}")
    print("-"*20)

memory_usage = 0
def _monitor_threshold():
    global memory_usage
    while True:
        memory_usage = process.memory_info().rss
        time.sleep(1)

def netprobe(network: str, timeout:int = 5, verbose: bool = False, retry: bool = False, port:int=80, maxthreads:int=0, info:bool=False,
            r:bool=True, output:bool=False, threshold:bool=True, maxthreshold:int=DEFAULTTHRESHOLD) -> list | None:
    """
    netprobe: cross-platform python network scanner
    -----------------------------------------------------------------
    scans network for online devices (alternate version of nmap for python)\n
    ### parameters
    network: the gateway ip address for scanning (don't set the subnet, or host bits)\n
    verbose: way to much extra info \n
    retry: retry all offline results \n
    port: the port used \n
    maxthreads: specifies the maximum number of threads (0 or less for no max) \n
    info: shows percent complete and the ram usage (only for no verbose) \n
    r: return output list \n
    output: print an output list \n
    threshold: specify if you want to stop thread production at a certain memory limit until more space is freed \n
    maxthreshold: the maximum memory usage if threshold constraining is active"""
    try:
        net4 = ipaddress.ip_network(network, strict=False)
    except ValueError:
        raise InvalidIp(f"'{network}' does not appear to be a valid IPv4 or IPv6 host address. If the ip address appears correct, try changing the IP to your router's IP, or the gateway IP, or remove the subnet if you gave one")
    netsize = 0
    for _ in net4.hosts():
        netsize+=1
    i = 0
    retrystate = False
    online = []
    sigint = False
    threads = []
    result_queue = Queue()
    if threshold:
        if maxthreshold <= MINTHRESHOLD:
            raise ThresholdError(f"the maxthreshold of {maxthreshold} is lower than the program minimum threshold of {MINTHRESHOLD}")
        threshmon = threading.Thread(target=_monitor_threshold, daemon=True)
        threshmon.start()
    try:
        for x in net4.hosts():
            i+=0.5
            if info and not verbose and output:
                percentdone = (i / netsize) * 100
                if percentdone != 100:
                    print(f"\r{percentdone:.2f}%; ram usage: {(memory_usage / mebibyte(1)):.2f}MB" + ' ' * 20, end="", flush=True)
                else:
                    print(f"\r{percentdone:.2f}%; ram usage: {0}MB" + ' ' * 20, end="", flush=True)
            if threshold:
                while memory_usage >= maxthreshold:
                    time.sleep(0.1)
            if maxthreads > 0:
                while threading.active_count() > maxthreads:
                    time.sleep(0.1)
            if sigint:
                if output:
                    _finalinfo(online)
                break
            if sigint:
                break
            if not retrystate:
                if verbose:
                    print(f"checking host {str(x)}... ", flush=True)
            elif retrystate and retry:
                if verbose:
                    print(f"(retry). rechecking host {str(x)}... ", end="", flush=True)
            try:
                thread = threading.Thread(target = check_host, kwargs={"host":str(x),"timeout":timeout, "result_queue":result_queue, "port":port})
                threads.append(thread)
                thread.start() #checking host
            except KeyboardInterrupt:
                sigint = True
                break
            time.sleep(0.01)
        for thread in threads:
            thread.join()
            i+=0.5
            if info and not verbose and output:
                percentdone = (i / netsize) * 100
                if percentdone != 100:
                    print(f"\r{percentdone:.2f}%; ram usage: {(memory_usage / mebibyte(1)):.2f}MB" + ' ' * 20, end="", flush=True)
                else:
                    print(f"\r{percentdone:.2f}%; ram usage: {0}MB" + ' ' * 20, end="", flush=True)
        while not result_queue.empty():
            host, status = result_queue.get()
            if status == True:
                if verbose:
                    print(f"{host} is online", flush=True)
                online.append(host)
            elif status == 2:
                if retry:
                    if not retrystate:
                        if verbose:
                            print("request timed out")
                        retrystate = True
                        continue
                    else:
                        if verbose:
                            print(f"{host} is offline")
                        retrystate = False
                else:
                    if verbose:
                        print(f"{host} is offline")
            elif status == 0:
                sigint = True
                break
            else:
                if verbose:
                    print(f"{host} is offline")
        if output:
            _finalinfo(online)
        if r: return online
    except KeyboardInterrupt:
        if output:
            _finalinfo(online)
        if r: return online
