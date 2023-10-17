from ats import tcl
from ats import aetest
from ats.log.utils import banner

from unicon.eal.dialogs import Dialog
from unicon.eal.dialogs import Statement

import time
import logging
import os
import sys
import re
import pdb
import json
import pprint
import socket
import struct
import inspect
import yaml
import random
import ipaddress

from yaml import loader
from pyats.aetest.steps import Steps

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

global uut1           
global port
class ForkedPdb(pdb.Pdb):
    '''A Pdb subclass that may be used
    from a forked multiprocessing child1
    '''
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin
class common_setup(aetest.CommonSetup):
    @aetest.subsection
    def connecting_to_device(self,testscript,testbed,R1):
        global file
        global uut1
        uut1=testbed.devices[R1]
        log.info("Connecting to Device...")
        log.info("%s"%uut1.name)
        try:
            uut1.connect()
        except Exception as e:
            log.info("Connection to %s Unsuccessful "\
                    "Exiting error:%s"%(uut1.name,e))
            self.failed(goto=['exit'])
class permutation_for_vpc(aetest.Testcase):
    @aetest.test
    def cli(self,testbed,testscript):
        global command , run_conf , error , a , b
        command = []
        run_conf = []
        error = []
        a = 0
        b = 0
        c = 1
        d = 0
        cli = """source 10.105.100.156 precedence 7 hold-timeout 6
source 10.105.100.156 precedence 7 interval 499 timeout 19
source 10.105.100.156 precedence 7 udp-port 1113
source 10.105.100.156 precedence 7 vrf default
source 10.105.100.156 hold-timeout 6 precedence 7
source 10.105.100.156 hold-timeout 6 interval 499 timeout 19
source 10.105.100.156 hold-timeout 6 udp-port 1113
source 10.105.100.156 hold-timeout 6 vrf default
source 10.105.100.156 interval 499 timeout 19 precedence 7
source 10.105.100.156 interval 499 timeout 19 hold-timeout 6
source 10.105.100.156 interval 499 timeout 19 udp-port 1113
source 10.105.100.156 interval 499 timeout 19 vrf default
source 10.105.100.156 udp-port 1113 precedence 7
source 10.105.100.156 udp-port 1113 hold-timeout 6
source 10.105.100.156 udp-port 1121 interval 498 timeout 18
source 10.105.100.156 udp-port 1113 vrf default
source 10.105.100.156 vrf default precedence 7
source 10.105.100.156 vrf default hold-timeout 6
source 10.105.100.156 vrf default interval 499 timeout 19
source 10.105.100.156 vrf default udp-port 1113
precedence 7 source 10.105.100.156 hold-timeout 6
precedence 7 source 10.105.100.156 interval 499 timeout 19
precedence 7 source 10.105.100.156 udp-port 1113
precedence 7 source 10.105.100.156 vrf default
precedence 7 hold-timeout 6 source 10.105.100.156
precedence 7 hold-timeout 6 interval 499 timeout 19
precedence 7 hold-timeout 6 udp-port 1113
precedence 7 hold-timeout 6 vrf default
precedence 7 interval 499 timeout 19 source 10.105.100.156
precedence 7 interval 499 timeout 19 hold-timeout 6
precedence 7 interval 499 timeout 19 udp-port 1113
precedence 7 interval 499 timeout 19 vrf default
precedence 7 udp-port 1113 source 10.105.100.156
precedence 7 udp-port 1113 hold-timeout 6
precedence 7 udp-port 1113 interval 499 timeout 19
precedence 7 udp-port 1113 vrf default
precedence 7 vrf default source 10.105.100.156
precedence 7 vrf default hold-timeout 6
precedence 7 vrf default interval 499 timeout 19
precedence 7 vrf default udp-port 11131
hold-timeout 6 source 10.105.100.156 precedence 7
hold-timeout 6 source 10.105.100.156 interval 499 timeout 19
hold-timeout 6 source 10.105.100.156 udp-port 1113
hold-timeout 6 source 10.105.100.156 vrf default
hold-timeout 6 precedence 7 source 10.105.100.156
hold-timeout 6 precedence 7 interval 499 timeout 19
hold-timeout 6 precedence 7 udp-port 1113
hold-timeout 6 precedence 7 vrf default
hold-timeout 6 interval 499 timeout 19 source 10.105.100.156
hold-timeout 6 interval 499 timeout 19 precedence 7
hold-timeout 6 interval 499 timeout 19 udp-port 1113
hold-timeout 6 interval 499 timeout 19 vrf default
hold-timeout 6 udp-port 1113 source 10.105.100.156
hold-timeout 6 udp-port 1113 precedence 7
hold-timeout 6 udp-port 1113 interval 499 timeout 19
hold-timeout 6 udp-port 1113 vrf default
hold-timeout 6 vrf default source 10.105.100.156
hold-timeout 6 vrf default precedence 7
hold-timeout 6 vrf default interval 499 timeout 19
hold-timeout 6 vrf default udp-port 1113
interval 499 timeout 19 source 10.105.100.156 precedence 7
interval 499 timeout 19 source 10.105.100.156 hold-timeout 6
interval 499 timeout 19 source 10.105.100.156 udp-port 1113
interval 499 timeout 19 source 10.105.100.156 vrf default
interval 499 timeout 19 precedence 7 source 10.105.100.156interval 499 timeout 19 precedence 7 hold-timeout 6
interval 499 timeout 19 precedence 7 udp-port 1113
interval 499 timeout 19 precedence 7 vrf default
interval 499 timeout 19 hold-timeout 6 source 10.105.100.156
interval 499 timeout 19 hold-timeout 6 precedence 7
interval 499 timeout 19 hold-timeout 9 udp-port 1113
interval 499 timeout 19 hold-timeout 6 vrf default
interval 499 timeout 19 udp-port 1113 source 10.105.100.156
interval 499 timeout 19 udp-port 1113 precedence 7
interval 499 timeout 19 udp-port 1113 hold-timeout 6
interval 499 timeout 19 udp-port 1113 vrf default
interval 499 timeout 19 vrf default source 10.105.100.156
interval 499 timeout 19 vrf default precedence 7
interval 499 timeout 19 vrf default hold-timeout 6
interval 499 timeout 19 vrf default udp-port 1113
udp-port 1113 source 10.105.100.156 precedence 7
udp-port 1113 source 10.105.100.156 hold-timeout 6
udp-port 1113 source 10.105.100.156 interval 499 timeout 19
udp-port 1113 source 10.105.100.156 vrf default
udp-port 1113 precedence 7 source 10.105.100.156
udp-port 1113 precedence 7 hold-timeout 6
udp-port 1113 precedence 7 interval 499 timeout 19
udp-port 1113 precedence 7 vrf default
udp-port 1113 hold-timeout 6 source 10.105.100.156
udp-port 1113 hold-timeout 6 precedence 7
udp-port 1113 hold-timeout 6 interval 499 timeout 19
udp-port 1113 hold-timeout 6 vrf default
udp-port 1113 interval 499 timeout 19 source 10.105.100.156
udp-port 1113 interval 499 timeout 19 precedence 7
udp-port 1113 interval 499 timeout 19 hold-timeout 6
udp-port 1113 interval 499 timeout 19 vrf default
udp-port 1113 vrf default source 10.105.100.156
udp-port 1113 vrf default precedence 7
udp-port 1113 vrf default hold-timeout 6
udp-port 1113 vrf default interval 499 timeout 19
vrf default source 10.105.100.156 precedence 7
vrf default source 10.105.100.156 hold-timeout 6
vrf default source 10.105.100.156 interval 499 timeout 19
vrf default source 10.105.100.156 udp-port 1113
vrf default precedence 7 source 10.105.100.156
vrf default precedence 7 hold-timeout 6
vrf default precedence 7 interval 499 timeout 19
vrf default precedence 7 udp-port 1113
vrf default hold-timeout 6 source 10.105.100.156
vrf default hold-timeout 6 precedence 7
vrf default hold-timeout 6 interval 499 timeout 19
vrf default hold-timeout 6 udp-port 1113
vrf default interval 499 timeout 19 source 10.105.100.156
vrf default interval 499 timeout 19 precedence 7
vrf default interval 499 timeout 19 hold-timeout 6
vrf default interval 499 timeout 19 udp-port 1113
vrf default udp-port 1113 source 10.105.100.156
vrf default udp-port 1113 precedence 7
vrf default udp-port 1113 hold-timeout 6
vrf default udp-port 1113 interval 499 timeout 19
"""
        command = cli.split('\n')
        output_lines = cli.strip().split('\n')
        command = [line.strip() for line in output_lines]  
        log.info("Confiuring Peer-Keepalive VPC")
        for i in command:
            uut1.configure("no feature vpc\nfeature vpc")
            uut1.configure(f"vpc domain 10\npeer-keepalive destination 10.105.100.155 {i}")
            output = uut1.execute("show run vpc | in alive")
            if output:
                log.info(f"Running Config of {i} :-\n{output}")
                run_conf.append(output)
            else:    
                error.append(i)
        if len(error) != 0:
            log.error("Error commands :-\n") 
            for j in error:
                log.info(f"{j}")
                d = d + 1
        if d != 0:
            self.failed(goto=['exit'])
        while a < len(command) and b < len(run_conf):
            log.info(f"( {c} ) COMMAND :- peer-keepalive destination 10.105.100.155 {command[a]} \n RUNNING_CONFIG :- {run_conf[b]}\n\n")
            a = a + 1
            b = b + 1
            c = c + 1
class common_cleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnecting_from_device(self,testscript,testbed,R1):
        uut1.disconnect()
        log.info(banner("Successfully disconnecting from the device.")) 

        
    
            
