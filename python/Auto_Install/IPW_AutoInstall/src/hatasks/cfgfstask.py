import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from hautil import hautilInstance



class CfgFsTask(object) :
    """
    Config File System
    """

    def __init__(self) :
        self._lv_all = ["/dev/ipwdg/ipwvol", "/dev/ipwdg/mgmvol", "/dev/ipwdg/sqlvol", "/dev/ipwdg/csvvol"]
        self._lv_single = ["/dev/ipwdg/ipwvol"]

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Config HA File System Begin")
        # config LVM on SS nodes
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configLvm(cfgInstance().getSsCfg(0))
            self._checkLvmStatus(cfgInstance().getSsCfg(0))
            self._configOcfs(cfgInstance().getSsCfg(0))
            self._createDir(cfgInstance().getSsCfgList(), "ss")
            self._startResGrp(cfgInstance().getSsCfg(0))
        # config LVM on PS nodes
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configLvm(cfgInstance().getPsCfg(0))
            self._checkLvmStatus(cfgInstance().getPsCfg(0))
            self._configOcfs(cfgInstance().getPsCfg(0))
            self._createDir(cfgInstance().getPsCfgList(), "ps") 
            self._startResGrp(cfgInstance().getPsCfg(0))
        log._file.debug("<< Config HA File System End")
        
        

    def cleanup(self) :
        log._file.debug(">> Config HA File System Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._stopResGrp(cfgInstance().getSsCfg(0))
            self._removeDir(cfgInstance().getSsCfgList())
            self._removeLvm(cfgInstance().getSsCfg(0))
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._stopResGrp(cfgInstance().getPsCfg(0))
            self._removeDir(cfgInstance().getPsCfgList())
            self._removeLvm(cfgInstance().getPsCfg(0))
        log._file.debug("<< Config HA File System End")


    def verify(self) :
        pass

    def updateProgress(self) :
        pass



    def _configLvm(self, cfg) :
        log._file.debug(">>> Config LV on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        dev = ""
        if cfgInstance().getHaCfg().getHaDisk02() :
            dev = "/dev/md0"
        else :
            dev = cfgInstance().getHaCfg().getHaDisk01() + "1"      
        cmd = "pvcreate -ff -y " + dev
        ssh_util.remote_exec(cmd)
        cmd = "vgcreate -c y ipwdg " + dev
        ssh_util.remote_exec(cmd)
        cmd = "lvcreate -n ipwvol -L %dG ipwdg" %cfgInstance().getHaCfg().getFsIpwvolSize()
        ssh_util.remote_exec(cmd)
        if common.g_isInstall_AAA :
            cmd = "lvcreate -n mgmvol -L %dG ipwdg" %cfgInstance().getHaCfg().getFsMgmvolSize()
            ssh_util.remote_exec(cmd)
            cmd = "lvcreate -n sqlvol -L %dG ipwdg" %cfgInstance().getHaCfg().getFsSqlvolSize()
            ssh_util.remote_exec(cmd)
            cmd = "lvcreate -n csvvol -L %dG ipwdg" %cfgInstance().getHaCfg().getFsCsvvolSize()
            ssh_util.remote_exec(cmd)
        log._file.debug("<<<")
 

    def _removeLvm(self, cfg) :
        log._file.debug(">>> Remove LV on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if common.g_isInstall_AAA :
            ssh_util.remote_exec("lvremove /dev/ipwdg/csvvol")
            ssh_util.remote_exec("lvremove /dev/ipwdg/sqlvol")
            ssh_util.remote_exec("lvremove /dev/ipwdg/mgmvol")
        ssh_util.remote_exec("lvremove /dev/ipwdg/ipwvol")
        ssh_util.remote_exec("vgremove ipwdg")
        dev = ""
        if cfgInstance().getHaCfg().getHaDisk02() :
            dev = "/dev/md0"
        else :
            dev = cfgInstance().getHaCfg().getHaDisk01() + "1"
        ssh_util.remote_exec("pvremove " + dev) 
        log._file.debug("<<<")

 
    def _checkLv(self, cfg, lvs, result) :
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        status_lst = {}
        for lv in lvs :
            status_lst[lv] = "inactive"
            for line in result :
                if re.search(lv, line) :
                    status = line.strip().split()[0]
                    if cmp("ACTIVE", status) :
                        log._file.debug("need active " + lv)
                        ssh_util.remote_exec("lvchange -a y " + lv)
                    status_lst[lv] = status
                    break 
        for lv in lvs :
            if cmp("ACTIVE", status_lst[lv]) :
                return False       
        return True
 
 
 
    def _checkLvmStatus(self, cfg) :
        log._file.debug(">>> Check LV status on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        while True :
            res, code = ssh_util.remote_exec("lvscan")
            tmp = res.split("\n")
            if common.g_isInstall_AAA :
                if self._checkLv(cfg, self._lv_all, tmp) :
                    break
            else :
                if self._checkLv(cfg, self._lv_single, tmp) :
                    break
        log._file.debug("<<<")
            
    
    
    def _configOcfs(self, cfg) :
        log._file.debug(">>> Config OCFS on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if common.g_isInstall_AAA :
            for lv in self._lv_all :
                cmd = "echo \'y\' |mkfs.ocfs2 -N 8 " + lv
                ssh_util.remote_exec(cmd)
        else :
            for lv in self._lv_single :
                cmd = "echo \'y\' |mkfs.ocfs2 -N 8 " + lv
                ssh_util.remote_exec(cmd)
        log._file.debug("<<<")



    def _createDir(self, cfg_list, node) :
        for cfg in cfg_list :
            log._file.debug(">>> Create mount point on " + cfg.getHostName())
            ssh = sshManagerInstance().getSsh(cfg.getHostName())
            ssh_util = SshUtil(ssh)
            ssh_util.remote_exec("rm -rf /global", p_err=False, throw=False)
            ssh_util.remote_exec("mkdir /global")   
            if not cmp("ss", node) :
                ssh_util.remote_exec("mkdir /global/ipworks")
                if common.g_isInstall_AAA :
                    ssh_util.remote_exec("mkdir /global/mgmnode")
                    ssh_util.remote_exec("mkdir /global/sqlnode")
                    ssh_util.remote_exec("mkdir /global/csvengine")
            elif not cmp("ps", node) :
                if common.g_isInstall_CLF :
                    ssh_util.remote_exec("mkdir /global/clf")
        log._file.debug("<<<")


    def _removeDir(self, cfg_list) :
        for cfg in cfg_list :
            log._file.debug(">>> Remove mount point on " + cfg.getHostName())
            ssh = sshManagerInstance().getSsh(cfg.getHostName())
            ssh_util = SshUtil(ssh)
            ssh_util.remote_exec("rm -rf /global", p_err=False, throw=False)
        log._file.debug("<<<")


    def _startResGrp(self, cfg) :
        log._file.debug(">>> Start Resource Group on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        # start ipw-vg-clone
        hautilInstance().startVgClone(ssh)
        hautilInstance().waitVgCloneStart(ssh)
        # start fs-ipworks-clone
        hautilInstance().startIpworksClone(ssh)
        hautilInstance().waitIpworksCloneStart(ssh)     
        if common.g_isInstall_AAA :
            # start fs-mgm-clone
            hautilInstance().startMgmClone(ssh)
            hautilInstance().waitMgmCloneStart(ssh)
            # start fs-sql-clone
            hautilInstance().startSqlClone(ssh)
            hautilInstance().waitSqlCloneStart(ssh)
            # start fs-csv-clone
            hautilInstance().startCsvClone(ssh)
            hautilInstance().waitCsvCloneStart(ssh)
        log._file.debug("<<<")
        
        
    def _stopResGrp(self, cfg) :        
        log._file.debug(">>> Stop Resource Group on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())     
        if common.g_isInstall_AAA :
            # stop fs-csv-clone
            hautilInstance().stopCsvClone(ssh)
            hautilInstance().waitCsvCloneStop(ssh)
            # stop fs-sql-clone
            hautilInstance().stopSqlClone(ssh)
            hautilInstance().waitSqlCloneStop(ssh)
            # stop fs-mgm-clone
            hautilInstance().stopMgmClone(ssh)
            hautilInstance().waitMgmCloneStop(ssh)
        # stop fs-ipworks-clone
        hautilInstance().stopIpworksClone(ssh)
        hautilInstance().waitIpworksCloneStop(ssh)
        # stop ipw-vg-clone
        hautilInstance().stopVgClone(ssh)
        hautilInstance().waitVgCloneStop(ssh)
        log._file.debug("<<<")
        
        
        
        
        
        


