import log
from cfg import cfgInstance
from sshmanager import sshManagerInstance


class RebootOSTask(object):
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
        log._all.debug(">>> Reboot OS Start")
        log._all.debug("<<< Reboot OS End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass









