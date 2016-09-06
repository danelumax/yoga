import os,re,subprocess 
import log, common
import ipwutils


from hautil import hautilInstance

class StopMgmNodeTask(object) :
    """
    Stop Mgm Node
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopMgmNodeTask Begin")

        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA :
            ipwutils.stopMgmResource(cfg)
        else :
            ipwutils.stopMgmNode(cfg)

        log._file.debug("<< StopMgmNodeTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to stop Mgm Node manually:")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA :
            helpinfo='''
            1. Stop mgm resource group.
            # crm_resource -r group-mgmnode -p target-role -v stopped --meta

            2. Ensure that the resource group is stopped.
            # crm_mon -1
            '''
        else :
            helpinfo='''
            Stop Mgm Node with control panel.
            # ipwscp
            Select MySQL Cluster Node > Management Node > Stop.
            '''
        log._print.info(helpinfo)
        pass 

