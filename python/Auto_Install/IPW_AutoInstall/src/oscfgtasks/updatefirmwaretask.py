import log
from cfg import cfgInstance
from sshmanager import sshManagerInstance


class UpdateFirmwareTask(object):
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
        log._all.debug(">>> Update Firmware Start")
        log._all.debug("<<< Update Firmware End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass









