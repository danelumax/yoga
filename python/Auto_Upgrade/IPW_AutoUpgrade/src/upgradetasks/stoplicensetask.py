import os,re,subprocess 
import log, common
import time
import utils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class StopLicenseTask(object) :
    """
    Stop License Server
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopLicenseTask Begin")
        self.stopLicenseServer(cfg)
        log._file.debug("<< StopLicenseTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def stopLicenseServer(self, host):
        log._file.debug(">>> Begin to stop License Server on host " + host.getHostName())
        cmd = "/etc/init.d/ipworks.slm stop"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        if not utils.check_process(ssh, "lserv_sn", "stop"):
            log._file.error("Stop License Server Failed")
            raise Exception("Stop License Server Failed")
        log._file.debug("Stop License Server Succeed!")

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to stop License Server manually:")
        helpinfo='''
        # /etc/init.d/ipworks.slm stop
        '''
        log._print.info(helpinfo)
        pass

