import re, time
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class HealthCheckAlarmTask(object) :
    """
    Check Alarm Table
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self) :
        log._file.debug(">> Check Alarm Table Begin")
        checkList = common.getNodeList(cfgInstance())
        for host in checkList:
            #self._startSNMP(host)
            self._stopSNMP(host)
        #checkList = self._getCheckList()
        #appList = self._getAppList()
        #for host in checkList:
        #    for app in appList:
        #        if app == "aaa":
        #            self._getAAAAlarm(host)
        #        if app == "dns":
        #            self._getDNSAlarm(host)
        #        if app == "enum":
        #            self._getENUMAlarm(host)
        #        if app == "dhcp":
        #            self._getDHCPAlarm(host)
        #        if app == "clf":
        #            self._getCLFAlarm(host)
        self._getHAAlarm()
        self._getNDBClusterAlarm()
        log._file.debug("<< Check Alarm Table End")
        

    def verify(self) :
        pass

    def updateProgress(self) :
        pass

    def _getCheckList(self):
        log._file.debug(">>> Get node check list")
        checkList = []
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode):
            checkList.append(cfgInstance().getPsCfg(0))
        if not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) \
         or not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):
            checkList.append(cfgInstance().getPsCfg(0))
            checkList.append(cfgInstance().getPsCfg(1))
        if not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode):
            checkList.append(cfgInstance().getPsCfg(0))
            checkList.append(cfgInstance().getSsCfg(0))
        log._file.debug("<<<")
        return checkList
 
    def _getAppList(self):
        log._file.debug(">>> Get app check list")
        appList = []
        if common.g_isInstall_AAA:
            appList.append("aaa")
        if common.g_isInstall_DNS:
            appList.append("dns")
        if common.g_isInstall_ENUM:
            appList.append("enum")
        if common.g_isInstall_DHCP:
            appList.append("dhcp")
        if common.g_isInstall_CLF:
            appList.append("clf")
        log._file.debug("<<<")
        return appList
    
    def _startSNMP(self, host):
        log._file.debug(">>> Start snmp on host: " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        #command = "/etc/init.d/ipworks.snmpd start noreset" 
        command = "/etc/init.d/ipworks.snmpd start"
        ssh_util.remote_exec(command)
        command = "/etc/init.d/ipworks.snmptrapd start"
        ssh_util.remote_exec(command)
        time.sleep(3)
        log._file.debug("<<<")

    def _stopSNMP(self, host):
        log._file.debug(">>> Stop snmp on host: " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        command = "/etc/init.d/ipworks.snmpd stop" 
        ssh_util.remote_exec(command)
        command = "/etc/init.d/ipworks.snmptrapd stop"
        ssh_util.remote_exec(command)
        time.sleep(3)
        log._file.debug("<<<")
 
    # app: ipworksDns, ipworksEnum, ipworksAAA, ipworksDhcpv4, ipworksCLF, ipworksCLFCommon, ipworksCLFPmal,
    #      ipworksEM, ClusterSS, SharedStorage, ClusterCLF
    def _getAppAlarm(self, host, app):
        log._file.debug(">>> Get %s alarm on host %s" %(app, host.getHostName()))
        command = 'cat /var/net-snmp/ipworks_snmpdata.conf | grep "%s"' %(app)       
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
        tmplist = res.split('\n')
        alarm_no = 0
        for alarm in tmplist:
            alarm = alarm.strip()
            if re.search("this alarm", alarm.lower()) :
                log._file.info("alarmInfo = " + alarm)
                item = "Alarm %s_%d On %s" %(app, alarm_no, host.getHostName())
                common.save_healthcheck_info(item, alarm, "", "--")
                alarm_no += 1
        log._file.debug("<<<")

    def _getDNSAlarm(self, host):
        log._file.debug(">>> Get DNS alarm begin")
        self._getAppAlarm(host, 'ipworksDns')
        log._file.debug("<<< Get DNS alarm end")

    def _getENUMAlarm(self, host):
        log._file.debug(">>> Get Enum alarm begin")
        self._getAppAlarm(host, 'ipworksEnum')      
        log._file.debug("<<< Get Enum alarm end")

    def _getDHCPAlarm(self, host):
        log._file.debug(">>> Get Dhcp alarm begin")     
        self._getAppAlarm(host, 'ipworksDhcpv4')
        log._file.debug("<<< Get Dhcp alarm end")
 
    def _getAAAAlarm(self, host):
        log._file.debug(">>> Get AAA alarm begin")   
        self._getAppAlarm(host, 'ipworksAAA')   
        log._file.debug("<<< Get AAA alarm end")
  
    def _getCLFAlarm(self, host):
        log._file.debug(">>> Get CLF alarm begin") 
        self._getAppAlarm(host, 'ipworksCLF')
        self._getAppAlarm(host, 'ipworksCLFCommon') 
        self._getAppAlarm(host, 'ipworksCLFPmal') 
        log._file.debug("<<< Get CLF alarm end")
    
    def _getHAAlarm(self):
        log._file.debug(">>> Get HA alarm begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :
            for app in ['ClusterSS', 'SharedStorage']:
                self._getAppAlarm(cfgInstance().getSsCfg(0), app)
                self._getAppAlarm(cfgInstance().getSsCfg(1), app)
        elif not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            for app in ['ClusterSS', 'SharedStorage', 'ClusterCLF']:
                self._getAppAlarm(cfgInstance().getSsCfg(0), app)
                self._getAppAlarm(cfgInstance().getSsCfg(1), app)
                self._getAppAlarm(cfgInstance().getPsCfg(0), app)
                self._getAppAlarm(cfgInstance().getPsCfg(1), app)
        else :
            log._file.info("No need to check HA Alarm")
        log._file.debug("<<< Get HA alarm end")
     
    def _getNDBClusterAlarm(self):
        log._file.debug(">>> Get NDB Cluster alarm begin")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode):
            self._getAppAlarm(cfgInstance().getPsCfg(0), 'ipworksEM')
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode):
            self._getAppAlarm(cfgInstance().getSsCfg(0), 'ipworksEM')
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):
            self._getAppAlarm(cfgInstance().getSsCfg(0), 'ipworksEM')    
            self._getAppAlarm(cfgInstance().getSsCfg(1), 'ipworksEM') 
        log._file.debug("<<< Get NDB Cluster alarm end")
  
    
    

