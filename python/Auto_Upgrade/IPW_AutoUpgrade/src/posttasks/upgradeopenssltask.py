import os,re,subprocess 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class UpgradeOpenSSLTask(object) :
    """
    Upgrading openSSL
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self):
        log._file.debug(">> UpgradeOpenSSLTask Begin")

        cfg_list = common.getNodeList(cfgInstance())
        for host in cfg_list:
            self._upgradeOpenSSL(host)

        log._file.debug("<< UpgradeOpenSSLTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        log._print.info(" remove openssl 1.0.1p installed from modified source code")
            
    
    def _cmd(self):
        cmd = "rm -rf /usr/ssl;" \
        "rm -rf /usr/include/openssl" \
        "rm -f /usr/lib64/libssl.a;" \
        "rm -f /usr/lib64/libcrypto.a;" \
        "rm -f /usr/lib64/pkgconfig/openssl.pc;" \
        "rm -f /usr/lib64/pkgconfig/libssl.pc;" \
        "rm -f /usr/lib64/pkgconfig/libcrypto.pc;"
        
        return cmd;


    def _upgradeOpenSSL(self, host):
        log._file.debug(">>> Begin to remove OpenSSL 1.0.1p installed from modified source code on host " + host.getHostName())
        cmd = self._cmd()
        
        ssh = sshManagerInstance().getSsh(host.getHostName())
        
        ssh_util = SshUtil(ssh)        
               
        res,code = ssh_util.remote_exec(cmd)

        log._file.debug("remove openSSL 1.0.1p Succeed!")
        