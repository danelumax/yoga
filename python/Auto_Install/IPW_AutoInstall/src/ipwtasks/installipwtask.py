import threading, traceback, sys, time, re
import log, common
from cfg import cfgInstance
from healthcheckinfo import healthcheckInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from installthread import InstallThread


class InstallIpwTask(object) :
    """
    Install IPWorks RPMs
    """

    def __init__(self) :
        self._file = "src/ipwtasks/rpm_install.json"
        self._is_install_ndb = False

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Install IPWorks Begin")	
        if common.g_isInstall_AAA or common.g_isInstall_ENUM :
            self._is_install_ndb = True
        # single:
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._install_Single()
        # medium1:
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :
            self._install_Medium1()
        # medium2:
        if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._install_Medium2()
        # entry1:
        if not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._install_Entry1()
        # entry2:
        if not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._install_Entry2()
        log._file.debug("<< Install IPWorks End")


    def verify(self) :
        ipw_version = healthcheckInstance().getIpwVersion()
        if ipw_version == "":
            log._file.info("Ipworks version is not configured, so doesn't need to check it!")
            return 
        check_list = common.getNodeList(cfgInstance())
        for host in check_list:
            self._checkIpwVersion(host)
        common.save_healthcheck_info("IPWorks Version", ipw_version, ipw_version, "OK")


    def updateProgress(self) :
        pass



    def _install_Single(self) :
        log._file.debug(">>> Install Single Mode Begin")
        json_root = common.parse_file(self._file)
        ps1 = cfgInstance().getPsCfg(0)
        rpm_list = ["Element_Manager", "SLM", "SM"]
        if self._is_install_ndb :
            rpm_list.append("NDB_Single")
        if common.g_isInstall_AAA :
            rpm_list.append("AAA_Single")
        if common.g_isInstall_DNS :
            rpm_list.append("DNS_Single")
        if common.g_isInstall_ENUM :
            rpm_list.append("ENUM_Single")
        if common.g_isInstall_DHCP :
            rpm_list.append("DHCP_Single")
        self._rmLogs(ps1)
        thread_t = InstallThread(ps1, rpm_list, json_root, cfgInstance().getInstallSS7())
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        self._join()
        log._file.debug("<<< Install Single Mode End")



    def _install_Entry1(self) :
        log._file.debug(">>> Install Entry1 Mode Begin")
        json_root = common.parse_file(self._file)
        ss1 = cfgInstance().getSsCfg(0)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        ss_rpm  = ["Element_Manager", "SLM"]
        ps1_rpm = ["Entry_Common", "SLM", "SM"]
        ps2_rpm = ["Entry_Common", "SM"]
        if common.g_isInstall_AAA :
            ss_rpm.append("NDB_NonSingle")
            ps1_rpm.append("AAA_NonSingle")
            ps2_rpm.append("AAA_NonSingle")
        if common.g_isInstall_ENUM :
            ps1_rpm.append("NDB_Single")
            ps1_rpm.append("ENUM_Single")
            ps2_rpm.append("NDB_Single")
            ps2_rpm.append("ENUM_Single")
        if common.g_isInstall_DNS :
            ps1_rpm.append("DNS_Single")
            ps2_rpm.append("DNS_Single")
        if common.g_isInstall_DHCP :
            ps1_rpm.append("DHCP_Single")
            ps2_rpm.append("DHCP_Single")
        for node in [ss1, ps1, ps2] :
            self._rmLogs(node)
        thread_t = InstallThread(ss1, ss_rpm, json_root)
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ps1, ps1_rpm, json_root, cfgInstance().getInstallSS7())
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ps2, ps2_rpm, json_root, cfgInstance().getInstallSS7())
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        self._join()
        log._file.debug("<<< Install Entry1 Mode End")



    def _install_Entry2(self) :
        log._file.debug(">>> Install Entry2 Mode Begin")
        json_root = common.parse_file(self._file)
        ss1 = cfgInstance().getSsCfg(0)
        ps1 = cfgInstance().getPsCfg(0)
        ss_rpm = ["Element_Manager", "SLM", "SM"]
        ps_rpm = ["Entry_Common", "SLM", "SM"]
        if common.g_isInstall_DNS :
            ss_rpm.append("DNS_Single")
            ps_rpm.append("DNS_Single")
        if common.g_isInstall_ENUM :
            ss_rpm.append("NDB_Single")
            ps_rpm.append("NDB_Single")
            ss_rpm.append("ENUM_Single")
            ps_rpm.append("ENUM_Single")
        if common.g_isInstall_DHCP :
            ss_rpm.append("DHCP_Single")
            ps_rpm.append("DHCP_Single")
        for node in [ss1, ps1] :
            self._rmLogs(node)
        thread_t = InstallThread(ss1, ss_rpm, json_root, cfgInstance().getInstallSS7())
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ps1, ps_rpm, json_root, cfgInstance().getInstallSS7())
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        self._join()
        log._file.debug("<<< Install Entry2 Mode End")



    def _install_Medium1(self) :
        log._file.debug(">>> Install Medium1 Mode Begin")
        json_root = common.parse_file(self._file)
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        ss_rpm = ["Element_Manager", "Element_Manager_HA", "SLM"]
        ps_rpm = ["Entry_Common", "SM"]
        if common.g_isInstall_AAA :
            ss_rpm.append("NDB_NonSingle")
            ps_rpm.append("AAA_NonSingle")
        if common.g_isInstall_ENUM :
            ps_rpm.append("NDB_Single")
            ps_rpm.append("ENUM_Single")
        if common.g_isInstall_DNS :
            ps_rpm.append("DNS_Single")
        if common.g_isInstall_DHCP :
            ps_rpm.append("DHCP_Single")
        for node in [ss1, ss2, ps1, ps2] :
            self._rmLogs(node)
        thread_t = InstallThread(ss1, ss_rpm, json_root)
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ss2, ss_rpm, json_root)
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ps1, ps_rpm, json_root, cfgInstance().getInstallSS7())
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ps2, ps_rpm, json_root, cfgInstance().getInstallSS7())
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        self._join()
        self._adduser(ss1)
        self._adduser(ss2)
        log._file.debug("<<< Install Medium1 Mode End")



    def _install_Medium2(self) :
        log._file.debug(">>> Install Medium2 Mode Begin")
        json_root = common.parse_file(self._file)
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        if cfgInstance().getClfCfg().isInstallEM() :
            ss_rpm = ["Element_Manager", "Element_Manager_HA", "SLM", "CLF_EM"]
        else :
            ss_rpm = ["Element_Manager", "Element_Manager_HA", "SLM"]
        ps_rpm = ["Entry_Common", "SM", "DHCP_Single", "CLF", "Element_Manager_HA"]
        for node in [ss1, ss2, ps1, ps2] :
            self._rmLogs(node)
        thread_t = InstallThread(ss1, ss_rpm, json_root)
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ss2, ss_rpm, json_root)
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ps1, ps_rpm, json_root)
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        thread_t = InstallThread(ps2, ps_rpm, json_root)
        thread_t.setDaemon(True)
        common.g_install_thread.append(thread_t)
        self._join()
        self._adduser(ss1)
        self._adduser(ss2)
        log._file.debug("<<< Install Medium2 Mode End")

	
    def _join(self) :
        try :
            for x in common.g_install_thread :
                x.start()
            while 1 :
                alive = False
                for x in common.g_install_thread :
                    alive = alive or x.isAlive()
                if alive :
                    time.sleep(1.0)
                else :
                    common.g_install_thread = []
                    break
        except Exception as e :
            log._all.error("Exception info: " + str(e))
            raise Exception("Running Install Thread Failed")


    def _checkIpwVersion(self, cfg):
        log._file.debug(">>> Check IPWorks Version on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec('/opt/ipworks/IPWcommon/scripts/ipwversion')
        log._file.info("Fatch IPWorks version:\n%s" %(res))
        if not re.search(healthcheckInstance().getIpwVersion(), res):
            log._file.error("IPWorks Version is Incorrect !")
            raise Exception("IPWorks Version is Incorrect !")
        log._file.debug("<<<")


    def _rmLogs(self, cfg):
        log._file.debug(">>> Remove IPWorks Logfiles on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec('rm -rf /var/ipworks', p_err=False, throw=False)
        ssh_util.remote_exec('rm -rf /var/log/clfd', p_err=False, throw=False)
        ssh_util.remote_exec('rm -rf /var/log/pmald', p_err=False, throw=False)
        log._file.debug("<<<")


    # add user hacluster to group ipworks on each SS
    def _adduser(self, cfg) :
        log._file.debug(">>> Add user ipworks to group ipworks on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec('usermod -A ipworks hacluster')
        log._file.debug("<<<")



