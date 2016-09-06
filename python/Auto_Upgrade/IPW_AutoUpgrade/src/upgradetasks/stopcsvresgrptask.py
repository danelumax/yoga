import os,re,subprocess 
import log, common
import ipwutils


class StopCsvResGrpTask(object) :
    """
    Stop CSV Engine Resource Group
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopCsvResGrpTask Begin")

        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA :
            ipwutils.stopCsvResource(cfg)

        log._file.debug("<< StopCsvResGrpTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to stop csv engine resource group manually:")
        helpinfo='''
        1. Stop csv engine resource group.
        # crm_resource -r group-csvengine -p target-role -v stopped --meta

        2. Check if the resource is stopped.
        # crm_mon -1
        '''
        log._print.info(helpinfo)
        pass


