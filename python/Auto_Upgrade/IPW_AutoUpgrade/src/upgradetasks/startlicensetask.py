import os,re,subprocess 
import log, common
import time
import utils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class StartLicenseTask(object) :
    """
    Start License Server 
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartLicenseTask Begin")
        self.startLicenseServer(cfg)
        log._file.debug("<< StartLicenseTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def startLicenseServer(self, host):
        log._file.debug(">>> Begin to start License Server on host " + host.getHostName())
        cmd = "/etc/init.d/ipworks.slm start"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        if not utils.check_process(ssh, "lserv_sn", "start"):
            log._file.error("Start License Server Failed")
            raise Exception("Start License Server Failed")
        log._file.debug("Start License Server Succeed!")

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to start License Server manually:")
        helpinfo='''
        # /etc/init.d/ipworks.slm start
        '''
        log._print.info(helpinfo)
        pass
