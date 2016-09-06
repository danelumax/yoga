import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class InstallHATask(object) :
    """
    Install HA RPM
    """

    def __init__(self) :
        self._cfg = cfgInstance()
        self._os_alise = "SuSE_OS"
        self._hae_alise = "SuSE_HA"
        self._hostname = common.getHostName()

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">>> Install HA Begin")
        # install HA on SS nodes
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            for cfg in self._cfg.getSsCfgList() :
                self._removeRepository(cfg)
                self._addRepository(cfg)
                self._installHA(cfg)
                self._removeRepository(cfg)      
        # install HA on PS nodes
        if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            for cfg in self._cfg.getPsCfgList() :
                self._removeRepository(cfg)
                self._addRepository(cfg)
                self._installHA(cfg)    
                self._removeRepository(cfg)         
        log._file.debug("<<< Install HA End")
        
        

    def verify(self) :
        pass

    def updateProgress(self) :
        pass


    def _addRepository(self, cfg) :
        log._file.debug(">> Add repository on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        
        log._file.debug("add %s" %self._os_alise)
        if cmp(cfg.getHostName(), self._hostname) :
            cmd = "zypper ar \"iso:///?iso=%s&url=file://%s\" \"%s\"" %(self._cfg.getOsIsoName(), self._cfg.getInstallPath(), self._os_alise)
        else :
            iso_path = self._cfg.getOsIsoPath()
            iso_path = iso_path[0:iso_path.rfind('/')]
            cmd = "zypper ar \"iso:///?iso=%s&url=file://%s\" \"%s\"" %(self._cfg.getOsIsoName(), iso_path, self._os_alise)
        #log._file.debug("cmd: " + cmd)
        ssh_util.remote_exec(cmd)
        
        log._file.debug("add %s" %self._hae_alise)
        if cmp(cfg.getHostName(), self._hostname) :
            cmd = "zypper ar \"iso:///?iso=%s&url=file://%s\" \"%s\"" %(self._cfg.getHaeIsoName(), self._cfg.getInstallPath(), self._hae_alise)
        else :
            iso_path = self._cfg.getHaeIsoPath()
            iso_path = iso_path[0:iso_path.rfind('/')]
            cmd = "zypper ar \"iso:///?iso=%s&url=file://%s\" \"%s\"" %(self._cfg.getHaeIsoName(), iso_path, self._hae_alise)
        #log._file.debug("cmd: " + cmd)
        ssh_util.remote_exec(cmd)
        log._file.debug("<<")
    
    
    
    def _removeRepository(self, cfg) :
        log._file.debug(">> Remove repository on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        #cmd = "zypper lr |awk -F \"|\" \'/^[0-9]/ {print $2}\'"
        #log._file.debug("cmd: " + cmd)
        res, code = ssh_util.remote_exec("zypper lr |awk -F \"|\" \'/^[0-9]/ {print $2}\'")
        tmp = res.split('\n')[1:]
        log._file.debug("Repostories: %s" %tmp)
        for x in tmp :
            log._file.debug("Remove: " + x)
            ssh_util.remote_exec("zypper rr \"%s\"" %x.strip())
        log._file.debug("<<")
        
        
        
    def _installHA(self, cfg) :
        log._file.debug(">> Install HA package on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh) 
        #cmd = "zypper -n in -t pattern -l ha_sles"
        #log._file.debug("cmd: " + cmd)
        log._file.debug("install HA packages")
        ssh_util.remote_exec("zypper -n in -t pattern -l ha_sles")
        #cmd = "zypper -n in ocfs2-tools-o2cb"
        #log._file.debug("cmd: " + cmd)
        log._file.debug("install o2cb packages")
        ssh_util.remote_exec("zypper -n in ocfs2-tools-o2cb")
        log._file.debug("<<")
    
    
    
