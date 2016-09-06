import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from hautil import hautilInstance



class ConfigSbdTask(object) :
    """
    Config SBD
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Config SBD Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                self._config(cfgInstance().getSsCfgList())
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                self._config(cfgInstance().getPsCfgList())
        log._file.debug("<< Config SBD End")

    def verify(self) :
        pass

    def updateProgress(self) :
        pass


    def cleanup(self) :
        log._file.debug(">> Cleanup SBD Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
           or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._removeSbd(cfgInstance().getSsCfgList())
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._removeSbd(cfgInstance().getPsCfgList())
        log._file.debug("<< Cleanup SBD End")


    def _removeSbd(self, cfg_list) :
        self._disableStonith(cfg_list[0])
        id_list = self._getIdList(cfg_list[0])
        for cfg in cfg_list :
            self._stopSbd(cfg, id_list)


    def _disableStonith(self, cfg) :
        log._file.debug(">>> Disable Stonith on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("crm configure property stonith-enable=false")
        log._file.debug("<<<")


    def _stopSbd(self, cfg, id_list) :
        log._file.debug(">>> Stop SBD on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        option = ""
        for x in id_list :
            option += "-d %s " %x
        cmd = "sbd %s -D message LOCAL exit" %option
        ssh_util.remote_exec(cmd)
        cmd = "sbd %s list" %option
        ssh_util.remote_exec(cmd)
        ssh_util.remote_exec("rm -f /etc/sysconfig/sbd", p_err=False, throw=False)
        log._file.debug("<<<")



    def _config(self, cfg_list) :
        # get disk id
        id_list = self._getIdList(cfg_list[0])
        # get host namel
        host_list = []
        for cfg in cfg_list :
            host_list.append(cfg.getHostName())
        # create SBD
        self._createSbd(cfg_list[0], id_list, host_list)
        # config SBD
        for cfg in cfg_list :
            self._configSbd(cfg, id_list)
        # register SBD
        self._registerSbd(cfg_list[0])
        # stop hp-asrd server
        for cfg in cfg_list :
            self._stopHpasrd(cfg)
        # start SBD resource
        self._startSbd(cfg_list[0])


    def _getIdList(self, cfg) :
        log._file.debug(">>> Get EMC disk UUID on " + cfg.getHostName())
        id_list = []
        id_list.append("/dev/disk/by-id/%s" %self._getDiskById(cfg, cfgInstance().getHaCfg().getHaDisk01()))
        if cfgInstance().getHaCfg().getHaDisk02() :
            id_list.append("/dev/disk/by-id/%s" %self._getDiskById(cfg, cfgInstance().getHaCfg().getHaDisk02()))
        log._file.debug("<<<")
        return id_list


    def _getDiskById(self, cfg, dev_path) :
        log._file.debug(">>> Get UUID of disk %s on %s " %(dev_path, cfg.getHostName()))    
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        dev = dev_path.split('/')[-1] + '2'
        log._file.debug("dev = " + dev)
        disk_by_id = ''
        command = "ls -l --color=never /dev/disk/by-id/"
        res, r_code = ssh_util.remote_exec(command)
        pattern = '../../' + dev
        lines = res.split("\n")
        for line in lines :
#            log._file.debug('#' + line + "#")
#            log._file.debug('pattern = ' + pattern)
            if re.search(pattern, line) :
#                toks = line.strip().split(' ')
                toks = re.split('\s+', line.strip())
                disk_by_id = toks[8]
                break
        log._file.debug("disk-by-id: " + str(disk_by_id))
        log._file.debug("<<<")
        return disk_by_id

 
    def _createSbd(self, cfg, id_list, host_list) :
        log._file.debug(">>> Create SBD on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        option = ""
        for disk_id in id_list :
            option += "-d %s " %disk_id
        cmd = "sbd %s -1 25 -4 50 create" %option
        ssh_util.remote_exec(cmd)
        for hostname in host_list :
            cmd = "sbd %s allocate %s" %(option, hostname)
            ssh_util.remote_exec(cmd)
        log._file.debug("<<<")


    def _configSbd(self, cfg, id_list) :
        log._file.debug(">>> Config SBD on %s" %cfg.getHostName())
        option = ";".join(id_list)
        content = "SBD_DEVICE=%s\nSBD_OPTS=\"-W\"" %option
        common.create_file(cfg, content, '/etc/sysconfig/', 'sbd')
        log._file.debug("<<<")


    def _registerSbd(self, cfg) :
        log._file.debug(">>> Register SBD on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        filename = "/opt/ipworks/IPWhaagents/confs/ipworks_sbd_fence.xml"
        ssh_util.remote_exec("cibadmin -o resource --cib_update --xml-file %s" %filename)
        ssh_util.remote_exec("cibadmin --cib_sync")
        ssh_util.remote_exec("crm configure property stonith-enabled=true stonith-action=poweroff shutdown-escalation=1min")
        log._file.debug("<<<")


    def _stopHpasrd(self, cfg) :
        log._file.debug(">>> Stop service hp-asrd on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("chkconfig hp-asrd off")
        ssh_util.remote_exec("service hp-asrd stop")
        log._file.debug("<<<")


    def _startSbd(self, cfg) :
        log._file.debug(">>> Start SBD resource on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        hautilInstance().startSbdResGrp(ssh)
        hautilInstance().waitSbdResGrpStart(ssh)
        log._file.debug("<<<")






