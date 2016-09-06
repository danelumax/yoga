'''
Created on 2015/04/17

@author: eyotang
'''

import os,re,subprocess
import log, common, procs
import time

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class StopServiceProcessTask(object) :
    """
    Stop Service Process
    """

    def __init__(self) :
        self._hostip = None
        self._hostname = None
        self._ss_host = None
        self._ipwss_vip = None
        self._admin = None
        self._password = None
        self._partnerhost = None # Only for DHCP
        self._snapshot = None
        self._RunningProcList = []
        self._problem_proc = None
        pass

    def _initial(self, node) :
        assert node != None

        self._RunningProcList = []
        self._hostip = node.getOamIp()
        self._hostname = node.getHostName()
        self._ss_host, self._ipwss_vip = self._GetSsIP(node)
        self._admin = cfgInstance().getCliUserName()
        self._password = cfgInstance().getCliPassword()
        self._snapshot = self._hostname + "_" + procs.GetRunningProcsFileName()

        if os.path.exists(self._snapshot):
            log._file.info("Snapshot '" + self._snapshot +"' already there, load it!")
            self._RunningProcList = procs.ReadRunningProcs(self._snapshot)
        else:
            '''
            Once the object is initialized, take the snapshot.
            '''
            service_procs = procs.GetService(common.g_upgrade_service)
            self._Snapshot(service_procs)

    def precheck(self) :
        pass


    def execute(self, node = None):
        log._file.debug(">> StopServiceProcessTask Begin")

        # Initial should be done in __init__, due to some reason, do it here
        self._initial(node)

        for proc in self._RunningProcList:
            if proc[procs.status][0] != "running":
                continue

            # 1. Stop process
            '''
            Didn't care about the process status, just stop it!
            '''
            cmd = proc[procs.stop]
            for index in range(2): # at most stop twice
                log._file.debug("==== Try to stop [" + proc[procs.name] + "] ===>")
                self._RemoteExec(self._hostname, cmd)
                result = self._CheckStatus(proc)
                if not result:
                    break

            # 2. Check status
            if result:
                self._problem_proc = proc
                status = "stop failed"
                log._file.error("Stop [" + proc[procs.name] + "] failed")
                raise Exception("Stop [" + proc[procs.name] + "] failed")
            else:
                status = "stopped"
                log._file.info("Stop [" + proc[procs.name] + "] successfully")

            # 3. Record status
            if len(proc[procs.status]) > 1:
                proc[procs.status][1] = status
            else:
                proc[procs.status].append(status)

            # 4. Additional actions, only for DHCP
            if proc[procs.name] == procs.DHCP:
                # 4.1 Get partner PS host
                self._GetPartnerHost()
                # 4.2 Login to partner PS, Switch to 'Partner Down Mode'
                self._PartnerDown()
                # 4.3 Show status of dhcpv4 server
                self._ShowStatus()

        procs.WriteRunningProcs(self._RunningProcList, self._snapshot)

        log._file.debug("<< StopServiceProcessTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        if not self._problem_proc:
            log._print.info("Please refer the exception information!")
        else:
            proc = self._problem_proc
            log._print.info("Please use the following steps to manually fix it on host '%s':" %(self._hostname))
            check = proc[procs.check]
            cmd = procs.GetChecker(check)
            log._print.info("[Check] # %s" %cmd)
            cmd = proc[procs.stop]
            log._print.info("[Stop]  # %s" %cmd)
        pass


    def _GetSsIP(self, node):
        cfg = cfgInstance()
        if common.C_IPW_MODE_SINGLE == common.g_ipw_mode:
            ss_host = self._hostname
            ipwss_vip = self._hostip
        elif common.C_IPW_MODE_MEDIUM1 == common.g_ipw_mode \
        or common.C_IPW_MODE_MEDIUM2 == common.g_ipw_mode:
            ss_host = cfg.getSsCfg(0).getHostName()
            ipwss_vip = cfg.getHaCfg().getSsVip()
        elif common.C_IPW_MODE_ENTRY1 == common.g_ipw_mode \
        or common.C_IPW_MODE_ENTRY2 == common.g_ipw_mode:
            ss_host = cfg.getSsCfg(0).getHostName()
            ipwss_vip = cfg.getSsCfg(0).getOamIp()

        return ss_host, ipwss_vip

    def _GetPartnerHost(self):
        if common.C_IPW_MODE_SINGLE == common.g_ipw_mode:
            log._file.error("Single mode, no partner PS!")
            raise Exception("Single mode, no partner PS!")
        elif common.C_IPW_MODE_ENTRY2 == common.g_ipw_mode:
            ss_ps = self._ss_host
            ps = cfgInstance().getPsCfg(0).getHostName()
            if self._hostname == ss_ps:
                self._partnerhost = ps
            else:
                self._partnerhost = ss_ps
        else :
            for host in cfgInstance().getPsCfgList():
                hostname = host.getHostName()
                if hostname != self._hostname:
                    self._partnerhost = hostname
                    break
        assert self._partnerhost != None

    def _PartnerDown(self):
        cmd = "/opt/ipworks/IPWsm/scripts/ipwdhcpctl ServerType=dhcpv4 Command=partnerdown"
        self._RemoteExec(self._partnerhost, cmd)

    def _ShowStatus(self):
        # Check the dhcpv4server are failover mode or not
        cmd = "list dhcpv4server"
        res = self._ExecuteIPWcli(cmd)
        if re.search("Primary:", res): # failover mode
            log._file.debug("PS servers are running in failover mode!")
            expect = "[\\\"server is \'down\'\\\", \\\"server is \'running partner-down\'\\\"]"
        else:
            log._file.debug("PS servers are running in single mode!")
            expect = "[\\\"server is \'down\'\\\", \\\"server is \'running \'\\\"]"
        cmd = "show status dhcpv4server"
        self._ExecuteIPWcli(cmd, expect)

    def _RemoteExec(self, hostname, command):
        ssh = sshManagerInstance().getSsh(hostname)
        ssh_util = SshUtil(ssh)
        res, _rcode = ssh_util.remote_exec(command, p_err=False, throw=False)
        return res

    def _ExecuteIPWcli(self, cmd, expect=None):
        self._RemoteExec(self._ss_host, "cd " + cfgInstance().getUpgradePath())
        res = self._RemoteExec(self._ss_host, "python ssipwcli.py --ipwss_vip=%s --user=%s --password=%s --command=\"%s\" --expect=\"%s\"" %(self._ipwss_vip, self._admin, self._password, cmd, expect))
        return res


    def _Snapshot(self, proc_name_list):
        log._file.debug("Take snapshot for running services on %s", self._hostname)
        for proc in procs.PROCS:
            if proc[procs.name] not in proc_name_list:
                continue
            check = proc[procs.check]
            cmd = procs.GetChecker(check)
            expect = check[1]
            res = self._RemoteExec(self._hostname, cmd)
            result = re.search(expect, res)
            proc[procs.status] = []
            if result:
                proc[procs.status].append("running")
            else:
                proc[procs.status].append("not running")
                log._file.warning(proc[procs.name] + " is not running!")
            self._RunningProcList.append(proc)
        procs.WriteRunningProcs(self._RunningProcList, self._snapshot)

    def _CheckStatus(self, proc):
        FIB = [1, 2, 3, 5, 8, 13]
        for interval in FIB:
            log._file.debug("Wait for %ss, then check again!" %(5*interval))
            time.sleep(5*interval) # delay in a increasing sequence timer
            check = proc[procs.check]
            cmd = procs.GetChecker(check)
            expect = check[1]
            res = self._RemoteExec(self._hostname, cmd)
            result = re.search(expect, res)
            if not result: # stop successfully
                break
        return result
