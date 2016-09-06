
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class ConfigSmTask(object):
    '''
    Config Server Manager
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
        log._file.debug(">> Config Server Manager Start")

        cfg = cfgInstance()

        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode):  # single
            self._prepare(cfg.getPsCfg(0), cfg.getPsCfg(0).getInternalIp())

        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode):  # entry1
            for ps_cfg in cfg.getPsCfgList() :
                self._prepare(ps_cfg, cfg.getSsCfg(0).getInternalIp())

        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode):  # entry2
            self._prepare(cfg.getSsCfg(0), cfg.getSsCfg(0).getInternalIp())
            self._prepare(cfg.getPsCfg(0), cfg.getSsCfg(0).getInternalIp())
 
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):  # medium1/2
            for ps_cfg in cfg.getPsCfgList() :
                self._prepare(ps_cfg, cfg.getHaCfg().getSsVip())

        log._file.debug("<< Config Server Manager End")


    def verify(self):
        #TODO: check the version.txt from the mount point
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass


    def _prepare(self, cfg, ss_ip) :
        log._file.debug(">>> Config Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=config --ipwss_vip=%s --username=%s --password=%s ' %( ss_ip, common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")



