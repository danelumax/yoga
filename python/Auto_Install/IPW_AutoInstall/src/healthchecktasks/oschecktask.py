import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from healthcheckinfo import healthcheckInstance


class OsCheckTask(object):
    '''
    Check OS Version
    '''

    def __init__(self):
        self._os_version = ''
        self._os_patchlevel = ''
        self._kernal_version = ''

    def precheck(self):
        pass


    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def execute(self):
        log._file.debug(">> OS Version Check Begin") 
        if not healthcheckInstance().getOsVersion() and not healthcheckInstance().getOsPatchLevel():
            log._file.info("No need to Check OS Version, Because OS Version doesn't Configured.")
            return
        cfg_list = common.getNodeList(cfgInstance())
        for host in cfg_list:
            self._checkosversion(host)
        expValue = "SuSE %s  SP %s" %(self._os_version, self._os_patchlevel)
        common.save_healthcheck_info("OS Version", expValue, expValue, "OK")
        if not healthcheckInstance().getKernalVersion():
            log._file.info("No need to Check Kernal Version, Because Kernal Version doesn't Configured.")
            return
        for host in cfg_list:
            self._checkKernalVersion(host)
        common.save_healthcheck_info("Kernal Version", self._kernal_version, self._kernal_version, "OK")
        log._file.debug("<< OS Version Check End") 


    def _checkosversion(self, host):
        log._file.debug(">>> Begin to check os version on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        command = 'cat /etc/SuSE-release'
        res,r_code = ssh_util.remote_exec(command)
        self._os_version = ''
        self._os_patchlevel = ''
        lines = res.split('\n')
        for line in lines:
            if re.search('VERSION =', line):
                log._file.info('Find OS version: ' + line)
                self._os_version = line.split('=')[1].strip()
                continue
            if re.search('PATCHLEVEL =', line):
                log._file.info('Find OS patchlevel: ' + line)
                self._os_patchlevel = line.split('=')[1].strip()
        if not self._os_version or not self._os_patchlevel:
            log._file.error("Can't find OS version: %s, Patchlevel: %s" %(self._os_version, self._os_patchlevel))
            raise Exception("Os version is not find! Please Check!")
        if cmp(self._os_version, healthcheckInstance().getOsVersion()) \
          or cmp(self._os_patchlevel, healthcheckInstance().getOsPatchLevel()):
            errinfo = 'Exp OS Version: %s, Patchlevel: %s, Real OS Version: %s, Patchlevel: %s' %(healthcheckInstance().getOsVersion(), healthcheckInstance().getOsPatchLevel(), self._os_version, self._os_patchlevel)
            log._file.error("OS version is incorrect: \n%s" %(errinfo))
            raise Exception("Os version is Incorrect! Please Check!")
        log._file.debug("<<<")


    def _checkKernalVersion(self, host):
        log._file.debug(">>> Begin to check kernal version on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec('uname -r')
        lines = res.split('\n')
        expvalue = healthcheckInstance().getKernalVersion()
        isFind = False
        self._kernal_version = lines[1]
        for line in lines:
            if re.search(expvalue, line):
                log._file.info('Find Kernal version: ' + line)
                self._kernal_version = line
                isFind = True
                break
        if not isFind:
            errinfo = "Exp Kernal Version: %s, Real Version: %s" %(expvalue, self._kernal_version)
            raise Exception("Kernal version is Incorrect! %s" %(errinfo))
        log._file.debug("<<< End to check kernal version")


