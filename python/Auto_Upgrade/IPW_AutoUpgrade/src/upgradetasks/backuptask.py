import os,re,subprocess 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class BackupTask(object) :
    """
    Back Up 
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> BackupTask Begin")
        self._checkInnodbStatus(cfg)
        self._backup(cfg)
        log._file.debug("<< BackupTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def _checkInnodbStatus(self, host):
        log._file.debug(">> Begin to check Innodb status on host " + host.getHostName())
        cmd = "ps -ef | grep -v grep | grep innodbnode"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd, p_err=False, throw=False)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("ipworks_innodbnode_my", res)
        if not result:
            log._file.error("Innodb not running, cannot backup")
            raise Exception("Innodb not running, cannot backup")
        log._file.debug("Innodb is running")

    def _backup(self, host):
        log._file.debug(">> backup begin on host " + host.getHostName())
        cmd = "rm -rf /tmp/ipwbackup*.tar.gz;" + cfgInstance().getMountPoint() + "/x86-linux/utils/ipwbackup" 
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("File Created", res)
        if not result:
            log._file.error("Backup Failed")
            raise Exception("Backup Failed")
        log._file.debug("Backup Succeed!")
        log._file.debug("<< backup end")

    def help(self):
        log._print.info("Please ensure Innodb is running before backup.")
        log._print.info("If backup fail, please check messages in log: /var/ipworks/logs/ipworks_backup.log")
        pass


