import re, time
import log, common
from sshutil import SshUtil
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from hautil import hautilInstance



class CfgRaidTask(object) :
    """
    Config RAID
    """

    def __init__(self) :
        self._cfg = cfgInstance()

    def precheck(self) :
        pass


    def execute(self) :
        log._file.debug(">> Config HA Raid Begin")
        # config Raid on SS nodes
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configRaid(self._cfg.getSsCfgList())
        # config Raid on PS nodes
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._configRaid(self._cfg.getPsCfgList())       
        log._file.debug("<< Config HA Raid End")


    def cleanup(self) :
        log._file.debug(">> Cleanup HA Raid Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._removeRaid(self._cfg.getSsCfgList())
            self._removePartition(self._cfg.getSsCfg(0))
        if not cmp (common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._removeRaid(self._cfg.getPsCfgList())
            self._removePartition(self._cfg.getPsCfg(0))
        log._file.debug("<< Cleanup HA Raid End")


    def verify(self) :
        pass

    def updateProgress(self) :
        pass


    def _configRaid(self, cfg_list) :
        self._createPartition(cfg_list[0])
        if self._cfg.getHaCfg().getHaDisk02() :
            self._createRaid(cfg_list[0])
            self._waitingMdSync(cfg_list[0])
            uuid = self._getRaidUUID(cfg_list[0])
            self._configMdadm(cfg_list[0], uuid)
            self._configMdadm(cfg_list[1], uuid)
        else :
            log._file.debug("Only exist One EMC Disk")
        self._reboot(cfg_list[1])
        self._waitPeerReboot(cfg_list[0], cfg_list[1].getOamIp())
        hostname_list = []
        for cfg in cfg_list :
            hostname_list.append(cfg.getHostName())
        self._checkStatus(cfg_list[1], hostname_list)
        self._checkPartition(cfg_list[1])



    def _createPartition(self, cfg) :
        log._file.debug(">>> Create Partition on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + self._cfg.getInstallPath())
        # create patition on EMC disk 01
        cmd = "python configraid.py --command=create_partition --device_path=" + self._cfg.getHaCfg().getHaDisk01() + " --md0_size=" + str(self._cfg.getHaCfg().getMd0Size()) + " --sbd_size=" + str(self._cfg.getHaCfg().getSbdSize())
        ssh_util.remote_exec(cmd)
        # create patition on EMC disk 02
        if self._cfg.getHaCfg().getHaDisk02() :
            cmd = "python configraid.py --command=create_partition --device_path=" + self._cfg.getHaCfg().getHaDisk02() + " --md0_size=" + str(self._cfg.getHaCfg().getMd0Size()) + " --sbd_size=" + str(self._cfg.getHaCfg().getSbdSize())
            ssh_util.remote_exec(cmd)
        log._file.debug("<<<")
        

    def _removePartition(self, cfg) :
        log._file.debug(">>> Remove Partition on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + self._cfg.getInstallPath())
        tt = "python configraid.py --command=remove_partition --device_path="
        cmd = tt + self._cfg.getHaCfg().getHaDisk01()
        ssh_util.remote_exec(cmd)
        if self._cfg.getHaCfg().getHaDisk02() :
            # has two EMC disk
            cmd = tt + self._cfg.getHaCfg().getHaDisk02()
            ssh_util.remote_exec(cmd)
        log._file.debug("<<<")



    def _createRaid(self, cfg) :
        log._file.debug(">>> Create Raid on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + self._cfg.getInstallPath())
        cmd = "python configraid.py --command=create_raid --device_path=" + self._cfg.getHaCfg().getHaDisk01() + ',' + self._cfg.getHaCfg().getHaDisk02()
        ssh_util.remote_exec(cmd)
        log._file.debug("<<<")


    def _removeRaid(self, cfg_list) :
        if self._cfg.getHaCfg().getHaDisk02() :
            for cfg in cfg_list :
                log._file.debug(">>> Remove RAID on " + cfg.getHostName())
                ssh = sshManagerInstance().getSsh(cfg.getHostName())
                ssh_util = SshUtil(ssh)
                ssh_util.remote_exec("mdadm --stop /dev/md0")
                ssh_util.remote_exec("chkconfig boot.md off")
                ssh_util.remote_exec("rm -f /etc/mdadm.conf", p_err=False, throw=False)
            log._file.debug("<<<")
        else :
            log._file.debug("No need to remove RAID, Only exist one EMC Disk Array")



    def _waitingMdSync(self, cfg) :
        log._file.debug(">>> Wait for mdstat resync on " + cfg.getHostName())
        cmd = "cat /proc/mdstat"
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        while True :    
            res, code = ssh_util.remote_exec(cmd)
            log._file.debug("mdstat:\n %s" %res)
            if re.search("resync = ", res) :
                time.sleep(20)
            else :
                break
        log._file.debug("<<<")
    
    
    def _getRaidUUID(self, cfg) :
        log._file.debug(">>> Get Raid UUID on " + cfg.getHostName())
        cmd = "mdadm --detail --scan"
        uuid = ""
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        while True :
            res, r_code = ssh_util.remote_exec(cmd)
            lines = res.split("\n")
            for line in lines :
                toks = line.split("UUID=")
                if len(toks) == 2 :
                    uuid = toks[1].strip()
            
            if not uuid :
                log._file.warning("Can't find UUID with md0")
                time.sleep(5)
            else :
                log._file.debug("UUID = " + str(uuid))
                break
        log._file.debug("<<<")
        return uuid
    

    def _configMdadm(self, cfg, uuid) :
        log._file.debug(">>> Config mdadm.conf on " + cfg.getHostName())
        content = "DEVICE containers partitions\nARRAY /dev/md0 UUID=" + uuid
        common.create_file(cfg, content, '/etc/', 'mdadm.conf')
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("chkconfig -s boot.md on")
        log._file.debug("<<<")


    def _reboot(self, cfg) :
        log._file.debug(">>> Reboot on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        # the openais will hangs sometimes, so force the openais down before the note reboot
        ssh_util.remote_exec("/etc/init.d/openais force-stop")
        ssh_util.remote_exec("reboot")
        #time.sleep(5)
        log._file.debug("<<<")


    def _waitPeerReboot(self, cfg, peer_ip) :
        log._file.debug(">>> Wait Peer Reboot on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + self._cfg.getInstallPath())
        ssh_util.remote_exec("python configraid.py --command=wait_peer_reboot --peer_ip=" + peer_ip)
        while not sshManagerInstance().trySsh(cfg.getHostName()) :
            time.sleep(10)
        log._file.debug("<<<")


    def _checkStatus(self, cfg, hostname_list) :
        log._file.debug(">>> Check Cluster Status on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        if hautilInstance().checkClusterStatus(ssh, hostname_list) :
            log._file.debug("Cluster has synchronized !")
        else :
            raise Exception("Cluster hasn't synchronized !")
        log._file.debug("<<<")
        
    
    def _checkPartition(self, cfg) :
        log._file.debug(">>> Check Partition on %s" %cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, code = ssh_util.remote_exec("fdisk -l")
        p1 = "%s1" %self._cfg.getHaCfg().getHaDisk01()
        p2 = "%s2" %self._cfg.getHaCfg().getHaDisk01()
        if self._cfg.getHaCfg().getHaDisk02() :
            p3 = "%s1" %self._cfg.getHaCfg().getHaDisk02()
            p4 = "%s2" %self._cfg.getHaCfg().getHaDisk02()
            cmd = "ls %s %s %s %s /dev/md0" %(p1, p2, p3, p4)
            res, code = ssh_util.remote_exec(cmd, p_err=False, throw=False)
            if 0 == code :
                log._file.debug("Two EMC Disk Partition has Synchronized")
            else :
                raise Exception("Partition hasn't Synchronized !")
        else :
            # only one EMC disk, doesn't exist md0, sdc
            cmd = "ls %s %s" %(p1, p2)
            res, code = ssh_util.remote_exec(cmd, p_err=False, throw=False)
            if 0 == code :
                log._file.debug("One EMC Disk Partition has Synchronized")
            else :
                raise Exception("Partition hasn't Synchronized !")
        log._file.debug("<<<")
            



















