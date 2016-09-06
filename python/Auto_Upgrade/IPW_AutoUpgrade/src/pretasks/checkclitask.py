import os
import log, common
import subprocess
import re
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from hautil import hautilInstance


class CheckCliTask(object):
    '''
    Check server name in CLI
    '''

    def __init__(self):
        '''
        self.app_command_dict = {common.C_IPW_APP_AAA : "list aaaserver ",
                                 common.C_IPW_APP_DNS : "list dnsserver ",
                                 common.C_IPW_APP_ENUM : "list enumserver ",
                                 common.C_IPW_APP_DHCP : "list dhcpserver "}
        '''

    def precheck(self):
        pass

    def execute(self):
        log._file.debug(">> CheckCliTask")
        cfg = cfgInstance();

        if not cmp(common.C_IPW_MODE_SINGLE,common.g_ipw_mode):
            ps1 = cfg.getPsCfg(0)
            servername = ps1.getPsName()
            oamip = ps1.getOamIp()
            self._CheckEachPs(ps1,servername,oamip)
        elif not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode):
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            ps2 = cfg.getPsCfg(1)

            servername = ps1.getPsName()
            oamip = ps1.getOamIp()
            self._CheckEachPs(ss1,servername,oamip)

            servername = ps2.getPsName()
            oamip = ps2.getOamIp()
            self._CheckEachPs(ss1,servername,oamip)

        elif not cmp(common.C_IPW_MODE_ENTRY2,common.g_ipw_mode):
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)

            servername = ss1.getPsName()
            oamip = ss1.getOamIp()
            self._CheckEachPs(ss1,servername,oamip)

            servername = ps1.getPsName()
            oamip = ps1.getOamIp()
            self._CheckEachPs(ss1,servername,oamip)

        elif not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) or \
            not cmp(common.C_IPW_MODE_MEDIUM2,common.g_ipw_mode):
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            ps2 = cfg.getPsCfg(1)
            ss_ip = cfg.getHaCfg().getSsVip()

            servername = ps1.getPsName()
            oamip = ps1.getOamIp()
            self._CheckEachPs(ss1,servername,oamip,ss_ip)

            servername = ps2.getPsName()
            oamip = ps2.getOamIp()
            self._CheckEachPs(ss1,servername,oamip,ss_ip)

        log._file.debug("<< CheckIpwEnvTask")

    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass


    def help(self):
        log._print.info("1 If Configured 'ps_name' (for example 'dns1') in network.json, Check if the ps name and it's oam ip is exactly equal with the result in CLI")
        log._print.info("2 If 'ps_name'(for example dns1) exists in CLI,but not configured in network.json,Please configure it rightly in network.json")
        common.cleanCliInfo()

    def _CheckEachPs(self,ss,servername,oam_ip,ss_ip=''):
        log._file.debug(">>> _CheckEachPs")
        for key in servername:
            log._file.debug("key = "+key)
            index = key.find("server")
            servertype = key[0:index]
            log._file.debug("servertype ="+servertype)
            if servertype.upper() in common.g_upgrade_service:
                if (servername[key] == ""):
                    flag = "YES"
                    command = "list " + key
                else:
                    flag = 'NO'
                    command = "list " + key + " "+ servername[key]
                self._CheckServerName(ss,command,oam_ip,flag,ss_ip)
        log._file.debug("<<<")

    def _CheckServerName(self, ss, clicommand, oamip, flag, ss_ip=''):
        log._file.debug(">>> _CheckServerName")

        ssh = sshManagerInstance().getSsh(ss.getHostName())
        ssh_util = SshUtil(ssh)

        cfg = cfgInstance();
        username = cfg.getCliUserName()
        password = cfg.getCliPassword()

        if(ss_ip == ''):
            ss_ip = ss.getOamIp()

        remote_command = 'python checkipwcliserver.py --ipwss_ip='+ss_ip+ ' --user='+username+ ' --password='+password+ ' --oamip='+oamip+ ' --flag='+flag +' --command='+'"'+clicommand+'"'
        log._file.debug("remote_command ="+ssh_util.obfuscate_passwd(remote_command))
        
        ssh_util.remote_exec("cd "+ cfg.getUpgradePath())
        res,r_code = ssh_util.remote_exec(remote_command,True,False,False)
        if(r_code == 2):
            raise Exception("Fail to check ps name in cli, command = "+ssh_util.obfuscate_passwd(remote_command))
        if(r_code == 1):
            psname = (clicommand.split(" "))[-1]
            raise Exception("PS "+ psname + " exists in cli but not configured, please configured it correctly!")
        log._file.debug("<<<")

