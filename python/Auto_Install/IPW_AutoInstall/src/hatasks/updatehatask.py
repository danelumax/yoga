import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class UpdateHATask(object) :
    """
    Update HA Patch
    """

    def __init__(self) :
        self._hostname = common.getHostName()

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">>> Update HA Begin")
        # Update HA on SS or PS nodes
        if cfgInstance().getHaCfg().getNeedUpdate() :
            if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
              or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                for cfg in cfgInstance().getSsCfgList() :
                    self._updateHA(cfg)
            if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                for cfg in cfgInstance().getPsCfgList() :
                    self._updateHA(cfg)
        log._file.debug("<<< Update HA End")


    def verify(self) :
        pass

    def updateProgress(self) :
        pass
    
    def _updateHA(self, cfg) :
        log._file.debug(">> Update HA patch on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if cmp(cfg.getHostName(), self._hostname) :
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        else :
            ssh_util.remote_exec("cd " + cfgInstance().getHaCfg().getUpdatePath())
        for x in cfgInstance().getHaCfg().getUpdateCmds() :
            #log._file.debug("exec update cmd: " + x)
            ssh_util.remote_exec(x, p_err=False, throw=False)
        # confirm HA patch is loaded
        res,code = ssh_util.remote_exec("rpm -q pacemaker")
        if not re.search("pacemaker-1.1.10-0.15.25", res) :
            log._file.error("HA patch load failed !!!")
            raise Exception("Failed to load HA Patch")
        log._file.debug("<<")
    
    
