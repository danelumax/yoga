import log, common
from sshutil import SshUtil
from cfg import cfgInstance
from hautil import hautilInstance
from sshmanager import sshManagerInstance
import errutil


class ConfigDhcpTask(object) :
    """
    Config DHCP Server
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Config DHCP Service Begin")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._configDHCPSingle()            
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._configDHCPEntry1()
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._configDHCPEntry2()
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configDHCPMedium()
        log._file.debug("<< Config DHCP Service End")

    def verify(self) :
        log._file.debug(">> Check DHCP Server Status Begin")
        common.save_healthcheck_info("DHCP Server Status", 'normal', 'normal', "OK")
        log._file.debug("<< Check DHCP Server Status End")

    def updateProgress(self) :
        pass


    def _configServerManager(self,cfg):
        log._file.debug(">>> Config dhcp server manager on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=confDhcpSM --ipwss_vip=%s --username=%s --password=%s ' %(cfg.getSsVip(),common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _startSm(self, cfg):
        log._file.debug(">>> Start dhcpv4 server manager on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=start_dhcpv4sm --username=%s  --password=%s' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopSm(self, cfg):
        log._file.debug(">>> Stop dhcpv4 server manager on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=stop_dhcpv4sm --username=%s --password=%s' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _createDhcpV4ServerFailoverMode(self, ss_cfg, ip1, ip2, ss_vip):
        log._file.debug(">>> Create dhcpv4 in failover mode on host " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=createDhcpFailover --username=%s --password=%s --ipwss_vip=%s --primary=%s --secondary=%s' %(common.g_cli_username, common.g_cli_password, ss_vip, ip1, ip2)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopDhcpV4ServerFailoverMode(self, ss_cfg, ss_vip):
        log._file.debug(">>> Stop dhcpv4 in failover mode on host " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=stopDhcpFailover --username=%s --password=%s --ipwss_vip=%s' %(common.g_cli_username, common.g_cli_password,ss_vip)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _deleteDhcpV4ServerFailoverMode(self, ss_cfg, ss_vip):
        log._file.debug(">>> Delete dhcpv4 in failover mode on host " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=deleteDhcpFailover --username=%s --password=%s --ipwss_vip=%s ' %(common.g_cli_username,common.g_cli_password, ss_vip)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _createDhcpV4ServerNormalMode(self, ss_cfg):
        log._file.debug(">>> Create dhcpv4 in normal mode on host " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=createDhcpNormal --primary=%s --username=%s --password=%s ' %( ss_cfg.getOamIp(),common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopDhcpV4ServerNormalMode(self, ss_cfg):
        log._file.debug(">>> Stop dhcpv4 in normal mode on host " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=stopDhcpNormal --primary=%s --username=%s --password=%s' %(ss_cfg.getOamIp(),common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _deleteDhcpV4ServerNormalMode(self, ss_cfg):
        log._file.debug(">>> Delete dhcpv4 in normal mode on host " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=deleteDhcpNormal --primary=%s --username=%s --password=%s ' %( ss_cfg.getOamIp(), common.g_cli_password,common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")

    
    def _verifyDhcpV4ServiceNormalMode(self, cfg, ss_vip):
        log._file.debug(">>> Verify dhcpv4 service in normal mode on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=verifyDhcp --ipwss_vip=%s --username=%s --password=%s' %(ss_vip,common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _verifyDhcpV4ServiceFailoverMode(self, cfg, ss_vip):
        log._file.debug(">>> Verify dhcpv4 service in failover mode on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=verifyDhcpFailover --ipwss_vip=%s --username=%s --password=%s ' %(ss_vip, common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")
    

    def _createSubnet(self, cfg, ss_vip) :
        log._file.debug(">>> Create Subnet & Pool on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=createSubnet --ipwss_vip=%s  --username=%s --password=%s' %(ss_vip,common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _deleteSubnet(self, cfg, ss_vip) :
        log._file.debug(">>> Delete Subnet & Pool on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=deleteSubnet --ipwss_vip=%s --username=%s --password=%s ' %(ss_vip,common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _checkAlarm(self, cfg):
        log._file.debug(">>> Check DHCP Alarm on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        command = common.getAlarmCmd('ipworksDhcpv4')
        res,code = ssh_util.remote_exec(command, p_err=False, throw=False)
        alarm = common.parseAlarmInfo(res)
        if alarm :
            item = "Alarm %s On %s" %('ipworksDhcpv4', cfg.getHostName())
            common.save_healthcheck_info(item, alarm, "", "--")
        log._file.debug("<<<")

######################################################################################

    def _configDHCPSingle(self):
        log._file.debug(">>> Config DHCP in Single Mode Begin")
        ps1 = cfgInstance().getPsCfg(0)
        self._cleanCfgfile(ps1)
        try :
            # create
            self._createDhcpV4ServerNormalMode(ps1)
            self._createSubnet(ps1, ps1.getInternalIp())
            self._startSm(ps1)
            self._enable_log(ps1)
            # verify
            self._verifyDhcpV4ServiceNormalMode(ps1, ps1.getInternalIp())
            # check alarm on ps
            self._checkAlarm(ps1)
            # check error log
            errutil.checkDHCPErrorLog(ps1)
        except Exception, e :
            log._file.error("Exception in _configDHCPSingle : " + str(e))
            raise
        finally :
            # cleanup
            self._stopDhcpV4ServerNormalMode(ps1)
            self._stopSm(ps1)
            self._deleteSubnet(ps1, ps1.getInternalIp())
            self._deleteDhcpV4ServerNormalMode(ps1)
        log._file.debug("<<< Config DHCP in Single Mode End")


    def _configDHCPEntry1(self):
        log._file.debug(">>> Config DHCP in Entry1 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfgInstance().getSsCfg(0)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        self._syncTime(ps1, ps2)
        self._cleanCfgfile(ps1)
        self._cleanCfgfile(ps2)
        try :
            # create
            self._createDhcpV4ServerFailoverMode(ss1, ps1.getOamIp(), ps2.getOamIp(), ss1.getInternalIp())
            self._createSubnet(ss1, ss1.getInternalIp())
            self._startSm(ps1)
            self._startSm(ps2)
            self._enable_log(ps1)
            self._enable_log(ps2)
            # verify
            self._verifyDhcpV4ServiceFailoverMode(ss1, ss1.getInternalIp())
            # check alarm on ps
            self._checkAlarm(ps1)
            self._checkAlarm(ps2)
            # check error log
            errutil.checkDHCPErrorLog(ps1)
            errutil.checkDHCPErrorLog(ps2)
        except Exception, e :
            log._file.error("Exception in _configDHCPEntry1 : " + str(e))
            raise
        finally :
            # cleanup
            self._stopDhcpV4ServerFailoverMode(ss1, ss1.getInternalIp())
            self._stopSm(ps1)
            self._stopSm(ps2)
            self._deleteSubnet(ss1, ss1.getInternalIp())
            self._deleteDhcpV4ServerFailoverMode(ss1, ss1.getInternalIp())
        log._file.debug("<<< Config DHCP in Entry1 Mode End")


    def _configDHCPEntry2(self):
        log._file.debug(">>> Config DHCP in Entry2 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfgInstance().getSsCfg(0)
        ps1 = cfgInstance().getPsCfg(0)
        self._syncTime(ss1, ps1)
        self._cleanCfgfile(ss1)
        self._cleanCfgfile(ps1)
        try :
            # create
            self._createDhcpV4ServerFailoverMode(ss1, ps1.getOamIp(), ss1.getOamIp(), ss1.getInternalIp())
            self._createSubnet(ss1, ss1.getInternalIp())
            self._startSm(ss1)
            self._startSm(ps1)
            self._enable_log(ss1)
            self._enable_log(ps1)
            # verify
            self._verifyDhcpV4ServiceFailoverMode(ss1, ss1.getInternalIp())
            # check alarm on ps
            self._checkAlarm(ps1)
            self._checkAlarm(ss1)
            # check error log
            errutil.checkDHCPErrorLog(ps1)
            errutil.checkDHCPErrorLog(ss1)
        except Exception, e :
            log._file.error("Exception in _configDHCPEntry2 : " + str(e))
            raise
        finally :
            # cleanup
            self._stopDhcpV4ServerFailoverMode(ss1, ss1.getInternalIp())
            self._stopSm(ps1)
            self._stopSm(ss1)
            self._deleteSubnet(ss1, ss1.getInternalIp())
            self._deleteDhcpV4ServerFailoverMode(ss1, ss1.getInternalIp())
        log._file.debug("<<< Config DHCP in Entry2 Mode End")


    def _configDHCPMedium(self):
        log._file.debug(">>> Config DHCP in Medium1/2 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
        self._syncTime(ps1, ps2)
        self._cleanCfgfile(ps1)
        self._cleanCfgfile(ps2)
        try :
            # create
            self._createDhcpV4ServerFailoverMode(ss1, ps1.getOamIp(), ps2.getOamIp(), cfg.getHaCfg().getSsVip())
            self._createSubnet(ss1, cfg.getHaCfg().getSsVip())
            self._startSm(ps1)
            self._startSm(ps2)
            self._enable_log(ps1)
            self._enable_log(ps2)
            # verify
            self._verifyDhcpV4ServiceFailoverMode(ss1, cfg.getHaCfg().getSsVip())
            # check alarm on ps
            self._checkAlarm(ps1)
            self._checkAlarm(ps2)
            # check error log
            errutil.checkDHCPErrorLog(ps1)
            errutil.checkDHCPErrorLog(ps2)
        except Exception as e :
            log._file.error("Exception in _configDHCPMedium : " + str(e))
            raise
        finally :
            # clean
            self._stopDhcpV4ServerFailoverMode(ss1, cfg.getHaCfg().getSsVip())
            self._stopSm(ps1)
            self._stopSm(ps2)
            self._deleteSubnet(ss1, cfg.getHaCfg().getSsVip())
            self._deleteDhcpV4ServerFailoverMode(ss1, cfg.getHaCfg().getSsVip())
        log._file.debug("<<< Config DHCP in Medium1/2 Mode End")


    def _cleanCfgfile(self, cfg) :
        log._file.debug(">>> Clean DHCP config file on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("rm -f /etc/ipworks/dhcpv4/*")
        ssh_util.remote_exec("touch /etc/ipworks/dhcpv4/dhcpd.leases")
        log._file.debug("<<<")


    def _syncTime(self, ps1, ps2) :
        log._file.debug(">>> Sync system time between Primary and Secondary Begin")
        t1, c1 = self._getSystemTime(ps1)
        t2, c2 = self._getSystemTime(ps2)
        if cmp(c1, c2) :
            self._setSystemTime(ps2, t1)
            log._file.debug("Find system time difference between Primary and Secondary, ajust PS2 to PS1")
        else :
            log._file.debug("The system time is no difference between Primary and Secondary")
        log._file.debug("<<< Sync system time between Primary and Secondary End")


    def _getSystemTime(self, cfg) :
        log._file.debug(">>> Fetch system time (UTC) on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, code = ssh_util.remote_exec("date '+%Y-%m-%d %H:%M:%S' -u")
        sys_time = res.split('\n')[1]
        log._file.debug("time: " + sys_time)
        cmp_time = sys_time[0:sys_time.rfind(':')]
        log._file.debug("compare time: " + cmp_time)
        log._file.debug("<<<")
        return sys_time, cmp_time


    def _setSystemTime(self, cfg, sys_time) :
        log._file.debug(">>> Set system time (UTC) on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("date -s '%s' -u" %sys_time)
        log._file.debug("<<<")


    def _enable_log(self, cfg) :
        log._file.debug(">>> Enbale DHCP Log on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configdhcp.py --command=enableLog --username=%s --password=%s' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")




