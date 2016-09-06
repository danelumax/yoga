import log
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class CfgRoutingTask(object):
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
        log._all.debug(">>> Config Default Route Begin")
        if cfgInstance.getDefaultGw() :
            for cfg in cfgInstance.getSsCfgList() :
                self._addRoute(cfg)
            for cfg in cfgInstance.getPsCfgList() :
                self._addRoute(cfg)
        else :
            log._all.debug("Don't exist default gateway")
        log._all.debug("<<< Config Default Route End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def _addRoute(self, cfg) :
        log._all.debug("Add default route on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        tt = "default %s - -" %cfgInstance.getDefaultGw()
        cmd = "echo %s >/etc/sysconfig/network/routes"
        ssh_util.remote_exec(cmd)
        ssh_util.remote_exec("service network restart")
        ssh_util.remote_exec("route |grep default")







