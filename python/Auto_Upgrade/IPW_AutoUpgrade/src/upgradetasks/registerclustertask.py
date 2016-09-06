import os,re,subprocess
import log, common
import utils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

from hautil import hautilInstance

class RegisterClusterTask(object) :
    """
    Register Cluster
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> RegisterClusterTask Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            ss1 = cfgInstance().getSsCfg(0)
            ss2 = cfgInstance().getSsCfg(1)
            self._stopInnodb(cfg)
            self._registerHaResource(cfg, ss1, ss2)
        log._file.debug("<< RegisterClusterTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to register SS resource group manually:")
        helpinfo='''
        1. Stop Innodb.
        # /etc/init.d/ipworks.mysql stop

        2. Register SS resource group.
           If the disk array is AX4-5:
           # /opt/ipworks/IPWhaagents/scripts/register_cluster.pl --diskarray --makelink-only

           If the disk array is VNXe3200:
           # /opt/ipworks/IPWhaagents/scripts/register_cluster.pl --nfs --makelink-only
        '''
        log._print.info(helpinfo)
        pass

    def _stopInnodb(self, host):
        log._file.debug(">>> Begin to stop Innodb on host " + host.getHostName())
        cmd = "/etc/init.d/ipworks.mysql stop"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        if not utils.check_process(ssh, "innodbnode", "stop"):
            log._file.error("Stop Innodb Failed")
            raise Exception("Stop Innodb Failed")
        log._file.debug("Stop Innodb Succeed!")

    def _registerHaResource(self, host, ss1_cfg, ss2_cfg) :
        log._file.debug(">>> Register SS resource group on " + host.getHostName())    
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        if not cmp(ss1_cfg.getPassword(), ss2_cfg.getPassword()):
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'echo "Y" | /opt/ipworks/IPWhaagents/scripts/register_cluster.pl --all-password ' + ss1_cfg.getPassword() + ' --diskarray' + ' --makelink-only'
            else:
                command = 'echo "Y" | /opt/ipworks/IPWhaagents/scripts/register_cluster.pl --all-password ' + ss1_cfg.getPassword() + ' --nfs' + ' --makelink-only'
        else :
            passwd = '%s,%s' %(ss1_cfg.getPassword(), ss2_cfg.getPassword())
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'python register_cluster.py --command=ss --password=%s --mode=diskarray --option=--makelink-only' %(passwd)
            else:
                command = 'python register_cluster.py --command=ss --password=%s --mode=nfs --option=--makelink-only' %(passwd)
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec(command)
        log._file.debug("<<<")    

