import os
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from scp import Scp


class CheckEMCTask(object):
    '''
    CheckEMC  
    '''


    def __init__(self):
        pass
        
        
    def precheck(self):
        pass
    
    
    def execute(self):
        log._file.debug(">>CheckEMC  Begin")

        cfg = cfgInstance()
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode):
            emc_ip = cfgInstance().getHaCfg().getNfsIp()
            for ss_cfg in cfg.getSsCfgList():
                self._check_emc_connection(ss_cfg,emc_ip)
        elif not cmp(common.C_IPW_MODE_MEDIUM2,common.g_ipw_mode):
            emc_ip = cfgInstance().getHaCfg().getNfsIp()
            for ss_cfg in cfg.getSsCfgList():
                self._check_emc_connection(ss_cfg,emc_ip)
            for ps_cfg in cfg.getPsCfgList():
                self._check_emc_connection(ps_cfg,emc_ip)

        log._file.debug("<<CheckEMC  End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass

    def _check_emc_connection(self,cfg,emc_ip):
        log._file.debug(">>>Check connection with emc,emc ip = " + emc_ip+" on host "+cfg.getHostName()+" Begin")
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = "python checkemc.py --emc_ip="+(emc_ip)
        ssh_util.remote_exec(command)
        log._file.debug("<<<Check connection with emc End")


