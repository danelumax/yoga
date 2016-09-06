#! /usr/bin/python
import os
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class MountISOTask(object):
    '''
    Mount IPWorks ISO
    '''


    def __init__(self):
        self._hostname = common.getHostName()
        pass
        
        
    def precheck(self):
        log._file.debug(">> Mount ISO Precheck begin")
        cfg = cfgInstance();
        isoPath = cfg.getUpgradePath() + cfg.getIpwIsoName();
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :  # single
            ps1 = cfg.getPsCfg(0)
            self._check_file_exists(ps1, isoPath)
        elif not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            for ss_cfg in cfg.getSsCfgList():
                self._check_file_exists(ss_cfg, isoPath)
            for ps_cfg in cfg.getPsCfgList():
                self._check_file_exists(ps_cfg, isoPath)
        elif not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode) :  # entry1
            ss1 = cfg.getSsCfg(0)
            self._check_file_exists(ss1, isoPath)
            for ps_cfg in cfg.getPsCfgList():
                self._check_file_exists(ps_cfg, isoPath)
        elif not cmp(common.C_IPW_MODE_ENTRY2,common.g_ipw_mode) :  # entry2
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            self._check_file_exists(ss1, isoPath)
            self._check_file_exists(ps1, isoPath)
        log._file.debug("<< Mount ISO Precheck end")

    
    def execute(self):
        log._file.debug(">> Mount ISO Begin")
        cfg = cfgInstance();
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :  # single
            ps1 = cfg.getPsCfg(0)
            self._remote_exec(ps1)
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            for ss_cfg in cfg.getSsCfgList():
                self._remote_exec(ss_cfg)
            for ps_cfg in cfg.getPsCfgList():
                self._remote_exec(ps_cfg)
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :  # entry1
            ss1 = cfg.getSsCfg(0)
            self._remote_exec(ss1)
            for ps_cfg in cfg.getPsCfgList():
                self._remote_exec(ps_cfg)
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :  # entry2
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            self._remote_exec(ss1)
            self._remote_exec(ps1)
        log._file.debug("<< Mount ISO End")
    

    def verify(self):
        log._file.debug(">> Verfiy mount iso Begin")
        cfg = cfgInstance();
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :  # single
            ps1 = cfg.getPsCfg(0)
            self._check_mount_result(ps1)
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            for ss_cfg in cfg.getSsCfgList():
                self._check_mount_result(ss_cfg)
            for ps_cfg in cfg.getPsCfgList():
                self._check_mount_result(ps_cfg)
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :  # entry1
            ss1 = cfg.getSsCfg(0)
            self._check_mount_result(ss1)
            for ps_cfg in cfg.getPsCfgList():
                self._check_mount_result(ps_cfg)
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :  # entry2
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            self._check_mount_result(ss1)
            self._check_mount_result(ps1)
        log._file.debug("<< Verify mount iso end")
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def _check_file_exists(self, cfg, filePath):
        log._file.debug(">>> Check IPWorks ISO is exist on %s" %cfg.getHostName())
	ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if not cmp(cfg.getHostName(), self._hostname) :
            ssh_util.remote_exec("ls " + cfgInstance().getIpwIsoPath())
        else :
	    ssh_util.remote_exec("ls " + filePath)
        log._file.debug("<<<")
	

    def _remote_exec(self, cfg) :
        log._file.debug(">>> Mount IPWorks ISO on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getUpgradePath())
        command = "python mountiso.py --mount_point=%s --iso_path=%s" %(cfgInstance().getMountPoint(), cfgInstance().getUpgradePath() + cfgInstance().getIpwIsoName())
        ssh_util.remote_exec(command) 
        log._file.debug("<<<")

    def _check_mount_result(self,cfg):
        log._file.debug(">>> Check mount result on "+ cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec("ls "+cfgInstance().getMountPoint()+"/x86-linux",True,False,False)
        if(r_code != 0):
            log._file.error("ISO is not mounted successfully in path:"+cfgInstance().getMountPoint()+"!!!")
            raise Exception("ISO mount failed on "+ cfg.getHostName())
        log._file.debug("<<< ISO successfully mounted on " + cfg.getHostName())

    def help(self):
        log._print.info("Use the command : mount -o loop <IPWorks ISO package name> <mount_point> to mount manually and check if it is successful")


   
	






