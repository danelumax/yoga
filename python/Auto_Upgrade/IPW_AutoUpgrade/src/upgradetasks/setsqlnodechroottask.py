import os,re,subprocess 
import log, common
import ipwutils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class SetSqlNodeChrootTask(object) :
    """
    Set NDB SQL Node Chroot Env Function
    """

    setSqlNodeChrootTaskDict = {}
    _hostname = ""

    def __init__(self) :
        
        #entry1
        self.setSqlNodeChrootTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_PS)] \
        = self._setSQLNodeChroot        
         
        self.setSqlNodeChrootTaskDict[(common.C_IPW_MODE_ENTRY1, common.C_IPW_APP_AAA, common.C_IPW_HOSTROLE_SS)] \
        = self._setSQLNodeChroot
        
        #entry2
        self.setSqlNodeChrootTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_SS)] \
        = self._setSQLNodeChroot

        self.setSqlNodeChrootTaskDict[(common.C_IPW_MODE_ENTRY2, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_PS)] \
        = self._setSQLNodeChroot
        
        #medium1 
        self.setSqlNodeChrootTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_ENUM, common.C_IPW_HOSTROLE_PS)] \
        = self._setSQLNodeChroot      
         
        self.setSqlNodeChrootTaskDict[(common.C_IPW_MODE_MEDIUM1, common.C_IPW_APP_AAA, common.C_IPW_HOSTROLE_SS)] \
        = self._setSQLNodeChrootWithHA
        


    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> SetSqlNodeChrootTask Begin")
        self._hostname = cfg.getHostName()
        if not common.g_isChangeRoot :
            log._file.debug("<< no need set Choot Env, exit SetSqlNodeChrootTask")
            return
        
        searchKey = (common.g_ipw_mode, common.g_upgrade_app, cfg.getHostRole())
        
        if searchKey in self.setSqlNodeChrootTaskDict:
            execFun = self.setSqlNodeChrootTaskDict[searchKey]
            execFun(cfg);
        else:
            log._file.debug("not found executable function for host %s",  cfg.getHostName())
            
        log._file.debug("<< SetSqlNodeChrootTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass


    def _setSQLNodeChroot(self,hostCfg):
        log._file.debug("<< _setSQLNodeChroot Begin")
        ret = self._isSqlNodeChrootStop(hostCfg)
        if ret:
            self._startSqlNodeChroot(hostCfg)
        log._file.debug("<< _setSQLNodeChroot End")
        
    def _setSQLNodeChrootWithHA(self,hostCfg):
        log._file.debug("<< _setSQLNodeChroot Begin")
        
        self._mountShareSQLNodeDir(hostCfg, True)
        ret = self._isSqlNodeChrootStop(hostCfg)
        if ret:
            self._startSqlNodeChroot(hostCfg, True)
        log._file.debug("<< _setSQLNodeChroot End")
        self._mountShareSQLNodeDir(hostCfg, False)
        

    
    def _isSqlNodeChrootStop(self, hostCfg):
        log._file.debug(">>> Begin to check NDB SQLNode Chroot status on host " + hostCfg.getHostName())
        cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_sqlnode_env status"
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Mysql sqlnode now in normal configuration", res)
        return result


    def _startSqlNodeChroot(self, hostCfg, isHAMode=False):
        log._file.debug(">>> Begin to start SQL Node Chroot on host " + hostCfg.getHostName())
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        cmd = ""
        if isHAMode :
            ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
            cmd = "python ConfigHAChrootEnv.py --chroot_type=%s --chroot_action=%s --slave_password=%s" \
            %("sqlnode", "start", cfgInstance().getStandBySS().getPassword())
        else:
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_sqlnode_env start"

        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
        result = re.search("Chroot mysql sqlnode successfully", res)
        if not result:
            log._file.error("Start Mysql sqlnode  Chroot Failed")
            raise Exception("Start Mysql sqlnode  Chroot Failed")
        log._file.debug("Start Innodb Chroot Succeed!")


    def _mountShareSQLNodeDir(self, hostCfg, isMount=True):
        cmd = ""
        if isMount:
            cmd = "mount /global/sqlnode"
        else:
            cmd = "umount /global/sqlnode"
        ssh = sshManagerInstance().getSsh(hostCfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)

    def help(self):
        log._print.info("")
        log._print.info("    Please refer the following steps to manually fix it on host '%s':" %(self._hostname))
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
            and not cmp(common.C_IPW_APP_AAA, common.g_upgrade_app) :
            helpinfo='''
            To harden the MySQL NDB with HA:
            1. Make sure IPWorks NDB SQL node is stop
            #crm_mon -1
            #crm_resource -r group-sqlnode -p target-role -v stopped --meta
            
            2. If the diskarray mode is nfs, might need to mount some directory temporarily.
            #mount /global/sqlnode
            
            3. Set up the MySQL SQL node Chroot environments
            #chroot_sqlnode_env start
            
            4. Use below command for ensure that the Chroot environment is enabled:
            #chroot_sqlnode_env status
            
            5. If the diskarray mode is nfs, remember umount the share directory
            #umount /global/sqlnode
            '''
        else:
            helpinfo='''
            To harden the MySQL NDB without HA:
            1. Make sure IPWorks NDB SQL node is stop
            
            2. Set up the MySQL SQL node Chroot environments
            #chroot_sqlnode_env start
            
            3. Use below command for ensure that the Chroot environment is enabled:
            #chroot_sqlnode_env status
            '''
        log._print.info(helpinfo)
        pass

