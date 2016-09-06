import re, time, random, os
import log, common
from sshutil import SshUtil
from cfg import cfgInstance
from hautil import hautilInstance
from sshmanager import sshManagerInstance


class ConfigSSTask(object):
    '''
    Config Storage Server
    '''


    def __init__(self):
        pass

        
    def precheck(self):
        #TODO: check the ISO file exist 
        #TODO: check the mount point exist and free to use
        pass
    
    def execute(self):
        log._file.debug(">> Config Storage Server Begin")
        cfg = cfgInstance()
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :  # single
            ps1 = cfg.getPsCfg(0)
            self._configSingleSs(ps1)
        if not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :  # entry1/2
            ss1 = cfg.getSsCfg(0)
            self._configSingleSs(ss1)
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2,common.g_ipw_mode) :  # medium1/2
            ss1 = cfg.getSsCfg(0)
            ss2 = cfg.getSsCfg(1)
            self._configSingleSs(ss1)
            self._stopSingleSsServices(ss1)
            self._registerHaResource(ss1, ss2)
            self._startHaResource(ss1)
        log._file.debug("<< Config Storage Server End")

    
    def verify(self):
        log._file.debug(">> Check Storage Server Statue Begin")
        common.save_healthcheck_info("Storage Server Status", 'running normal', 'running normal', "OK")
        log._file.debug("<< Check Storage Server Statue End")
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass


    def _stopSingleSsServices(self, cfg) :
        log._file.debug(">>> Stop SS in sigle mode on " + cfg.getHostName()) 
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        command = '/etc/init.d/ipworks.ss stop'
        ssh_util.remote_exec(command)
        time.sleep(5)
        command = '/etc/init.d/ipworks.mysql stop'
        ssh_util.remote_exec(command)
        time.sleep(5)
        command = '/etc/init.d/ipworks.tomcat stop'
        ssh_util.remote_exec(command)
        time.sleep(5)
        log._file.debug("<<<")



    def _addHost(self, cfg, hostname_list) :
        log._file.debug(">>>")    
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, r_code = ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        for hostname in hostname_list :
            command = 'python confighass.py --command=add_host --hostname=' + hostname + ' --ip=' + hostname_list[hostname]
            res, r_code = ssh_util.remote_exec(command)
        log._file.debug("<<<")



    def _registerHaResource(self, ss1_cfg, ss2_cfg) :
        log._file.debug(">>> Register SS resource group on " + ss1_cfg.getHostName())    
        ssh = sshManagerInstance().getSsh(ss1_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if not cmp(ss1_cfg.getPassword(), ss2_cfg.getPassword()):
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'echo "Y" | /opt/ipworks/IPWhaagents/scripts/register_cluster.pl --all-password ' + ss1_cfg.getPassword() + ' --diskarray'
            else:
                command = 'echo "Y" | /opt/ipworks/IPWhaagents/scripts/register_cluster.pl --all-password ' + ss1_cfg.getPassword() + ' --nfs'
            
            if cfgInstance().getHaCfg().getProvisionVip(): 
                command += ' --pro'
                
        else :
            passwd = '%s,%s' %(ss1_cfg.getPassword(), ss2_cfg.getPassword())
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'python register_cluster.py --command=ss --password=%s --mode=diskarray' %(passwd)
            else:
                command = 'python register_cluster.py --command=ss --password=%s --mode=nfs' %(passwd)
            
            if cfgInstance().getHaCfg().getProvisionVip(): 
                command+=' --has_prov_vip'
                    
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
            
        ssh_util.remote_exec(command)
        # wait for fs clone start
        if common.C_EMC_MOUNT_MODE_DOUBLE:
            hautilInstance().waitIpworksCloneStart(ssh)
        log._file.debug("<<<")    



    def _modifyTomcatStartTimeout(self, cfg) :
        log._file.debug(">>>")    
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python confighass.py --command=modify_tomcat_start_timeout'
        ssh_util.remote_exec(command)
        log._file.debug("<<<")   



    def _startHaResource(self, cfg) :
        log._file.debug(">>> Start SS resource group on " + cfg.getHostName())    
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        hautilInstance().startIpwssResGrp(ssh)
        hautilInstance().waitIpwssResGrpStart(ssh)
        log._file.debug("<<<")    



    def _configSingleSs(self, cfg) :
        log._file.debug(">>> Storage Server Initial configuration on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = "/etc/init.d/ipworks.mysql start-master-innodb"
        ssh_util.remote_exec(command) 
        command = '/opt/ipworks/IPWss/db/create_mysql_db'
        ssh_util.remote_exec(command) 
        command = '/etc/init.d/ipworks.ss start'
        ssh_util.remote_exec(command) 
        command = 'python configss.py --command=init_mysql_db --username=%s --password=%s ' %(common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        command = '/etc/init.d/ipworks.tomcat start'
        ssh_util.remote_exec(command)
        time.sleep(3)
        res,code = ssh_util.remote_exec('ps -ef |grep -v grep |grep "java -server -DApp=ipwss"')
        if not re.search('java -server -DApp=ipwss', res):
            raise Exception("Storage Server doesn't Started !")
        log._file.debug("<<<")
        common.saveCliPassword()


