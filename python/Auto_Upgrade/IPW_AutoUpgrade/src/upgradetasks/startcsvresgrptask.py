import os,re,subprocess 
import log, common
import ipwutils

from cfg import cfgInstance

class StartCsvResGrpTask(object) :
    """
    Start CSV Engine Resource Group
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartCsvResGrpTask Begin")

        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA \
          and cfgInstance().getHaCfg().useCsvGrp() :
            ipwutils.startCsvResource(cfg)

        log._file.debug("<< StartCsvResGrpTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to start csv engine resource group manually:")
        helpinfo='''
        1. Start csv engine resource group.
        # crm_resource -r group-csvengine -p target-role -v started --meta

        2. Check if the resource is started.
        # crm_mon -1
        '''
        log._print.info(helpinfo)
        pass


