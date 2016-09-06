import os,re,subprocess 
import log, common
import ipwutils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class SetInnodbTomcatChrootTask(object) :
    """
    Set Innodb & Tomcat Chroot Env Function.
    """

    SetInnodbTomcatChrootTaskDict = {}
    _hostname = ""

    def __init__(self) :
        #single
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_SINGLE, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_PS)] \
        = self._setInnodbAndTomcatChroot
        
        #entry1
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChroot
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChroot
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_DHCP, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChroot
        
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_AAA, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChroot
        
        #entry2
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChroot
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChroot
        
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_DHCP, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChroot
        
        
        #medium1 
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChrootWithHA
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChrootWithHA
                   
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_DHCP, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChrootWithHA

        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_AAA, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChrootWithHA
                
        #medium2 
        self.SetInnodbTomcatChrootTaskDict[(common.C_IPW_MODE_MEDIUM2, common.C_IPW_APP_CLF, common.C_IPW_HOSTROLE_SS)] \
        = self._setInnodbAndTomcatChrootWithHA             
        


    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> SetInnodbTomcatChrootTask Begin")
        self._hostname = cfg.getHostName()
        
        if not common.g_isChangeRoot :
            log._file.debug("<< no need set Choot Env, exit SetInnodbTomcatChrootTask")
            return
        
        searchKey = (common.g_ipw_mode, common.g_upgrade_app, cfg.getHostRole())
        
        if searchKey in self.SetInnodbTomcatChrootTaskDict:
            execFun = self.SetInnodbTomcatChrootTaskDict[searchKey]
            execFun(cfg);
        else:
            log._file.debug("not found executable function for host %s",  cfg.getHostName())
            
        log._file.debug("<< SetInnodbTomcatChrootTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def _setInnodbAndTomcatChroot(self,hostCfg):
        log._file.debug("<< _setInnodbAndTomcatChroot Begin")
        
        ret = self._isTomcatChrootStop(hostCfg)
        if ret:
            self._startTomcatChroot(hostCfg)
            
        ret = self._isInnodbChrootStop(hostCfg)
        if ret:
            self._startInnodbChroot(hostCfg)
        log._file.debug("<< _setInnodbAndTomcatChroot End")

    def _setInnodbAndTomcatChrootWithHA(self,hostCfg):
        log._file.debug("<< _setInnodbAndTomcatChroot Begin")
        ipwutils.mountShareDir(hostCfg)
        ret = self._isTomcatChrootStop(hostCfg)
        if ret:
            self._startTomcatChroot(hostCfg, True)
            
        ret = self._isInnodbChrootStop(hostCfg)
        if ret:
            self._startInnodbChroot(hostCfg, True)
            
        ipwutils.unmountShareDir(hostCfg)
        log._file.debug("<< _setInnodbAndTomcatChroot End")


    def _isTomcatChrootStop(self, hostCfg):
        log._file.debug(">>> Begin to check Tomcat Chroot status on host " + hostCfg.getHostName())
        cmd = "rpm -q IPWtomcat"
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd, p_err=False, throw=False)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("IPWtomcat", res)
        if not result:
            return result
        cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_tomcat_env status"
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Tomcat now in normal configuration", res)
        return result

    def _isInnodbChrootStop(self, hostCfg):
        log._file.debug(">>> Begin to check Innodb Chroot status on host " + hostCfg.getHostName())
        cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_innodb_env status"
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Mysql innodb now in normal configuration", res)
        return result
    

    def _startTomcatChroot(self, hostCfg, isHAMode=False):
        log._file.debug(">>> Begin to start Tomcat Chroot on host " + hostCfg.getHostName())
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        cmd = ""

        if isHAMode :
            ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
            cmd = "python ConfigHAChrootEnv.py --chroot_type=%s --chroot_action=%s --slave_password=%s" \
            %("tomcat", "start", cfgInstance().getStandBySS().getPassword())
        else:
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_tomcat_env start"

        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("set chroot tomcat successfully", res)
        if not result:
            log._file.error("start Tomcat Chroot Failed")
            raise Exception("start Tomcat Chroot Failed")
        log._file.debug("Stop Tomcat Chroot Succeed!")
        
                

    def _startInnodbChroot(self, hostCfg,isHAMode=False):
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        cmd = ""

        if isHAMode :
            ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
            cmd = "python ConfigHAChrootEnv.py --chroot_type=%s --chroot_action=%s --slave_password=%s" \
            %("innodb", "start", cfgInstance().getStandBySS().getPassword())
        else:
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_innodb_env start"
            
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Chroot mysql innodb successfully", res)
        if not result:
            log._file.error("Start Innodb Chroot Failed")
            raise Exception("Start Innodb Chroot Failed")
        log._file.debug("Start Innodb Chroot Succeed!")



    def help(self):
	log._print.info("")
        log._print.info("    Please refer the following steps to manually fix it on host '%s':" %(self._hostname))
        
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
           or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            helpinfo='''
            To harden the MySQL InnoDB and Tomcat Server with HA:
            1. Make sure IPWorks tomcat server, Storage server and MySQL Innodb is stop
            #crm_mon -1
            #crm_resource -r group-ipwss -p target-role -v stopped --meta
            
            2. If the diskarray mode is nfs, might need to mount some directory temporarily.
            #mount /global/ipworks
            
            3. Set up the MySQL InnoDB and Tomcat Chroot environments
            #chroot_innodb_env start
            #chroot_tomcat_env start
            
            4. Use below command for ensure that the Chroot environment is enabled:
            #chroot_innodb_env status
            #chroot_tomcat_env status
            
            5. If the diskarray mode is nfs, remember umount the share directory
            #umount /global/ipworks
            '''
        else:        
            helpinfo='''
            To harden the MySQL InnoDB and Tomcat Server without HA:
            1. Make sure IPWorks tomcat server, Storage server and MySQL Innodb is stop
            
            2. Set up the MySQL InnoDB and Tomcat Chroot environments 
            #chroot_innodb_env start
            #chroot_tomcat_env start
            
            3. Use below command for ensure that the Chroot environment is enabled:
            #chroot_innodb_env status
            #chroot_tomcat_env status
            '''
        log._print.info(helpinfo)
        pass

