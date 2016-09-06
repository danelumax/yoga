import os,re,subprocess 
import log, common
import ipwutils

class StopNDBDataNodeTask(object) :
    """
    Stop NDB Data Node 
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopNDBDataNodeTask Begin")
        ipwutils.stopDataNode(cfg)
        log._file.debug("<< StopNDBDataNodeTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to stop Data Node manually:")
        helpinfo='''
        Stop Data Node with control panel.
        # ipwscp
        Select MySQL Cluster Node > Data Node > Stop.
        '''
        log._print.info(helpinfo)
        pass


