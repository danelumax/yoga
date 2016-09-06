import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance


class ValidateNetworkTask(object):
    '''
    Check Network Connection
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def precheck(self):
        pass
    
    
    def execute(self):
        log._file.debug(">> Check network connection Begin")
        cfg = cfgInstance()
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._check_network(cfg.getPsCfg(0))
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._check_network(cfg.getSsCfg(0))
            self._check_network(cfg.getPsCfg(0))
            self._check_network(cfg.getPsCfg(1))
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._check_network(cfg.getSsCfg(0))
            self._check_network(cfg.getPsCfg(0))
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            for ss_cfg in cfg.getSsCfgList() :
                self._check_network(ss_cfg)
            for ps_cfg in cfg.getPsCfgList() :
                self._check_network(ps_cfg)
        log._file.debug("<< Check network connection End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def _check_network(self, node_cfg):
        log._file.debug("Connect host: " + node_cfg.getHostName())
        sshMgr = sshManagerInstance()
        try :
            ssh = sshMgr.connect(node_cfg.getHostName(), node_cfg.getOamIp(), node_cfg.getSshPort(), node_cfg.getUserName(), node_cfg.getPassword())
        except :
            print
            print common.print_red("Node Information(username & password) is Incorrect, please Execute again and Enter correct information")
            common.cleanNodeInfo()
            raise
        common.saveNodeInfo(node_cfg.getHostName(), node_cfg.getOamIp(), node_cfg.getUserName(), node_cfg.getPassword())






