import log
from cfg import cfgInstance
from sshmanager import sshManagerInstance


class ReorderNetworkCardTask(object):
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
        log._all.debug(">>> Reorder Network Card Start")
        log._all.debug("<<< Reorder Network Card End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass








