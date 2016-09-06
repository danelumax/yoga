import re, time, random, os
import log, common
from scp import Scp
from sshutil import SshUtil
from cfg import cfgInstance
from hautil import hautilInstance
from sshmanager import sshManagerInstance


class ConfigDnsTask(object):
    '''
    Config DNS Server
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass

        
    def precheck(self):
        #TODO: check the ISO file exist 
        #TODO: check the mount point exist and free to use
        pass
    
    def execute(self):
        log._file.debug(">> Config DNS Server Begin")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._configDNSSingle()
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._configDNSEntry1()
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._configDNSEntry2()
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :
            self._configDNSMedium1()
        else :
            log._file.debug("No need to config dns server")
        log._file.debug("<< Config DNS Server End")
    

    def verify(self):
        log._file.debug(">> Check DNS Server Status Begin")
        common.save_healthcheck_info("DNS Server Status", 'normal', 'normal', "OK")
        log._file.debug("<< Check DNS Server Status End")
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass


    def _prepare(self, cfg) :
        log._file.debug(">>> Prepare DNS Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=prepareDns' \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _create(self, cfg, host_list, ss_vip) :
        log._file.debug(">>> Create DNS Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        for hostname, oam_ip in host_list :
            command = 'python configdns.py --command=createDns --hostname=' + hostname \
                      + " --oam_ip=" + oam_ip \
                      + " --ipwss_vip=" + ss_vip \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _delete(self, cfg, host_list, ss_vip) :
        log._file.debug(">>> Delete DNS Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, r_code = ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        for hostname, oam_ip in host_list :
            command = 'python configdns.py --command=deleteDns --hostname=' + hostname \
                      + " --ipwss_vip=" + ss_vip \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _startSm(self, cfg) :
        log._file.debug(">>> Start DNS Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=start_dnssm' \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopSm(self, cfg) :
        log._file.debug(">>> Stop Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=stop_dnssm' \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _startDns(self, cfg, host_list, ss_vip) :
        log._file.debug(">>> Start DNS Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        for hostname, oam_ip in host_list :
            command = 'python configdns.py --command=startDns --hostname=' + hostname \
                      + " --ipwss_vip=" + ss_vip \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopDns(self, cfg, ss_vip) :
        log._file.debug(">>> Stop DNS Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, r_code = ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=stopDns --ipwss_vip=' + ss_vip \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        res, r_code = ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _configMasterZone(self, cfg, hostname, ss_vip) :
        log._file.debug(">>> Create Master Zone on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=configMasterZone --hostname=' + hostname + ' --ipwss_vip=' + ss_vip \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _cleanMasterZone(self, cfg, ss_vip) :
        log._file.debug(">>> Clean Master Zone on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, r_code = ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=cleanMasterZone --ipwss_vip=' + ss_vip \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        res, r_code = ssh_util.remote_exec(command, wait=10)
        log._file.debug("<<<")


    def _verifyDns(self, cfg) :
        log._file.debug(">>> Verify DNS Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=verifyDns' \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _configServerManager(self, cfg, ss_vip):
        log._file.debug(">>> Config Server Manager on "+ cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, r_code = ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=confDnsSM --ipwss_vip=' + ss_vip  \
                      + ' --username=' + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        res, r_code = ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _checkAlarm(self, cfg):
        log._file.debug(">>> Check DNS Alarm on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        command = common.getAlarmCmd('ipworksDns')
        res,code = ssh_util.remote_exec(command, p_err=False, throw=False)
        alarm = common.parseAlarmInfo(res)
        if alarm :
            item = "Alarm %s On %s" %('ipworksDns', cfg.getHostName())
            common.save_healthcheck_info(item, alarm, "", "--")
        log._file.debug("<<<")



##################################################################################

    def _configDNSSingle(self):
        log._file.debug(">>> Config DNS in Single Mode Begin")
        ps1 = cfgInstance().getPsCfg(0)
        self._prepare(ps1)  # on ps
        self._verifyDnsServer(ps1, ps1, ps1.getInternalIp())
        log._file.debug("<<< Config DNS in Single Mode End")
 

    def _configDNSEntry1(self):
        log._file.debug(">>> Config DNS in Entry1 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
        self._prepare(ps1)
        self._prepare(ps2)
        self._verifyDnsServer(ss1, ps1, ss1.getInternalIp())
        log._file.debug("<<< Config DNS in Entry1 Mode End")


    def _configDNSEntry2(self):
        log._file.debug(">>> Config DNS in Entry2 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        self._prepare(ps1)
        self._prepare(ss1)
        self._verifyDnsServer(ss1, ps1, ss1.getInternalIp())
        log._file.debug("<<< Config DNS in Entry2 Mode End")


    def _configDNSMedium1(self):
        log._file.debug(">>> Config DNS in Medium1 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
        self._prepare(ps1)
        self._prepare(ps2)
        self._verifyDnsServer(ss1, ps1, cfg.getHaCfg().getSsVip())
        log._file.debug("<<< Config DNS in Medium1 Mode End")
        
       
    def _verifyDnsServer(self, ss_cfg, ps_cfg, ss_vip) :
        log._file.debug(">>> Verify DNS Server Begin")
        host_list = []
        host_list.append(["dns1", ps_cfg.getOamIp()])
        try :
            # config env
            self._create(ss_cfg, host_list, ss_vip)  # on ss
            self._startSm(ps_cfg)  # on ps
            self._configMasterZone(ss_cfg, host_list[0][0], ss_vip)  # on ss 
            self._startDns(ss_cfg, host_list, ss_vip)  # on ss
            self._verifyDns(ps_cfg)  # on ps
            # check alarm on ps
            self._checkAlarm(ps_cfg)
        except Exception, e :
            log._file.error("Exception in _verifyDnsServer : " + str(e))
            raise
        finally :
            # clean env
            self._cleanMasterZone(ss_cfg, ss_vip)  # on ss
            self._stopDns(ss_cfg, ss_vip)  # on ss
            self._stopSm(ps_cfg)  # on ps
            self._delete(ss_cfg, host_list, ss_vip)  # on ss
        log._file.debug("<<< Verify DNS Server End")










