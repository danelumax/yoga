import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class CheckInstallEnvTask(object):
    '''
    Check Install Environment
    '''

    def __init__(self):
        pass

    def precheck(self):
        pass


    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def execute(self):
        log._file.debug(">> Install Env Check Begin") 
        cfg_list = common.getNodeList(cfgInstance())
        for host in cfg_list:
            self._checkenv(host)
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._checkhaenv()
        log._file.debug("<< Install Env Check End") 


    def _checkenv(self, host):
        log._file.debug(">>> Begin to check Env on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec('rpm -qa |grep IPW |grep -v grep', p_err=False, throw=False)
        lines = res.split('\n')
        for line in lines:
            if re.search('^IPW', line):
                log._file.info('Find Ipworks rpm: ' + line)
                errinfo = "Already Exist IPWorks on %s, Please stop ipworks process and uninstall it before execute new installation !" %(host.getHostName())
                log._file.error(errinfo)
                raise Exception(errinfo)
        log._file.debug("<<<")


    def _checkhaenv(self):
        log._file.debug(">>> Begin to check HA Env")
        if not cmp(common.C_EMC_MODE_NFS, cfgInstance().getHaCfg().getEmcMode()) :
            if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
              or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                ss1 = cfgInstance().getSsCfg(0)
                ss2 = cfgInstance().getSsCfg(1)
                if common.g_isInstall_AAA :
                    dirList = ['/global/ipworks', '/global/mgmnode', '/global/sqlnode', '/global/csvengine']
                else :
                    dirList = ['/global/ipworks']
                self._checkdir(ss1, dirList)
                self._checkdir(ss2, dirList)
                self._cleandir(ss1, dirList)
            if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                ps1 = cfgInstance().getPsCfg(0)
                ps2 = cfgInstance().getPsCfg(1)
                dirList = ['/global/clf']
                self._checkdir(ps1, dirList)
                self._checkdir(ps2, dirList)
                self._cleandir(ps1, dirList)
        log._file.debug("<<<")


    def _checkdir(self, host, dirlist):
        log._file.debug(">>> check directory %s is exsit on %s" %(str(dirlist), host.getHostName()))
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        for x in dirlist:
            res,code = ssh_util.remote_exec('ls %s' %(x), p_err=False, throw=False)
            if 0 != code:
                log._file.debug('Directory "%s" does not Exist, will create it automatically !' %(x))
                ssh_util.remote_exec("mkdir -p " + x)
            else :
                ssh_util.remote_exec("rm -rf %s/*" %(x), p_err=False, throw=False)
            res,code = ssh_util.remote_exec('cat /etc/fstab |grep "%s"| grep -v "^ *#"' %(x), p_err=False, throw=False)
            if 0 != code:
                log._file.debug('NFS Shared information of directory "%s" does not Exist in "/etc/fstab", will add it automatically !' %(x))
                dir_name = x.split('/')[2]
                ssh_util.remote_exec('echo "%s:/%s    %s    nfs    noauto    0  0" >> /etc/fstab ' %(cfgInstance().getHaCfg().getNfsIp(), dir_name, x))
                #ssh_util.remote_exec('echo "%s:%s    %s    nfs    noauto    0  0" >> /etc/fstab ' %(cfgInstance().getHaCfg().getNfsIp(), x, x))
        log._file.debug("<<<")


    def _cleandir(self, host, dirlist):
        log._file.debug(">>> cleanup dir %s on %s" %(str(dirlist), host.getHostName()))
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,code = ssh_util.remote_exec('mount')
        for x in dirlist:
            if not re.search(x, res):
                ssh_util.remote_exec('mount %s' %(x))
            ssh_util.remote_exec('rm -rf %s/*' %(x))
            ssh_util.remote_exec('umount %s' %(x))
        log._file.debug("<<<")








