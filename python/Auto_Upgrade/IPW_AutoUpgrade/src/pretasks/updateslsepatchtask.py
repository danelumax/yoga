import re 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class UpdateSlesPatchTask(object) :
    """
    Update SLES Patch
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self):
        log._file.debug(">> UpdateSlesPatchTask Begin")
        updateCmds = cfgInstance().getUpdateCmds()
        
        if len(updateCmds)!= 0 :
            cfg_list = common.getNodeList(cfgInstance())
            
            for host in cfg_list:
                self._upgradeSlesPatch(host)
        log._file.debug("<< UpdateSlesPatchTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        pass

    def _upgradeSlesPatch(self, host):
        log._file.debug(">>> Begin to update sles patch on host " + host.getHostName())

        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
        
        for updateRpmCMD in cfgInstance().getUpdateCmds() :
            log._file.debug("exec update cmd: " + updateRpmCMD)
            ssh_util.remote_exec(updateRpmCMD, p_err=False, throw=False)
            # confirm HA patch is loaded
            rpmname = updateRpmCMD[len("rpm -U "):len(updateRpmCMD)-len(".rpm")]
            res,code = ssh_util.remote_exec("rpm -q "+ rpmname)
            if (not re.search(rpmname, res)) and (not re.search(rpmname[0:(len(rpmname)-len(".x86_64"))], res)):
                log._file.error("update patch %s failed !!!", rpmname)
                raise Exception("Failed to load SLES Patch")
            else:
                log._file.debug("Upgrade sles patch %s Succeed!", rpmname)
            
        log._file.debug("Upgrade openSSL Succeed!")

