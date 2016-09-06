import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil




class HealthCheckErrorLogTask(object) :
    """
    Check Error Log
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Check Error Logs Begin")
        checkList = self._getCheckList()
        appList = self._getAppList()
        for host in checkList:
            for app in appList:
                if(app == "aaa"):
                    self._checkAAAErrorLog(host)
                if(app == "dns"):
                    self._checkDNSErrorLog(host)
                if(app == "enum"):
                    self._checkENUMErrorLog(host)
                if(app == "dhcp"):
                    self._checkDHCPErrorLog(host)
                if(app == "clf"):
                    self._checkCLFErrorLog(host) 
        log._file.debug("<< Check Error Logs End")
        

    def verify(self) :
        pass

    def updateProgress(self) :
        pass

    def _getCheckList(self):
        log._file.debug(">>> Get node check list")
        checkList = []
        if not cmp(common.C_IPW_MODE_SINGLE,common.g_ipw_mode):
            checkList.append(cfgInstance().getPsCfg(0))
        if not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode) \
         or not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2,common.g_ipw_mode):
            checkList.append(cfgInstance().getPsCfg(0))
            checkList.append(cfgInstance().getPsCfg(1))
        if not cmp(common.C_IPW_MODE_ENTRY2,common.g_ipw_mode):
            checkList.append(cfgInstance().getPsCfg(0))
            checkList.append(cfgInstance().getSsCfg(0))
        log._file.debug("<<<") 
        return checkList
 
    def _getAppList(self):
        log._file.debug(">> Get app check list")
        appList = []
        if common.g_isInstall_AAA :
            appList.append("aaa")
        if common.g_isInstall_DNS :
            appList.append("dns")
        if common.g_isInstall_ENUM :
            appList.append("enum")
        if common.g_isInstall_DHCP :
            appList.append("dhcp")
        if common.g_isInstall_CLF :
            appList.append("clf")
        log._file.debug("<<<") 
        return appList
    
 
    def _parseErrorInfo(self, errinfo, searchinfo, item, hostname):
        tmp = errinfo.split('\n')
        log._file.info("split info:\n%s" %(str(tmp)))
        num = len(tmp)
        errno = 0
        for i in xrange(1, num):
            err = tmp[i].strip()
            if re.search(searchinfo, err):
                log._file.info("find %s :\n%s" %(searchinfo, err))
                common.save_healthcheck_info("%s_%d On %s" %(item, errno, hostname), err, "", "NOK")
                errno += 1


    def _checkDNSErrorLog(self, host):
        log._file.debug(">>> Check DNS Server Error logs on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        command = "cat /var/ipworks/logs/ipworks_dns.log | grep error"
        res,r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, 'error', 'DNS Error Logs', host.getHostName())
        log._file.debug("<<<")
 

    def _checkENUMErrorLog(self,host):
        log._file.debug(">>> Check ENUM Server Error logs on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        command1 = "cat /var/ipworks/logs/ipworks_enum.log | grep error"
        res,r_code = ssh_util.remote_exec(command1, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, 'error', 'ENUM Error Logs', host.getHostName())
        command2 = "cat /var/ipworks/logs/ipworks_enum.log | grep fail"
        res,r_code = ssh_util.remote_exec(command2, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, 'fail', 'ENUM Fail Logs', host.getHostName())
        log._file.debug("<<<") 


    def _checkDHCPErrorLog(self,host):
        log._file.debug(">>> Check DHCP Server Error logs on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        command1 = 'cat /var/ipworks/logs/ipworks_dhcpv4.log |grep "License Control: DHCP server can\'t be started"'
        res,r_code = ssh_util.remote_exec(command1, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, "DHCP server can't be started", 'DHCP Error Logs', host.getHostName())
        command2 = 'cat /var/ipworks/logs/ipworks_dhcpv4.log |grep "corrupt lease file"'
        res,r_code = ssh_util.remote_exec(command2, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, "corrupt lease file", 'DHCP Lease file Error Logs', host.getHostName())
        log._file.debug("<<<")
        
 
    def _checkAAAErrorLog(self,host):
        log._file.debug(">>> Check AAA Server Error logs on host " + host.getHostName())
        command1 = 'cat /var/ipworks/logs/aaa_core_server.log | grep error'
        command2 = 'cat /var/ipworks/logs/aaa_pluginbackend.log | grep error' 
        command3 = 'cat /var/ipworks/logs/aaa_radius_stack.log | grep error'
        command4 = 'cat /var/ipworks/logs/aaa_server.log | grep error'
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(command1, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, "error", 'AAA Core Server Error Logs', host.getHostName())
        res,r_code = ssh_util.remote_exec(command2, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, "error", 'AAA Plugin Backend Error Logs', host.getHostName())
        res,r_code = ssh_util.remote_exec(command3, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, "error", 'AAA Radius Stack Error Logs', host.getHostName())
        res,r_code = ssh_util.remote_exec(command4, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, "error", 'AAA EPC Error Logs', host.getHostName())
        log._file.debug("<<<")


    def _checkCLFErrorLog(self,host):
        log._file.debug(">>> Get CLF Error logs on host " + host.getHostName())
        command = 'cat /var/ipworks/logs/clf/clfd.log | grep ERROR'
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
        if 0 == r_code:
            self._parseErrorInfo(res, "ERROR", 'CLF Error Logs', host.getHostName())
        log._file.debug("<<<")
      
 

    
    

