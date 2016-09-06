import os
import log, common
import subprocess
import re
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class CheckIPWVersionTask(object):
    '''
    Check IPWorks Version
    '''

    def __init__(self):
        '''
        The following defined the allowed upgrade path. If you're NOT RD, please don't change it.

        The valid upgrade paths:
        +---------------------------+---------------------------+
        |       base version        |      target version       |
        +---------------------------+---------------------------+
        | '15.b (AVA_901_16_5_R1C)' | '15.b (AVA_901_16_5_R2B)' |
        +---------------------------+---------------------------+
        '''

        self._base_version = None
        self._base_version_list = ['15.b (AVA_901_16_5_R1C)', '15.b (AVA_901_16_5_R2A04)','15.b (AVA_901_16_5_R2A05)']
        self._target_version    =  '15.b (AVA_901_16_5_R2B)'

        pass

    def precheck(self):
        pass

    def execute(self):
        log._file.debug(">> Check IPW Version  Begin")
        cfg = cfgInstance();
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :  # single
            ps1 = cfg.getPsCfg(0)
            self._checkInstalledIpworksVersion(ps1)
        elif not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            for ss_cfg in cfg.getSsCfgList():
                self._checkInstalledIpworksVersion(ss_cfg)
            for ps_cfg in cfg.getPsCfgList():
                self._checkInstalledIpworksVersion(ps_cfg)
        elif not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode) :  # entry1
            ss1 = cfg.getSsCfg(0)
            self._checkInstalledIpworksVersion(ss1)
            for ps_cfg in cfg.getPsCfgList():
                self._checkInstalledIpworksVersion(ps_cfg)
        elif not cmp(common.C_IPW_MODE_ENTRY2,common.g_ipw_mode) :  # entry2
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            self._checkInstalledIpworksVersion(ss1)
            self._checkInstalledIpworksVersion(ps1)
        log._file.debug("<< Check IPW Version End")
        pass

    def verify(self):
        pass

    def updateProgress(self):
        pass

    def _checkInstalledIpworksVersion(self,cfg):
        log._file.debug(">> checkInstalledIpworksVersion ")
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
        command = "python checkipwversion.py --base_versions=\"%s\"" % self._base_version_list
        res, rcode = ssh_util.remote_exec(command)
        if rcode != 0:
            log._file.error("Check base version failed!" + res)
            raise Exception("Check base version failed!")

        if not self._base_version:
            self._base_version = res
            common.saveUpgradePath(self._base_version, self._target_version)
        else:
            if self._base_version != res:
                log._file.error("The version '%s' on current server is NOT the same as others' version '%s'" % (res, self._base_version))
                raise Exception("The version '%s' on current server is NOT the same as others' version '%s'" % (res, self._base_version))
        log._file.debug("The base version is '%s'" %self._base_version)

        log._file.debug(">> checkInstalledIpworksVersion End")

    def help(self):
        log._print.info("Use the command '/opt/ipworks/IPWcommon/scripts/ipwversion' to check if the ipworks version are supported to upgrade.")
        log._print.info("The supported upgrade paths are as following:")
        log._print.info("+---------------------------+---------------------------+")
        log._print.info("|       base version        |      target version       |")
        log._print.info("+---------------------------+---------------------------+")
        for base_version in self._base_version_list:
            log._print.info("| '%s' | '%s' |" %(base_version, self._target_version))
            log._print.info("+---------------------------+---------------------------+")
        pass

