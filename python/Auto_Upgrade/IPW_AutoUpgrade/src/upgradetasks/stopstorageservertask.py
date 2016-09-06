import os,re,subprocess 
import log, common
import ipwutils


class StopStorageServerTask(object) :
    """
    Stop Storage Server
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopStorageServerTask Begin")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_ENTRY2,common.g_ipw_mode) :  # single/entry1/entry2
            ipwutils.stopSS(cfg)
            ipwutils.stopInnodb(cfg)
            ipwutils.stopTomcat(cfg)
        elif not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            ipwutils.stopSSResource(cfg)
        log._file.debug("<< StopStorageServerTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to stop SS manually:")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
           or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            helpinfo='''
            1. Stop the group-ipwss on SS1 or SS2.
            # crm_resource -r group-ipwss -p target-role -v stopped --meta

            2. Ensure that the resource group is stopped.
            # crm_mon -1
            '''
        else:
            helpinfo='''
            1. Stop the Storage Server process.
            # /etc/init.d/ipworks.ss stop
            Ensure that Storage Server process is stopped.
            # ps -ef | grep -v grep | grep ipwss

            2. Stop the MySQL process.
            # /etc/init.d/ipworks.mysql stop
            Ensure that MySQL process is stopped.
            # ps -ef | grep -v grep | grep mysql

            3. Stop the Tomcat servlet engine.
            # /etc/init.d/ipworks.tomcat start
            Ensure that Tomcat servlet engine is stopped.
            # ps -ef | grep -v grep | grep org.apache.juli
            '''
        log._print.info(helpinfo)
        pass 

