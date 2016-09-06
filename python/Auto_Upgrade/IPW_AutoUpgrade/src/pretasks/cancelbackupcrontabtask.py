#! /usr/bin/python
import os
import log, common
import time

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class CancelBackupCrontabTask(object):
    '''
    Cancel Backup Crontab 
    '''


    def __init__(self):
        pass
        
        
    def precheck(self):
        pass

    
    def execute(self):
        log._file.debug(">> CancelBackupCrontabTask Begin")

        cfg_list = common.getNodeList(cfgInstance())
        for host in cfg_list:
            self._disableBackupCronJob(host)

        log._file.debug("<< CancelBackupCrontabTask End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass

	
    def _disableBackupCronJob(self, host):
        log._file.debug(">>> Begin to disable backup cron job on host " + host.getHostName())
        cmd = "/opt/ipworks/IPWbackup/scripts/updatecrontab 0"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        log._file.debug("Disable backup cron job Succeed!")
 
    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to disable backup cron job manually:")
        helpinfo='''
        # /opt/ipworks/IPWbackup/scripts/updatecrontab 0
        '''
        log._print.info(helpinfo)
        pass

