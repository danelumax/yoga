import os
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from scp import Scp


class FileTransferTask(object):
    '''
    Transfer Files
    '''


    def __init__(self):
        self._hostname = common.getHostName()
        
        
    def precheck(self):
        pass
    
    
    def execute(self):
        log._file.debug(">> File Transfer Begin")
        cfg = cfgInstance()
        self._dest_dir = cfg.getInstallPath()
        self._mount_point = cfg.getMountPoint()
        self._os_iso = cfg.getOsIsoPath()
        self._hae_iso = cfg.getHaeIsoPath()
        self._ipw_iso = cfg.getIpwIsoPath()
        self._license = cfg.getLicensePath()
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._copy_file(cfg.getPsCfg(0))
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._copy_file(cfg.getSsCfg(0))
            self._copy_file(cfg.getPsCfg(0))
            self._copy_file(cfg.getPsCfg(1))
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._copy_file(cfg.getSsCfg(0))
            self._copy_file(cfg.getPsCfg(0))
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            for ss_cfg in cfg.getSsCfgList() :
                self._copy_file(ss_cfg, 'ss')
            for ps_cfg in cfg.getPsCfgList() :
                self._copy_file(ps_cfg, 'ps')
        log._file.debug("<< File Transfer End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass



    def _getfiles(self) :
        file_list = []
        #curDir = os.path.dirname(os.path.realpath(__file__))
        curDir = "target/"
        for dirpath, dirnames, filenames in os.walk(curDir) :
            log._file.debug("Files need to be copy: [%s]" %filenames)
            for x in filenames :
                #log._file.debug("file: %s" %x)
                file_list.append("%s%s" %(dirpath, x))
        return file_list


    def _copy_file(self, node, mode='ps') : 
        log._file.debug(">>> Copy files to %s" %node.getHostName())
        ssh = sshManagerInstance().getSsh(node.getHostName())
        ssh_util = SshUtil(ssh, node.getOamIp())
        # remove dir
        ssh_util.remote_exec("rm -rf " + self._dest_dir)
        # create dir
        ssh_util.remote_exec("mkdir -p " + self._dest_dir)
        # scp files to remote machine
        scp = Scp(node.getOamIp(), node.getSshPort(), node.getUserName(), node.getPassword())
        # copy ha used files to remote machine
        if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            if cmp(node.getHostName(), self._hostname) :
                self._copy_ha_file(scp, node)
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :
            if not cmp('ss', mode) :
                if cmp(node.getHostName(), self._hostname) :
                    self._copy_ha_file(scp, node)
        if cmp(node.getHostName(), self._hostname) :
            log._file.debug("Copy IPWorks ISO packet to " + node.getHostName())
            scp.copy_to(self._ipw_iso, self._dest_dir)
        log._file.debug("Copy License file to " + node.getHostName())
        scp.copy_to(self._license, self._dest_dir)
        log._file.debug("Copy Script file to " + node.getHostName())
        file_list = self._getfiles()
        for x in file_list : 
            scp.copy_to(x, self._dest_dir)
        log._file.debug("<<<")


    def _copy_ha_file(self, scp, node) :
        log._file.debug("Copy OS & HA ISO packet to " + node.getHostName())
        scp.copy_to(self._os_iso, self._dest_dir)
        scp.copy_to(self._hae_iso, self._dest_dir)
        if cfgInstance().getHaCfg().getNeedUpdate() :
            log._file.debug("Copy HA Update Rpms to " + node.getHostName())
            for x in cfgInstance().getHaCfg().getUpdateRpms() :
                tmp = cfgInstance().getHaCfg().getUpdatePath() + x
                scp.copy_to(tmp, self._dest_dir)


