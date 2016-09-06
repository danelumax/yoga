import log
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class StartIpmiTask(object):
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
        log._all.debug(">>> Start IPMI Begin")
        for cfg in cfgInstance.getSsCfgList() :
            self._startIpmi(cfg)
        for cfg in cfgInstance.getPsCfgList() :
            self._startIpmi(cfg)
        log._all.debug("<<< Start IPMI End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass



    def _startIpmi(self, cfg) :
        log._all.debug("Start IPMI on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("chkconfig -a ipmi")
        ssh_util.remote_exec("/etc/init.d/ipmi start")
        ssh_util.remote_exec("/etc/init.d/ipmi status")




