import os,re,subprocess
import log, common
import utils
import ipwutils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class UpgradeCLFResGroupTask(object) :
    """
    Register CLF Resource Group
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> UpgradeCLFResGroupTask Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium2
            ipwutils.mountShareDir(cfg)
            self._registerHaResource(cfg)
            ipwutils.unmountShareDir(cfg)
        log._file.debug("<< RegisterClusterTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to upgrade clf resource group manually:")
        helpinfo='''
        # /opt/ipworks/IPWhaagents/scripts/agent_clf/ipw_reg_clfcluster --upgrade
        '''
        log._print.info(helpinfo)
        pass

    def _registerHaResource(self, host) :
        log._file.debug(">>> Register CLF resource group on " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
	command = "/opt/ipworks/IPWhaagents/scripts/agent_clf/ipw_reg_clfcluster --upgrade"
        ssh_util.remote_exec(command)
        log._file.debug("<<<")    

