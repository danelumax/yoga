import os,re,subprocess
import log, common
import ipwutils


class StartMgmNodeTask(object) :
    """
    Start MGM Node
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartMgmNodeTask Begin")

        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA :
            ipwutils.startMgmResource(cfg)
        else :
            ipwutils.startMgmNode(cfg)
                
        log._file.debug("<< StartMgmNodeTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to start Mgm Node manually:")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA :
            helpinfo='''
            1. Start mgm resource group.
            # crm_resource -r group-mgmnode -p target-role -v started --meta

            2. Ensure that the resource group is started.
            # crm_mon -1
            '''
        else :
            helpinfo='''
            Start Mgm Node with control panel.
            # ipwscp
            Select MySQL Cluster Node > Management Node > Start.
            '''
        log._print.info(helpinfo)
        pass

