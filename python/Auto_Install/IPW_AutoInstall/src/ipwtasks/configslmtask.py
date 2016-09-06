import os
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class ConfigSlmTask(object) :
    """
    Config License Server
    """

    def __init__(self) :
        self._license_path = cfgInstance().getInstallPath() + cfgInstance().getLicenseName()


    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Config SLM Begin")
        # single
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._configLM_Single()
        # medium1 & medium2
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
           or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configLM_Medium()
        # entry1
        if not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._configLM_Entry1()
        # entry2
        if not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._configLM_Entry2()
        log._file.debug("<< Config SLM End")


    def verify(self) :
        log._file.debug(">> Check License Server Ready Begin")
        common.save_healthcheck_info("License Server Status", 'running normal', 'running normal', "OK")
        log._file.debug("<< Check License Server Ready End")

    def updateProgress(self) :
        pass


    def _check_file_exists(self, node, filePath):
        log._file.debug(">>> check %s is exist on %s" %(filePath, node.getHostName()))
        ssh = sshManagerInstance().getSsh(node.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("ls " + filePath)
        log._file.debug("<<<")


    def _startSlmServer(self, node) :
        log._file.debug(">>> _startSlmServer on " + node.getHostName())
        ssh = sshManagerInstance().getSsh(node.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = "python configslm.py --role=server --license=" + cfgInstance().getLicenseName()
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _startSlmClient(self, node, primary_ip=None, secondary_ip=None) :
        log._file.debug(">>> _startSlmClient on " + node.getHostName())
        ssh = sshManagerInstance().getSsh(node.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = "python configslm.py --role=client"
        if primary_ip != None:
            command = command + " --primary_ip=" + primary_ip
        if secondary_ip != None:
            command = command + " --secondary_ip=" + secondary_ip
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _configLM_Single(self) :
        log._file.debug(">>> Config License Management in Single Mode Begin")
        ps1 = cfgInstance().getPsCfg(0)
        self._check_file_exists(ps1, self._license_path)
        self._startSlmServer(ps1)
        self._startSlmClient(ps1, ps1.getOamIp())
        log._file.debug("<<< Config License Management in Single Mode End")


    def _configLM_Medium(self) :
        log._file.debug(">>> Config License Management in Medium Mode Begin")
        cfg = cfgInstance()
        for ss_cfg in cfg.getSsCfgList() :
            self._check_file_exists(ss_cfg, self._license_path)
            self._startSlmServer(ss_cfg)
        primary_ip = None
        secondary_ip = None
        for ss_cfg in cfg.getSsCfgList():
            if not primary_ip :
                primary_ip = ss_cfg.getOamIp()
            else :
                secondary_ip = ss_cfg.getOamIp()
        for ps_cfg in cfg.getPsCfgList() :
            self._startSlmClient(ps_cfg, primary_ip, secondary_ip)
        log._file.debug("<<< Config License Management in Medium Mode End")


    def _configLM_Entry1(self) :
        log._file.debug(">>> Config License Management in Entry1 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
        self._check_file_exists(ss1, self._license_path)
        self._check_file_exists(ps1, self._license_path)
        self._startSlmServer(ss1)
        self._startSlmServer(ps1)
        self._startSlmClient(ps1, ss1.getOamIp(), ps1.getOamIp())
        self._startSlmClient(ps2, ss1.getOamIp(), ps1.getOamIp())
        log._file.debug("<<< Config License Management in Entry1 Mode End")


    def _configLM_Entry2(self) :
        log._file.debug(">>> Config License Management in Entry2 Mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        self._check_file_exists(ss1, self._license_path)
        self._check_file_exists(ps1, self._license_path)
        self._startSlmServer(ss1)
        self._startSlmServer(ps1)
        self._startSlmClient(ss1, ss1.getOamIp(), ps1.getOamIp())
        self._startSlmClient(ps1, ss1.getOamIp(), ps1.getOamIp())
        log._file.debug("<<< Config License Management in Entry2 Mode End")





