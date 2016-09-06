import re
import log, common
from sshmanager import sshManagerInstance
from sshutil import SshUtil

    
def _parseErrorInfo(errinfo, searchinfo, item, hostname):
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


def checkDNSErrorLog(host):
    log._file.debug(">>> Check DNS Server Error logs on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    command = "cat /var/ipworks/logs/ipworks_dns.log | grep error"
    res,r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, 'error', 'DNS Error Logs', host.getHostName())
    log._file.debug("<<<")


def checkENUMErrorLog(host):
    log._file.debug(">>> Check ENUM Server Error logs on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    command1 = "cat /var/ipworks/logs/ipworks_enum.log | grep error"
    res,r_code = ssh_util.remote_exec(command1, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, 'error', 'ENUM Error Logs', host.getHostName())
    command2 = "cat /var/ipworks/logs/ipworks_enum.log | grep fail"
    res,r_code = ssh_util.remote_exec(command2, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, 'fail', 'ENUM Fail Logs', host.getHostName())
    log._file.debug("<<<") 


def checkDHCPErrorLog(host):
    log._file.debug(">>> Check DHCP Server Error logs on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    command1 = 'cat /var/ipworks/logs/ipworks_dhcpv4.log |grep "License Control: DHCP server can\'t be started"'
    res,r_code = ssh_util.remote_exec(command1, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, "DHCP server can't be started", 'DHCP Error Logs', host.getHostName())
    command2 = 'cat /var/ipworks/logs/ipworks_dhcpv4.log |grep "corrupt lease file"'
    res,r_code = ssh_util.remote_exec(command2, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, "corrupt lease file", 'DHCP Lease file Error Logs', host.getHostName())
    log._file.debug("<<<")
        
 
def checkAAAErrorLog(host):
    log._file.debug(">>> Check AAA Server Error logs on host " + host.getHostName())
    command1 = 'cat /var/ipworks/logs/aaa_core_server.log | grep error'
    command2 = 'cat /var/ipworks/logs/aaa_pluginbackend.log | grep error' 
    command3 = 'cat /var/ipworks/logs/aaa_radius_stack.log | grep error'
    command4 = 'cat /var/ipworks/logs/aaa_server.log | grep error'
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    res,r_code = ssh_util.remote_exec(command1, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, "error", 'AAA Core Server Error Logs', host.getHostName())
    res,r_code = ssh_util.remote_exec(command2, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, "error", 'AAA Plugin Backend Error Logs', host.getHostName())
    res,r_code = ssh_util.remote_exec(command3, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, "error", 'AAA Radius Stack Error Logs', host.getHostName())
    res,r_code = ssh_util.remote_exec(command4, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, "error", 'AAA EPC Error Logs', host.getHostName())
    log._file.debug("<<<")


def checkCLFErrorLog(host):
    log._file.debug(">>> Get CLF Error logs on host " + host.getHostName())
    command = 'cat /var/ipworks/logs/clf/clfd.log | grep ERROR'
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    res,r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
    if 0 == r_code:
        _parseErrorInfo(res, "ERROR", 'CLF Error Logs', host.getHostName())
    log._file.debug("<<<")











