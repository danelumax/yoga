import os,re,subprocess 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class DeactivateHpAsrdTask(object) :
    """
    Deactivate HP Asrd
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> DeactivateHpAsrdTask Begin")
        self._disableHPAsrd(cfg)
        log._file.debug("<< DeactivateHpAsrdTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        pass

    def _disableHPAsrd(self, host):
        log._file.debug(">>> Begin to disable HP Asrd on host " + host.getHostName())
        cmd = "chkconfig hp-asrd off; service hp-asrd stop"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        log._file.debug("Disable HP Asrd Succeed!")

