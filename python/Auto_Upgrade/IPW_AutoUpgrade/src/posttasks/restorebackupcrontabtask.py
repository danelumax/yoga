import os,re,subprocess 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class RestoreBackupCrontabTask(object) :
    """
    Restore Backup Crontab
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self):
        log._file.debug(">> RestoreBackupCrontabTask Begin")

        cfg_list = common.getNodeList(cfgInstance())
        for host in cfg_list:
            self._restoreBackupCronJob(host)

        log._file.debug("<< RestoreBackupCrontabTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to restore backup cron job manually:")
        helpinfo='''
        1. Check 'Enable.Scheduling' in /etc/ipworks/ipworks_backup.conf.
        # grep "^Enable.Scheduling" /etc/ipworks/ipworks_backup.conf

        2. If the value is '1', enable backup cron job.
        # /opt/ipworks/IPWbackup/scripts/updatecrontab 1
        '''
        log._print.info(helpinfo)
        pass

    def _restoreBackupCronJob(self, host):
        log._file.debug(">>> Begin to restore backup cron job on host " + host.getHostName())
        cmd = 'enable=`grep "^Enable.Scheduling" /etc/ipworks/ipworks_backup.conf | cut -d= -f2`;/opt/ipworks/IPWbackup/scripts/updatecrontab $enable'
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        log._file.debug("Restore backup cron job Succeed!")

