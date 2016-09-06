import log
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class OptimizePerformanceTask(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    def precheck(self):
        pass
    
    
    def execute(self):
        log._all.debug(">>> Optimize Performance Begin")
        for cfg in cfgInstance.getSsCfgList() :
            self._optimize(cfg)
        for cfg in cfgInstance.getPsCfgList() :
            self._optimize(cfg)
        log._all.debug("<<< Optimize Performance End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def _optimize(self, cfg) :
        log._all.debug("Optimize system performace on " + cfg.getHostName())
        content = common.open_file("src/template/sysctl.conf.tmp")
        common.create_file(cfg, content, '/etc/', 'sysctl.conf')
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("sysctl -p")




