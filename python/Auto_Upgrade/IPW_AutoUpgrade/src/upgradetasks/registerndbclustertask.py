import os,re,subprocess
import log, common
import utils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

from hautil import hautilInstance

class RegisterNDBClusterTask(object) :
    """
    Register NDB Cluster
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> RegisterNDBClusterTask Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) :
            self._register_ha_resource(cfg)
        log._file.debug("<< RegisterNDBClusterTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to register NDB resource group manually:")
        helpinfo='''
        If the disk array is AX4-5:
        # opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --diskarray --makelink-only

        If the disk array is VNXe3200:
        # /opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --nfs --makelink-only
        '''
        log._print.info(helpinfo)
        pass

    def _register_ha_resource(self, cfg) :
        log._file.debug(">>> Register NDB cluster resource on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        if not cmp(ss1.getPassword(), ss2.getPassword()) \
          and not cmp(ss1.getPassword(), ps1.getPassword()) \
          and not cmp(ss1.getPassword(), ps2.getPassword()) :
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --diskarray --makelink-only --changeCib --all-password=" + cfg.getPassword()
            else:
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --nfs --makelink-only --changeCib --all-password=" + cfg.getPassword()
        else :
            passwd = '%s,%s,%s,%s' %(ss1.getPassword(), ss2.getPassword(), ps1.getPassword(), ps2.getPassword())
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'python register_cluster.py --command=ndbcluster --password=%s --mode=diskarray --option="--makelink-only --changeCib"' %(passwd)
            else:
                command = 'python register_cluster.py --command=ndbcluster --password=%s --mode=nfs --option="--makelink-only --changeCib"' %(passwd)
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec(command)
        log._file.debug("<<<")

