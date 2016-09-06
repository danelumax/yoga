import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from hautil import hautilInstance
import errutil


class ConfigClfTask(object) :
    """
    Config CLF
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Config CLF Service Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):
            ss1 = cfgInstance().getSsCfg(0)
            ps1 = cfgInstance().getPsCfg(0)
            ps2 = cfgInstance().getPsCfg(1)
            self._register_ha_resource(ps1)
            self._start_ha_resource(ps1)

            self._modify_clfd_conf(ps1)
            self._stop_ha_resource(ps1)
            self._check_sctp_stack(ps1)
            self._check_sctp_stack(ps2)
            self._enable_clf_interface(ps1)
            self._enable_clf_interface(ps2)
            self._start_ha_resource(ps1)
            self._verify_clf(ss1)
        else :
            log._file.debug("No need to config CLF")
        log._file.debug(">> Config CLF Service End")

    def verify(self) :
        pass

    def updateProgress(self) :
        pass


    def _register_ha_resource(self, cfg) :
        log._file.debug(">>> Register CLF HA resource on " + cfg.getHostName())
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps2 = cfgInstance().getPsCfg(1)
        slm_ip = "%s,%s" %(ss1.getOamIp(), ss2.getOamIp())
        passwd = ps2.getPassword()
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            hacfg = cfgInstance().getHaCfg()
            clf_dev = ''
            if hacfg.getHaDisk03() :
                if hacfg.getHaDisk04() :
                    clf_dev = '/dev/md0'
                else :
                    clf_dev = "%s1" %(hacfg.getHaDisk03())
            command = 'python register_cluster.py --command=clf --password=%s --mode=diskarray --slm_ip=%s --clf_dev=%s' %(passwd, slm_ip, clf_dev)
        else :
            command = 'python register_cluster.py --command=clf --password=%s --mode=nfs --slm_ip=%s' %(passwd, slm_ip)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec(command)
        # wait for fs clone start
        if common.C_EMC_MOUNT_MODE_DOUBLE:
            hautilInstance().waitIpworksCloneStart(ssh)
        log._file.debug("<<<")


    def _start_ha_resource(self, cfg) :
        log._file.debug(">>> Start CLF HA resource on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        hautilInstance().startClfResGrp(ssh)
        hautilInstance().waitClfResGrpStart(ssh)
        log._file.debug("<<<")


    def _stop_ha_resource(self, cfg) :
        log._file.debug(">>> Stop CLF HA resource on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        hautilInstance().stopClfResGrp(ssh)
        hautilInstance().waitClfResGrpStop(ssh)
        log._file.debug("<<<")


    def _check_sctp_stack(self, cfg) :
        log._file.debug(">>> Check SCTP stack on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("modprobe sctp")
        ssh_util.remote_exec("lsmod |grep sctp")
        log._file.debug("<<<")


    def _enable_clf_interface(self, cfg) :
        log._file.debug(">>> CLF Interface Enable on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec('python configclf.py --command=enable_clf_int --username=%s --password=%s' %(common.g_cli_username,common.g_cli_password))
        log._file.debug("<<<")


    def _modify_clfd_conf(self, cfg) :
        log._file.debug(">>> Modify clfd.conf on " + cfg.getHostName())
        clfcfg = cfgInstance().getClfCfg()
        # in customer site must be used traffic ip to config
        ip1 = cfgInstance().getPsCfg(0).getTrafficIp()
        ip2 = cfgInstance().getPsCfg(1).getTrafficIp()
        # in our lab use internal ip
        #ip1 = cfgInstance().getPsCfg(0).getInternalIp()
        #ip2 = cfgInstance().getPsCfg(1).getInternalIp()
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec('python configclf.py --command=config_clf --username=%s --password=%s --dhcp1_ip=%s --dhcp2_ip=%s --address_zone=%s --clf_sbc_e2_host=%s --clf_sbc_e2_transport=%s --sbc_e2_peer_host=%s' %(common.g_cli_username, common.g_cli_password, ip1, ip2, clfcfg.getNacfZone(), clfcfg.getClfHost(), clfcfg.getClfTransport(), clfcfg.getSbcHost()))
        log._file.debug("<<<")


    def _verify_clf(self, cfg) :
        log._file.debug(">>> Verify CLF and DHCP Connection on " + cfg.getHostName())
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        self._cleanCfgfile(ps1)
        self._cleanCfgfile(ps2)
        clfcfg = cfgInstance().getClfCfg()
        hacfg = cfgInstance().getHaCfg()
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        try :
            # config CLF and DHCP
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
            command = 'python configclf.py --command=config_dhcp --username=%s --password=%s --dhcp1_ip=%s --dhcp2_ip=%s --address_zone=%s --clf_a2_ip=%s --ipwss_vip=%s' %(common.c_cli_username, common.g_cli_password, ps1.getInternalIp(), ps2.getInternalIp(), clfcfg.getNacfZone(), hacfg.getA2Vip(), hacfg.getSsVip())
            ssh_util.remote_exec(command)
            self._startSm(ps1)
            self._startSm(ps2)
            command = 'python configdhcp.py --command=verifyDhcpFailover --username=%s --password=%s --ipwss_vip=%s' %(common.g_cli_username, common.g_cli_password, hacfg.getSsVip())
            ssh_util.remote_exec(command)
            # Check Connection between CLF and DHCP
            self._checkClfLicense(ps1, hacfg.getPmalVip())
            self._check_conn_status(ps1, hacfg.getPmalVip())
            # Check Alarm
            self._checkAlarm(ps1)
            self._checkAlarm(ps2)
            # check error log
            errutil.checkCLFErrorLog(ps1)
            errutil.checkCLFErrorLog(ps2)
        except Exception, e :
            log._file.error("Exception in _verify_clf : " + str(e))
            raise
        finally :
            # clean all configure
            command = 'python configdhcp.py --command=stopDhcpFailover --username=%s --password=%s --ipwss_vip=%s' %(common.g_cli_username, common.g_cli_password, hacfg.getSsVip())
            ssh_util.remote_exec(command)
            self._stopSm(ps1)
            self._stopSm(ps2)
            command = 'python configclf.py --command=clean_dhcp --username=%s --password=%s --ipwss_vip=%s' %(common.g_cli_username, common.g_cli_password, hacfg.getSsVip())
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _check_conn_status(self, cfg, pmal_ip) :
        log._file.debug(">>> Check Connection Status between CLF and DHCP on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = '/opt/ipworks/IPWpmal/scripts/cli.pl -ip %s -port 80 -login super NGRCroot -one "clf.interfaces.nacf.show"' %(pmal_ip)
        res,code = ssh_util.remote_exec(command, p_err=False, throw=False)
        if re.search('NOT CONNECTED', res) :
            log._file.error("CLF and NACF: NOT CONNECTED")
            raise Exception("The Connection between CLF and NACF NOT CONNECTED")
        elif re.search('CONNECTED', res) :
            log._file.info("CLF and NACF: CONNECTED")
        else :
            log._file.error("CLF and NACF: incorrect")
            raise Exception("The Connection between CLF and NACF is incorrect")
        log._file.debug("<<<")


    def _startSm(self, cfg) :
        log._file.debug(">>> Start dhcpv4 server manager on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=start_dhcpv4sm --username=%s --password=%s ' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopSm(self, cfg) :
        log._file.debug(">>> Stop dhcpv4 server manager on host " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=stop_dhcpv4sm --username=%s --password=%s ' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _cleanCfgfile(self, cfg) :
        log._file.debug(">>> Clean DHCP config file on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("rm -f /etc/ipworks/dhcpv4/*")
        ssh_util.remote_exec("touch /etc/ipworks/dhcpv4/dhcpd.leases")
        log._file.debug("<<<")


    def _checkAlarm(self, cfg) :
        log._file.debug(">>> Check CLF and NACF Alarm on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        command = common.getAlarmCmd('ipworksCLF')
        res,code = ssh_util.remote_exec(command, p_err=False, throw=False)
        alarm = common.parseAlarmInfo(res)
        if alarm :
            item = "Alarm %s On %s" %('ipworksCLF', cfg.getHostName())
            common.save_healthcheck_info(item, alarm, "", "--")
        log._file.debug("<<<")


    def _checkClfLicense(self, cfg, pmal_ip) :
        log._file.debug(">>> Check CLF License on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = '/opt/ipworks/IPWpmal/scripts/cli.pl -ip %s -port 80 -login super NGRCroot -one "clf.licensing.show"' %(pmal_ip)
        res,code = ssh_util.remote_exec(command, p_err=False, throw=False)
        if re.search('License server contacted. License enforcement is active.', res) :
            item = "CLF License"
            common.save_healthcheck_info(item, "normal", "normal", "OK")
        else :
            errinfo = 'CLF License is incorrect'
            log._file.debug(errinfo)
            raise Exception(errinfo)
        log._file.debug("<<<")



