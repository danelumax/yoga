import re, time, random, os
import log, common
from scp import Scp
from sshutil import SshUtil
from cfg import cfgInstance
from hautil import hautilInstance
from sshmanager import sshManagerInstance
import errutil


class ConfigEnumTask(object):
    '''
    Config ENUM Server
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
        log._file.debug(">> Config Enum Server Start")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._configEnumSingle()           
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._configEnumEntry1()
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._configEnumEntry2()
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :
            self._configEnumMedium1()
        else :
            log._file.debug("No need to Config enum server")
        log._file.debug("<< Config Enum Server End")
    

    def verify(self):
        log._file.debug(">> Check Enum Server Status Begin")
        common.save_healthcheck_info("Enum & DNS Server Status", 'normal', 'normal', "OK")
        log._file.debug("<< Check Enum Server Status End")
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def _prepare(self, cfg) :
        log._file.debug(">>> Prepare DNS & Enum Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=prepareDns --username=%s --password=%s ' %(common.g_cli_username, common.g_cli_password )
        ssh_util.remote_exec(command)
        command = 'python configdns.py --command=prepareEnum --oam_ip=%s --username=%s --password=%s ' %(cfg.getInternalIp(),common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _create(self, cfg, host_list, ss_vip) :
        log._file.debug(">>> Create DNS & Enum Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        for hostname, oam_ip, server_id in host_list :
            command = 'python configdns.py --command=createDnsEnum --hostname=' + hostname \
                      + " --oam_ip=" + oam_ip + " --server_id=" + str(server_id) \
                      + " --ipwss_vip=" + ss_vip \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _delete(self, cfg, host_list, ss_vip) :
        log._file.debug(">>> Delete DNS & Enum Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        for hostname, oam_ip, server_id in host_list :
            command = 'python configdns.py --command=deleteDnsEnum --hostname=' + hostname \
                      + " --server_id=" + str(server_id) \
                      + " --ipwss_vip=" + ss_vip \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _startSm(self, cfg) :
        log._file.debug(">>> Start Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=start_dnssm --username=%s --password=%s' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        command = 'python configsm.py --command=start_enumsm --username=%s --password=%s' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopSm(self, cfg) :
        log._file.debug(">>> Stop Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=stop_dnssm' + " --password=" + common.g_cli_password \
                      + " --username=" + common.g_cli_username 
        ssh_util.remote_exec(command)
        command = 'python configsm.py --command=stop_enumsm' + " --password=" + common.g_cli_password \
                      + " --username=" + common.g_cli_username 
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _startDnsEnum(self, cfg, host_list, ss_vip) :
        log._file.debug(">>> Start DNS & Enum Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        for hostname, oam_ip, server_id in host_list :
            command = 'python configdns.py --command=startDnsEnum --hostname=' + hostname \
                      + " --server_id=" + str(server_id) + " --ipwss_vip=" + ss_vip \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopDnsEnum(self, cfg, ss_vip) :
        log._file.debug(">>> Stop DNS & Enum Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=stopDnsEnum --ipwss_vip=' + ss_vip \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")



    def _configMasterZone(self, cfg, hostname, ss_vip) :
        log._file.debug(">>> Create Master Zone on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=configMasterZone --hostname=' + hostname + ' --ipwss_vip=' + ss_vip  \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _cleanMasterZone(self, cfg, ss_vip) :
        log._file.debug(">>> Clean Master Zone on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=cleanMasterZone --ipwss_vip=' + ss_vip  \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command, wait=10)
        log._file.debug("<<<")


    def _configEnumZone(self, cfg, ss_vip) :
        log._file.debug(">>> Create Enum Zone on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=configEnumZone --ipwss_vip=' + ss_vip  \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command, wait=5)
        log._file.debug("<<<")


    def _cleanEnumZone(self, cfg, ss_vip):
        log._file.debug(">>> Clean Enum Zone on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=cleanEnumZone --ipwss_vip=' + ss_vip  \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command, wait=3)
        log._file.debug("<<<")


    def _verifyDnsEnum(self, cfg) :
        log._file.debug(">>> Verify DNS & ENUM Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=verifyDnsEnum' \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _configServerManager(self, cfg, ss_vip):
        log._file.debug(">>> Config Server Manager on "+ cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, r_code = ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdns.py --command=confEnumSM --ipwss_vip=' + ss_vip  \
                      + " --username=" + common.g_cli_username \
                      + " --password=" + common.g_cli_password
        res, r_code = ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _checkAlarm(self, cfg):
        log._file.debug(">>> Check ENUM Alarm on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        for x in ['ipworksDns', 'ipworksEnum'] :
            command = common.getAlarmCmd(x)
            res,code = ssh_util.remote_exec(command, p_err=False, throw=False)
            alarm = common.parseAlarmInfo(res)
            if alarm :
                item = "Alarm %s On %s" %(x, cfg.getHostName())
                common.save_healthcheck_info(item, alarm, "", "--")
        log._file.debug("<<<")

##############################################################################

    def _configEnumSingle(self):
        log._file.debug(">>> Config Enum in Single Mode Begin")
        cfg = cfgInstance()
        ps1 = cfg.getPsCfg(0)
        self._prepare(ps1)
        self._verifyEnumServer(ps1, ps1, ps1.getInternalIp())
        log._file.debug("<<< Config Enum in Single Mode Begin")


    def _configEnumEntry1(self):
        log._file.debug(">>> Config Enum in Entry1 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
        self._prepare(ps1)
        self._prepare(ps2)
        self._verifyEnumServer(ss1, ps1, ss1.getInternalIp())
        log._file.debug("<<< Config Enum in Entry1 Mode End")


    def _configEnumEntry2(self):
        log._file.debug(">>> Config Enum in Entry2 Mode")
        cfg = cfgInstance()
        ps1 = cfg.getPsCfg(0)
        ss1 = cfg.getSsCfg(0)
        self._prepare(ps1)
        self._prepare(ss1)
        self._verifyEnumServer(ss1, ps1, ss1.getInternalIp())
        log._file.debug("<<< Config Enum in Entry2 Mode End")
 

    def _configEnumMedium1(self):
        log._file.debug(">>> Config Enum in Medium1 Mode")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
        self._prepare(ps1)
        self._prepare(ps2)
        self._verifyEnumServer(ss1, ps1, cfg.getHaCfg().getSsVip())
        log._file.debug("<<< Config Enum in Medium1 Mode")


    def _verifyEnumServer(self, ss_cfg, ps_cfg, ss_vip) :
        log._file.debug(">>> Verify DNS & Enum Server Begin")
        host_list = []
        host_list.append(["dns1", ps_cfg.getOamIp(), 1])
        try :
            # config env
            self._create(ss_cfg, host_list, ss_vip)  # on ss
            self._startSm(ps_cfg)  # on ps
            self._configMasterZone(ss_cfg, host_list[0][0], ss_vip)  # on ss 
            self._configEnumZone(ss_cfg, ss_vip)
            self._startDnsEnum(ss_cfg, host_list, ss_vip)  # on ss
            self._verifyDnsEnum(ps_cfg)  # on ps
            # check alarm on ps
            self._checkAlarm(ps_cfg)
            # check error log
            errutil.checkENUMErrorLog(ps_cfg)
        except Exception, e :
            log._file.error("Exception in _verifyEnumServer : " + str(e))
            raise
        finally :
            # clean env
            self._cleanEnumZone(ss_cfg, ss_vip)  # on ss
            self._cleanMasterZone(ss_cfg, ss_vip)  # on ss
            self._stopDnsEnum(ss_cfg, ss_vip)  # on ss
            self._stopSm(ps_cfg)  # on ps
            self._delete(ss_cfg, host_list, ss_vip)  # on ss
        log._file.debug("<<< Verify DNS & ENUM Server End")







