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


class StartServiceProcessesTask(object) :
    """
    Start Service Process
    """

    def __init__(self) :
        self._hostip = None
        self._hostname = None
        self._ss_host = None
        self._ipwss_vip = None
        self._admin = None
        self._password = None
        self._servername = None
        self._partnerip = None # Only for DHCP
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
        self._servername_dict = node.getPsName()
        self._snapshot = self._hostname + "_" + procs.GetRunningProcsFileName()

        self._RunningProcList = procs.ReadRunningProcs(self._snapshot)
        self._RunningProcList.reverse()

        self._problem_proc = None


    def precheck(self) :
        pass


    def execute(self, node = None):
        log._file.debug(">> StartServiceProcessesTask Begin")

        # Initial should be done in __init__, due to some reason, do it here
        self._initial(node)

        for proc in self._RunningProcList:
            vstatus = proc[procs.status]

            # 1. Check status to avoid multiple start and unexpected running
            check = proc[procs.check]
            cmd = procs.GetChecker(check)
            expect = check[1]
            res = self._RemoteExec(self._hostname, cmd)
            result = re.search(expect, res)
            if result:
                '''
                Already started, perhaps cause by manual exit via last auto upgrade.
                Some ipwcli update will also cause unexpected running, stop it.
                '''
                if not self._ShouldStart(proc):
                    log._file.debug("[" + proc[procs.name] + "] is running unexpected, stopp it!")
                    cmd = proc[procs.stop]
                    self._RemoteExec(self._hostname, cmd)
                    continue

                if vstatus[0] != "running": # "vstatus": ["not running", "---", "running"]
                    self._UpdateStatus(vstatus, 1, "---")
                log._file.debug("[" + proc[procs.name] + "] has already started, just change the status to running!")
                self._UpdateStatus(vstatus, 2, "running")
            else:
                if not self._ShouldStart(proc):
                    continue
                if vstatus[0] != "running":
                    self._UpdateStatus(vstatus, 1, "---")
                # 2. Start process
                vstart = proc[procs.start]
                if type(vstart) is list:
                    cmd = vstart[1]
                    # append the server name
                    cmd = cmd + " " + self._GetServerName(proc)
                    self._ExecuteIPWcli(cmd)
                else:
                    cmd = vstart
                    log._file.debug("Running %s", cmd)
                    self._RemoteExec(self._hostname, cmd)

                # 3. Check status
                result = self._CheckStatus(proc)
                if not result:
                    self._problem_proc = proc
                    status = "start failed"
                    log._file.error("Start [" + proc[procs.name] + "] failed")
                    raise Exception("Start [" + proc[procs.name] + "] failed")
                else:
                    status = "running"
                    log._file.info("Start [" + proc[procs.name] + "] successfully")

                self._UpdateStatus(vstatus, 2, status)

                # 4. Additional actions, only for DHCP
                if proc[procs.name] == procs.DHCP:
                    # Show status of dhcpv4 server
                    self._ShowStatus()

        self._RunningProcList.reverse()
        procs.WriteRunningProcs(self._RunningProcList, self._snapshot)

        log._file.debug("<< StartServiceProcessesTask End on " + self._hostname)


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        procfd = open(self._snapshot, 'r')
        content = procfd.read()
        procfd.close()
        log._file.debug("Content of " + self._snapshot + ":\n" + content)

        log._file.debug("Remove the snapshot file, which record the running services processes")
        os.remove(self._snapshot)
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
            vstart = proc[procs.start]
            if type(vstart) is list:
                cmd = vstart[1]
                # append the server name
                cmd = cmd + " " + self._GetServerName(proc)
                log._print.info("[Start] Login active SS server:")
                log._print.info("[Start] # ipwcli")
                log._print.info("[Start] IPWorks> %s" %cmd)
            else:
                cmd = vstart
                log._print.info("[Start] # %s" %cmd)
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

    def _ShowStatus(self):
        # Check the dhcpv4server are failover mode or not
        cmd = "list dhcpv4server"
        res = self._ExecuteIPWcli(cmd)
        if re.search("Primary:", res): # failover mode
            log._file.debug("PS servers are running in failover mode!")
            expect = "[[\\\"server is \'running normal\'\\\", 2]]"
        else:
            log._file.debug("PS servers are running in single mode!")
            expect = "[[\\\"server is \'running \'\\\", 2]]"
        cmd = "show status dhcpv4server"
        expect = "[[\\\"server is \'running normal\'\\\", 2]]"
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

    def _ShouldStart(self, proc):
        vstatus = proc[procs.status]
        proc_name = proc[procs.name]
        # 1. Must start, since it's running at the beginning.
        if vstatus[0] == "running":
            return True
        # 2. Shouldn't start, because not running before, and it's not Server Manager.
        elif not procs.IsServerManager(proc_name):
            return False
        # 3. If one of the SM controled service is running at the beginning, start it. Otherwise, keep it stopped.
        else:
            proc_name_list = procs.SMProcsMap(proc_name)
            for proc_item in self._RunningProcList:
                if proc_item[procs.name] in proc_name_list and proc_item[procs.status][0] == "running":
                    log._file.debug("Proc [%s] should be started, since running service [%s] required it!" %(proc_name, proc_item[procs.name]))
                    return True
            return False

    def _UpdateStatus(self, vstatus, index, value):
        if len(vstatus) > index:
            vstatus[index] = value
        else:
            vstatus.append(value)


    def _GetServerName(self, proc):
        vstart = proc[procs.start]
        assert type(vstart) is list

        start_cmd = vstart[1]
        server_type = start_cmd.split()[1]
        return self._servername_dict[server_type]

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
            if result: # start successfully
                if procs.IsServerManager(proc[procs.name]):
                    log._file.debug("Wait for 5s, let the server manager connected to SS")
                    time.sleep(5)
                break
        return result
