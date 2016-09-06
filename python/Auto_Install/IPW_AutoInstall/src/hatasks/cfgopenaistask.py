import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from hautil import hautilInstance


class CfgOpenAISTask(object) :
    """
    Config OpenAIS
    """

    def __init__(self) :
        self._cfg = cfgInstance()
        self._corosync_cfg = "src/template/corosync.conf.tmp"
        self._csync2_cfg = "src/template/csync2.cfg.tmp"
        

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">>> Config HA OpenAIS Begin")
        # config OpenAIS on SS nodes
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._cfgopenais(self._cfg.getSsCfgList())
        # config OpenAIS on PS nodes
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._cfgopenais(self._cfg.getPsCfgList())             
        log._file.debug("<<< Config HA OpenAIS End")
        

    def verify(self) :
        pass

    def updateProgress(self) :
        pass


    def cleanup(self) :
        log._file.debug(">>> Cleanup HA OpenAIS Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._stopService(self._cfg.getSsCfgList())
            self._removeFile(self._cfg.getSsCfgList())
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._stopService(self._cfg.getPsCfgList())
            self._removeFile(self._cfg.getPsCfgList())
        log._file.debug(">>> Cleanup HA OpenAIS Begin")


    def _stopService(self, cfg_list) :
        for cfg in cfg_list :
            self._chkconfigService(cfg, "csync2", "off")
            self._chkconfigService(cfg, "openais", "off", start="stop")


    def _removeFile(self, cfg_list) :
        for cfg in cfg_list :
            log._file.debug("Remove openais cfg file on " + cfg.getHostName())
            files = ["/var/lib/csync2/*", "/etc/sysconfig/pacemaker", "/etc/sysconfig/openais", "/etc/csync2/key_hagroup", "/etc/csync2/csync2.cfg", "/etc/corosync/corosync.conf"]
            ssh = sshManagerInstance().getSsh(cfg.getHostName())
            ssh_util = SshUtil(ssh)
            for x in files :    
                cmd = "rm -f %s" %x
                ssh_util.remote_exec(cmd, p_err=False, throw=False)           



    def _cfgCorosync(self, cfg) :
        log._file.debug("Config corosync.conf on " + cfg.getHostName())
        content = common.open_file(self._corosync_cfg)
        content = content.replace("###bindnetaddr1###", cfg.getNetAddr(cfg.getHeartbeatIp1(), cfg.getHeartbeatPrefix()))
        content = content.replace("###mcastaddr1###", self._cfg.getHaCfg().getHaMulticastIp1())
        content = content.replace("###mcastport1###", str(self._cfg.getHaCfg().getHaMulticastPort1()))
        content = content.replace("###bindnetaddr2###", cfg.getNetAddr(cfg.getHeartbeatIp2(), cfg.getHeartbeatPrefix()))
        content = content.replace("###mcastaddr2###", self._cfg.getHaCfg().getHaMulticastIp2())
        content = content.replace("###mcastport2###", str(self._cfg.getHaCfg().getHaMulticastPort2()))
        log._file.debug("corosync.conf content: \n %s" %content)
        common.create_file(cfg, content, '/etc/corosync/', 'corosync.conf')



    def _cfgCsync2(self, cfg, hostname_list) :
        log._file.debug("Config csync2.cfg on " + cfg.getHostName())
        content = common.open_file(self._csync2_cfg)
        content = content.replace("###ss_01_hostname###", hostname_list[0]) 
        content = content.replace("###ss_02_hostname###", hostname_list[1])
        log._file.debug("csync2.cfg content: \n %s" %content)
        common.create_file(cfg, content, '/etc/csync2/', 'csync2.cfg')
        content = common.open_file("src/template/openais.tmp")
        common.create_file(cfg, content, '/etc/sysconfig/', 'openais')
        content = common.open_file("src/template/pacemaker.tmp")
        common.create_file(cfg, content, '/etc/sysconfig/', 'pacemaker')



    def _chkconfigService(self, cfg, service, on="on", start="") :
        log._file.debug("Chkconfig %s %s, %s: %s" %(service, on, cfg.getHostName(), start))
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        cmd = "chkconfig -s %s %s" %(service, on)
        ssh_util.remote_exec(cmd)
        if start :
            cmd = "/etc/init.d/" + service + " " + start
            ssh_util.remote_exec(cmd)



    def _generateSharedkey(self, master, slave) :
        log._file.debug("Generate PreShared Keys on %s" %master.getHostName())
        ssh = sshManagerInstance().getSsh(master.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("rm /etc/csync2/key_hagroup", p_err=False, throw=False)
        cmd = "csync2 -k /etc/csync2/key_hagroup"
        ssh_util.remote_exec(cmd, p_err=False, throw=False)    
        # copy to ss02
        res, code = ssh_util.remote_exec("cat /etc/csync2/key_hagroup")
        content = res.split("\n")[1]
        common.create_file(slave, content, '/etc/csync2/', 'key_hagroup')



    def _syncfiles(self, cfg) :
        log._file.debug("Synchronize the files of cluster on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, code = ssh_util.remote_exec("csync2 -xv", p_err=False, throw=False)
        #if (not re.search("Finished with 0 errors", res)) and (not re.search("Finished with 1 errors", res)) :
        #    raise Exception("Synchronize files failed !")



    def _setHaclusterPasswd(self, cfg) :
        log._file.debug("Set user hacluster password on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + self._cfg.getInstallPath())
        ssh_util.remote_exec("python sethaclusterpasswd.py --passwd=" + self._cfg.getHaCfg().getHaClusterPassword())



    def _checkClusterStatus(self, cfg, hostname_list) :
        log._file.debug("Check Cluster Status on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        if hautilInstance().checkClusterStatus(ssh, hostname_list) :
            log._file.debug("Cluster has synchronized !")
        else :
            raise Exception("Cluster hasn't synchronized !")
        
        #ssh_util = SshUtil(ssh)
        #res, code = ssh_util.remote_exec("crm_mon -1 |grep Online")
        #log._file.debug("command: \n %s" %"crm_mon -1 |grep Online")
        #if re.search(str(hostname_list[0]), res) and re.search(str(hostname[1]), res) :
        #    log._file.debug("Cluster has synchronized !")
        #else :
        #    raise Exception("Cluster hasn't synchronized !")



    def _cfgopenais(self, cfg_list) :
        hostname_list = []
        for cfg in cfg_list :
            hostname_list.append(cfg.getHostName())
        try :    
            for cfg in cfg_list :
                self._cfgCorosync(cfg)
                self._cfgCsync2(cfg, hostname_list)          
            self._generateSharedkey(cfg_list[0], cfg_list[1])    
            for cfg in cfg_list :
                self._chkconfigService(cfg, "openais", start="start")
                self._chkconfigService(cfg, "csync2")
                self._chkconfigService(cfg, "xinetd", start="restart")  
            self._syncfiles(cfg_list[0])   
            for cfg in cfg_list :
                self._setHaclusterPasswd(cfg)         
            self._checkClusterStatus(cfg_list[0], hostname_list)
        except :
            log._file.error("Failed when config OpenAIS !!!")
            self._stopService(cfg_list)
            self._removeFile(cfg_list)
            raise
    

   



