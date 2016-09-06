import os,re,subprocess 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class MigrateInnoDBDataTask(object) :
    """
    Migrate InnoDB Data
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> MigrateInnoDBDataTask Begin")
        self._migrateData(cfg)
        log._file.debug("<< MigrateInnoDBDataTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def _migrateData(self, host):
        log._file.debug(">> Migrate Innodb Data begin on host " + host.getHostName())
        cmd = "cd " + cfgInstance().getMountPoint() + "/x86-linux/utils/;./ipwmigrate_for_update -d /tmp/"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Migration process Completed successfully", res)
        if not result:
            log._file.error("Migrate Innodb Data Failed")
            raise Exception("Migrate Innodb Data  Failed")
        log._file.debug("Migrate Innodb Data Succeed!")
        log._file.debug("<< Migrate Innodb Data end")

    def help(self):
        log._print.info("Please ensure Innodb is running before migrate data")
        log._print.info("If migrate fail, please check messages in log: /var/ipworks/logs/ipworks_upgrade_migrate.log")
        pass
        

