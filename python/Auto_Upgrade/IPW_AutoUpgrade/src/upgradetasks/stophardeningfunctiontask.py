import os,re,subprocess 
import log, common
import ipwutils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class StopHardeningFunctionTask(object) :
    """
    Stop Hardening Function
    """

    stopHandeningTaskDict = {}
    _hostname = ""

    def __init__(self) :
        #single
        self.stopHandeningTaskDict[(common.C_IPW_MODE_SINGLE, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_PS)] \
        = self._closeInnodbAndTomcatChroot
        
        #entry1
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_DHCP, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot
        
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_PS)] \
        = self._closeSQLNodeChroot        
         
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_AAA, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbTomcatAndSQLNodeChroot
        
        #entry2
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbTomcatAndSQLNodeChroot

        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_DHCP, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot
                
        self.stopHandeningTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_PS)] \
        = self._closeSQLNodeChroot
        

        
        #medium1 
        self.stopHandeningTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_DNS, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot
        self.stopHandeningTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot           

        self.stopHandeningTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_PS)] \
        = self._closeSQLNodeChroot        
         
        self.stopHandeningTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_DHCP, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot

        self.stopHandeningTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_AAA, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbTomcatAndSQLNodeChroot
                
        #medium2 
        self.stopHandeningTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_CLF, common.C_IPW_HOSTROLE_SS)] \
        = self._closeInnodbAndTomcatChroot        
        


    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopHardeningFunctionTask Begin")
        self._hostname = cfg.getHostName()
        
        searchKey = (common.g_ipw_mode, common.g_upgrade_app, cfg.getHostRole())
        
        if searchKey in self.stopHandeningTaskDict:
            ipwutils.mountShareDir(cfg)
            execFun = self.stopHandeningTaskDict[searchKey]
            execFun(cfg);
            ipwutils.unmountShareDir(cfg)
        else:
            log._file.debug("not found executable function for host %s",  cfg.getHostName())
            
        log._file.debug("<< StopHardeningFunctionTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def _closeInnodbAndTomcatChroot(self,hostCfg):
        log._file.debug("<< _closeInnodbAndTomcatChroot Begin")
        isHAMode = False
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
            or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            isHAMode = True
        
        ret = self._isTomcatChrootStart(hostCfg)
        if ret:
            self._stopTomcatChroot(hostCfg, isHAMode)
            
        ret = self._isInnodbChrootStart(hostCfg)
        if ret:
            self._stopInnodbChroot(hostCfg, isHAMode)
        log._file.debug("<< _closeInnodbAndTomcatChroot End")

        
    def _closeInnodbTomcatAndSQLNodeChroot(self,hostCfg):
        log._file.debug("<< _closeInnodbTomcatAndSQLNodeChroot Begin")
        isHAMode = False
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
            or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            isHAMode = True
        
        ret = self._isTomcatChrootStart(hostCfg)
        if ret:
            self._stopTomcatChroot(hostCfg, isHAMode)
        ret = self._isInnodbChrootStart(hostCfg)
        if ret:
            self._stopInnodbChroot(hostCfg, isHAMode)
        ret = self._isSqlNodeChrootStart(hostCfg)
        if ret:
            self._stopSqlNodeChroot(hostCfg, isHAMode)
        log._file.debug("<< _closeInnodbTomcatAndSQLNodeChroot End")
        
    def _closeSQLNodeChroot(self,hostCfg,isHAMode=False):
        log._file.debug("<< _closeSQLNodeChroot Begin")
        ret = self._isSqlNodeChrootStart(hostCfg)
        if ret:
            self._stopSqlNodeChroot(hostCfg)
        log._file.debug("<< _closeSQLNodeChroot End")
        

    def _isTomcatChrootStart(self, hostCfg):
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
        result = re.search("Tomcat now in chroot configuration", res)
        return result

    def _isInnodbChrootStart(self, hostCfg):
        log._file.debug(">>> Begin to check Innodb Chroot status on host " + hostCfg.getHostName())
        cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_innodb_env status"
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Mysql innodb now in chroot configuration", res)
        return result
    
    def _isSqlNodeChrootStart(self, hostCfg):
        log._file.debug(">>> Begin to check NDB SQLNode Chroot status on host " + hostCfg.getHostName())
        cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_sqlnode_env status"
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Mysql sqlnode now in chroot configuration", res)
        return result

    def _stopTomcatChroot(self, hostCfg,isHAMode=False):
        log._file.debug(">>> Begin to stop Tomcat Chroot on host " + hostCfg.getHostName())
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        cmd = ""
        if isHAMode :
            ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
            cmd = "python ConfigHAChrootEnv.py --chroot_type=%s --chroot_action=%s --slave_password=%s" \
            %("tomcat", "stop", cfgInstance().getStandBySS().getPassword())
        else:
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_tomcat_env stop"
        
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("stop chroot tomcat sucessfully", res)
        if not result:
            log._file.error("Stop Tomcat Chroot Failed")
            raise Exception("Stop Tomcat Chroot Failed")
        log._file.debug("Stop Tomcat Chroot Succeed!")

    def _stopInnodbChroot(self, hostCfg,isHAMode=False):
        log._file.debug(">>> Begin to stop Innodb Chroot on host " + hostCfg.getHostName())
        cmd = ""
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        
        if isHAMode :
            ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
            cmd = "python ConfigHAChrootEnv.py --chroot_type=%s --chroot_action=%s --slave_password=%s" \
            %("innodb", "stop", cfgInstance().getStandBySS().getPassword())
        else:
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_innodb_env stop"
        
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("stop chroot innodb successfully", res)
        if not result:
            log._file.error("Stop Innodb Chroot Failed")
            raise Exception("Stop Innodb Chroot Failed")
        log._file.debug("Stop Innodb Chroot Succeed!")

    def _stopSqlNodeChroot(self, hostCfg,isHAMode=False):
        log._file.debug(">>> Begin to stop SQL Node Chroot on host " + hostCfg.getHostName())
        cmd = ""
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        
        if isHAMode :
            ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
            cmd = "python ConfigHAChrootEnv.py --chroot_type=%s --chroot_action=%s --slave_password=%s" \
            %("sqlnode", "stop", cfgInstance().getStandBySS().getPassword())
        else:
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_sqlnode_env stop"
       
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("stop chroot sqlnode successfully", res)
        if not result:
            log._file.error("Stop Mysql sqlnode  Chroot Failed")
            raise Exception("Stop Mysql sqlnode  Chroot Failed")
        log._file.debug("Stop Innodb Chroot Succeed!")



    def help(self):
	log._print.info("")
        log._print.info("    Please refer the following steps to manually fix it on host '%s':" %(self._hostname))
        helpinfo='''
        Use below command to stop the Chroot enviroment if the hardening function is enabled, either for MySQL Innodb or Tomcat
        #chroot_innodb_env stop
        #chroot_tomcat_env stop
        
        Use below command for ensure that the Chroot environment is disabled:
        #chroot_innodb_env status
        #chroot_tomcat_env status
        '''
        log._print.info(helpinfo)

        pass

