import os
import log, common
import subprocess
import re
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil
from hautil import hautilInstance


class SetActiveSSTask(object):
    '''
    Set Active SS 
    '''

    def __init__(self):
        pass 
        
    def precheck(self):
        pass
    
    
    def execute(self):
        log._file.debug(">> CheckIpwEnvTask")
          
        cfg = cfgInstance();
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2
            common.cleanEnvInfo()
            ss1 = cfg.getSsCfg(0)
            ss2 = cfg.getSsCfg(1)
            self._CheckActiveSs(ss1,ss2)


    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def help(self):
        log._print.info("1 Log on to ss1 or ss2")
        log._print.info('2 Use the command "crm_mon -1" to check resource gourp "res-ipwss-ss" status')
        log._print.info('3 If group "res-ipwss-ss" not started,make sure it is already started when execute this task')

    def _CheckActiveSs(self,ss1,ss2):
        log._file.debug(">>> _CheckActiveSs")
        ssh = sshManagerInstance().getSsh(ss1.getHostName())
        hostname = hautilInstance().ssStartOn(ssh)
        if hostname == ss1.getHostName():
            log._file.debug("SS group is started on : "+ss1.getHostName())
            ss1._isActiveSs = True
            common.saveEnvInfo(ss1.getHostName(),"Active-SS")
        elif hostname == ss2.getHostName():
            log._file.debug("SS group is started on : "+ss2.getHostName())
            ss2._isActiveSs = True
            common.saveEnvInfo(ss2.getHostName(),"Active-SS")
        else:
            raise Exception("group-ipwss started on unknown host: " + hostname)
        log._file.debug("<<< _CheckActiveSs")
      

    def _setEnvInfo(self,context):
        log._file.debug(">>> _setEnvInfo")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ss2 = cfg.getSsCfg(1)
        for x in context :
            tmp = x.split(';')
            if(tmp[1] == "Active-SS"):
                hostname = temp[0]
                if(hostname == ss1.getHostName()):
                    ss1._isActiveSs = True
                    common.saveEnvInfo(ss1.getHostName(),"Active-SS")
                if(hostname == ss2.getHostName()):
                    ss2._isActiveSs = True
                    common.saveEnvInfo(ss2.getHostName(),"Active-SS")
        log._file.debug("<<<")

