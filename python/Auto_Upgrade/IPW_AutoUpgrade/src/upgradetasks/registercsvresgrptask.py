import os,re,subprocess 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

from hautil import hautilInstance

class RegisterCsvResGrpTask(object) :
    """
    Register CSV Engine 
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> RegisterCsvResGrpTask Begin")

        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA \
          and cfgInstance().getHaCfg().useCsvGrp() :
            ss1 = cfgInstance().getSsCfg(0)
            ss2 = cfgInstance().getSsCfg(1)
            mgm_vip = cfgInstance().getHaCfg().getMgmVip()
            self._registerHaCsvengine(cfg, ss1, ss2, mgm_vip)

        log._file.debug("<< RegisterCsvResGrpTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to register CSV Engine resource group manually:")
        helpinfo='''
        If the disk array is AX4-5:
        # /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --diskarray --ndb-mgm-vip <dbcluster_vip>

        If the disk array is VNXe3200:
        # /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --nfs --ndb-mgm-vip <dbcluster_vip>
        '''
        log._print.info(helpinfo)
        pass

    def _registerHaCsvengine(self, host, ss1_cfg, ss2_cfg, mgm_vip):
        log._file.debug(">> Register CSV engine resource on " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        if not cmp(ss1_cfg.getPassword(), ss2_cfg.getPassword()) :
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --diskarray --ndb-mgm-vip " + mgm_vip + " --all-password=" + ss1_cfg.getPassword()
            else:
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --nfs --ndb-mgm-vip " + mgm_vip + " --all-password=" + ss1_cfg.getPassword()
        else :
            passwd = '%s,%s' %(ss1_cfg.getPassword(), ss2_cfg.getPassword())
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'python register_cluster.py --command=csvengine --password=%s --mgm_vip=%s --mode=diskarray' %(passwd, mgm_vip)
            else:
                command = 'python register_cluster.py --command=csvengine --password=%s --mgm_vip=%s --mode=nfs' %(passwd, mgm_vip)
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec(command)
        log._file.debug("<<")

