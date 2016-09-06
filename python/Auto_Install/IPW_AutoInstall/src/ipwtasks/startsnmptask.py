import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class StartSnmpTask(object) :
    """
    Start SNMP
    """

    def __init__(self) :
        self._mgm_vip = ''

    def precheck(self) :
        pass

    def execute(self) :
        log._file.debug(">> Start SNMP Begin")
        startList = self._getStartList()
        for host in startList:
            self._startSNMP(host)
        log._file.debug("<< Start SNMP End")
        

    def verify(self) :
        pass

    def updateProgress(self) :
        pass

    def  _getStartList(self):
        log._file.debug(">>> Get Start Snmp node List")
        startlist = []
        if not cmp(common.C_IPW_MODE_SINGLE,common.g_ipw_mode):
            startlist.append(cfgInstance().getPsCfg(0))
            if common.g_isInstall_AAA or common.g_isInstall_ENUM :
                self._configSNMP(cfgInstance().getPsCfg(0), cfgInstance().getPsCfg(0).getInternalIp())
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2,common.g_ipw_mode) :
            startlist.append(cfgInstance().getSsCfg(0))
            startlist.append(cfgInstance().getSsCfg(1))
            startlist.append(cfgInstance().getPsCfg(0))
            startlist.append(cfgInstance().getPsCfg(1))
            if common.g_isInstall_AAA :
                self._configSNMP(cfgInstance().getSsCfg(0), cfgInstance()._ha_cfg.getMgmVip())
                self._configSNMP(cfgInstance().getSsCfg(1), cfgInstance()._ha_cfg.getMgmVip())
            elif common.g_isInstall_ENUM :
                ip = '"%s;%s"' %(cfgInstance().getPsCfg(0).getInternalIp(), cfgInstance().getPsCfg(1).getInternalIp())
                self._configSNMP(cfgInstance().getSsCfg(0), ip)
                self._configSNMP(cfgInstance().getSsCfg(1), ip)
        if not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode):
            startlist.append(cfgInstance().getSsCfg(0))
            startlist.append(cfgInstance().getPsCfg(0))
            startlist.append(cfgInstance().getPsCfg(1))
            if common.g_isInstall_AAA:
                self._configSNMP(cfgInstance().getSsCfg(0), cfgInstance().getSsCfg(0).getInternalIp())
            elif common.g_isInstall_ENUM :
                ip = '"%s;%s"' %(cfgInstance().getPsCfg(0).getInternalIp(), cfgInstance().getPsCfg(1).getInternalIp())
                self._configSNMP(cfgInstance().getSsCfg(0), ip)
        if not cmp(common.C_IPW_MODE_ENTRY2,common.g_ipw_mode):
            startlist.append(cfgInstance().getSsCfg(0))
            startlist.append(cfgInstance().getPsCfg(0))
            if common.g_isInstall_ENUM :
                ip = '"%s;%s"' %(cfgInstance().getPsCfg(0).getInternalIp(), cfgInstance().getSsCfg(0).getInternalIp())
                self._configSNMP(cfgInstance().getSsCfg(0), ip)
        log._file.debug("<<<")
        return startlist

    def _startSNMP(self, host):
        log._file.debug(">>> Start SNMP On Host : " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        #command = "/etc/init.d/ipworks.snmpd start noreset"
        command = "/etc/init.d/ipworks.snmpd start"
        ssh_util.remote_exec(command)
        command = "/etc/init.d/ipworks.snmptrapd start"
        ssh_util.remote_exec(command)
        log._file.debug("<<<")

        
    def _configSNMP(self, host, mgm_vip):
        log._file.debug(">>> Config SNMP on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec("python configsnmp.py --mgm_vip " + mgm_vip)
        log._file.debug("<<<")
        






