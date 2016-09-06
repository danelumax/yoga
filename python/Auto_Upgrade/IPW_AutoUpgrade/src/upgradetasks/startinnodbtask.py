import os,re,subprocess 
import log, common
import ipwutils


class StartInnoDBTask(object) :
    """
    Start InnoDB 
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartInnoDBTask Begin")
        ipwutils.startInnodb(cfg)
        log._file.debug("<< StartInnoDBTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to start Innodb manually:")
        helpinfo='''
        # /etc/init.d/ipworks.mysql start-master-innodb
        '''
        log._print.info(helpinfo)
        pass
