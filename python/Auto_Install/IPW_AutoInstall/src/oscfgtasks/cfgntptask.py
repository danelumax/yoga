import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class CfgNtpTask(object):
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
        log._all.debug(">>> Config NTP Begin")
        if cfgInstance.getNtpServer() :
            for cfg in cfgInstance.getSsCfgList() :
                self._configNtp(cfg)
            for cfg in cfgInstance.getPsCfgList() :
                self._configNtp(cfg)
        else :
            log._all.debug("Don't exist NTP server")
        log._all.debug("<<< Config NTP End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def _configNtp(self, cfg) :
        log._all.debug("Config NTP on " + cfg.getHostName())
        content = common.open_file("src/template/ntp.conf.tmp")
        content = content.replace("<NTP_SERVER>", cfgInstance.getNtpServer())
        common.create_file(cfg, content, '/etc/', 'ntp.conf')
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("chkconfig ntp on")
        ssh_util.remote_exec("service ntp restart")
        ssh_util.remote_exec("service ntp status")




