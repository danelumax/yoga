import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from hautil import hautilInstance



class CfgCrmTask(object) :
    """
    Config CRM
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Config HA Crm Begin")
        # config CRM on SS nodes
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configCrm(cfgInstance().getSsCfg(0), "ss")
            self._waitingResUp(cfgInstance().getSsCfg(0))
        # config CRM on PS nodes
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configCrm(cfgInstance().getPsCfg(0), "ps")
            self._waitingResUp(cfgInstance().getPsCfg(0))
        log._file.debug("<< Config HA Crm End")


    def cleanup(self) :
        log._file.debug(">> Cleanup HA Crm Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._stopResGrp(cfgInstance().getSsCfg(0))
            self._resetCrm(cfgInstance().getSsCfg(0))
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._stopResGrp(cfgInstance().getPsCfg(0))
            self._resetCrm(cfgInstance().getPsCfg(0))
        log._file.debug("<< Cleanup HA Crm End")


    def _stopResGrp(self, cfg) :
        log._file.debug(">>> Stop ipw-lvm-clone on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        hautilInstance().stopLvmClone(ssh)
        hautilInstance().waitLvmCloneStop(ssh)
        log._file.debug("<<<")

    
    def _resetCrm(self, cfg) :
        log._file.debug(">>> Reset CRM on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec("python configcrm.py --command=reset_crm")
        log._file.debug("<<<")


    def verify(self) :
        pass

    def updateProgress(self) :
        pass


    def _configCrm(self, cfg, node) :
        log._file.debug(">>> Config CRM on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        cmd = "python configcrm.py --command=config_crm " + "--conf_file="
        if not cmp("ss", node) :
            if common.g_isInstall_AAA :
                cmd += "aaa.crm"
            else :
                cmd += "dns.crm"
        elif not cmp("ps", node) :
            if common.g_isInstall_CLF :
                cmd += "clf.crm"
        ssh_util.remote_exec(cmd)
        log._file.debug("<<<")


    def _waitingResUp(self, cfg) :
        log._file.debug(">>> Waiting ipw-lvm-clone start on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        hautilInstance().waitLvmCloneStart(ssh)
        log._file.debug("<<<")



