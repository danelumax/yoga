import os,re,subprocess 
import log, common
import ipwutils


class StartStorageServerTask(object) :
    """
    Start Storage Server
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartStorageServerTask Begin")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_ENTRY2,common.g_ipw_mode) :  # single/entry1/entry2
            ipwutils.startSS(cfg)
            ipwutils.startTomcat(cfg)
        elif not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            ipwutils.startSSResource(cfg)
        log._file.debug("<< StartStorageServerTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to start SS manually:")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
           or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            helpinfo='''
            1. Bring the resource group online on SS1 or SS2.
            # crm_resource -r group-ipwss -p target-role -v started --meta

            2. Ensure that the resource group is started.
            # crm_mon -1

            Note:  
            If the MySQL resource group fails to start, refer to Section Fail to Start MySQL Resource in IPWorks Troubleshooting Guideline to check and fix the error.
            '''
        else:
            helpinfo='''
            1. Restart the Storage Server process.
            # /etc/init.d/ipworks.ss start

            2. Restart the Tomcat servlet process.
            # /etc/init.d/ipworks.tomcat start
            '''
        log._print.info(helpinfo)
        pass

