import os,re,subprocess
import log, common
import ipwutils

class StartDataNodeTask(object) :
    """
    Start DATA Node
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartDataNodeTask Begin")
        ipwutils.startDataNode(cfg)
        ipwutils.checkDataNode(cfg)
        log._file.debug("<< StartDataNodeTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to start DataNode manually:")
        helpinfo='''
        1. Start Data Node with control panel.
        # ipwscp
        Select MySQL Cluster Node > Data Node > Start Initial and press y.
        Go to the Control Panel Main Screen, check if the status of Data Node is "running".

        If DataNode cannot be started, please check your configuration and system enviorment.
        For example, memory size, disk space...

        If DataNode is "starting", please wait until it become "running".
        The duration may take time depends on the size of user data.
        '''
        log._print.info(helpinfo)
        pass
