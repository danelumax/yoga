import os,re,subprocess
import log, common
import ipwutils

from hautil import hautilInstance


class StartSQLNodeTask(object) :
    """
    Start SQL Node
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartSqlNodeTask Begin")

        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA :
            ipwutils.startSQLResource(cfg)
        else :
            ipwutils.startSqlNode(cfg)

        log._file.debug("<< StartSqlNodeTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to start SQL Node manually:")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          and common.g_isInstall_AAA :
            helpinfo='''
            1. Start SQL Node resource group.
            # crm_resource -r group-sqlnode -p target-role -v started --meta

            2. Ensure that the resource group is started.
            # crm_mon -1
            '''
        else:
            helpinfo='''
            Start SQL Node with control panel.
            # ipwscp
            Select MySQL Cluster Node > SQL Node > Start.
            '''
        log._print.info(helpinfo)
        pass

