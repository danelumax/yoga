import os,re,subprocess 
import log, common
import ipwutils

class MoveClfResourceTask(object) :
    """
    Move Clf Resource Group
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> MoveClfResourceTask Begin")
	ipwutils.moveClfResource(cfg)
        log._file.debug("<< MoveClfResourceTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to move CLF resource manually:")
        helpinfo='''
        1. Move CLF Resource to the other PS.
        Note: This step expects 30 seconds traffic down.

        # crm_resource -r group-clf -M -N <hostname>

        2. Check if the resource is started on the other PS.
        # crm_mon -1
        '''
        log._print.info(helpinfo)
        pass


