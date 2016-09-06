import os,re,subprocess
import log, common
import ipwutils


class StopNDBClusterTask(object) :
    """
    Stop NDB Cluster 
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopNDBClusterTask Begin")
        ipwutils.stopSQLNode(cfg)
        ipwutils.stopNDBCluster(cfg)
        log._file.debug("<< StopNDBClusterTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to stop NDB Cluster manually:")
        helpinfo='''
        Stop NDB Cluster with control panel.
        # ipwscp
        Select MySQL Cluster Node > Management Node > Cluster Shutdown.
        '''
        log._print.info(helpinfo)
        pass

