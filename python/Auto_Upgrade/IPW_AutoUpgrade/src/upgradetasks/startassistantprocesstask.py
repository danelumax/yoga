import os,re,subprocess 
import log, common, procs

import time

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class StartAssistantProcessTask(object) :
    """
    Start Assistant Process
    """

    def __init__(self) :
        self._hostip = None
        self._hostname = None
        self._snapshot = None
        self._RunningProcList = []
        self._problem_proc = None
        pass
    

    def _initial(self, node) :
        assert node != None

        self._RunningProcList = []
        self._hostip = node.getOamIp()
        self._hostname = node.getHostName()
        self._snapshot = self._hostname + "_" + "running_assistant_proc.tmp"

        self._RunningProcList = procs.ReadRunningProcs(self._snapshot)
        self._RunningProcList.reverse()

        self._problem_proc = None
    

    def precheck(self) :
        pass


    def execute(self, node = None):
        log._file.debug(">> StartAssistantProcessTask Begin")
        
        # Initial should be done in __init__, due to some reason, do it here
        self._initial(node)

        for proc in self._RunningProcList:
            vstatus = proc[procs.status]

            # 1. Check status to avoid multiple start and unexpected running
            check = proc[procs.check]
            cmd = ' '.join(check)
            expect = check[1]
            res = self._RemoteExec(self._hostname, cmd)
            result = re.search(expect, res)
            if result:
                '''
                Already started, perhaps cause by manual exit via last auto upgrade.
                Some ipwcli update will also cause unexpected running, stop it.
                '''
                if vstatus[0] != "running":
                    log._file.debug("[" + proc[procs.name] + "] is running unexpected, stopp it!")
                    cmd = proc[procs.stop]
                    self._RemoteExec(self._hostname, cmd)
                    continue
                log._file.debug("[" + proc[procs.name] + "] has already started, just change the status to running!")
                self._UpdateStatus(vstatus, 2, "running")
            else:
                if vstatus[0] != "running":
                    continue
                # 2. Start process
                cmd = proc[procs.start]
                log._file.debug("Running %s", cmd)
                self._RemoteExec(self._hostname, cmd)

                # 3. Check status
                time.sleep(5) # delays for 5 seconds
                check = proc[procs.check]
                cmd = ' '.join(check)
                expect = check[1]
                res = self._RemoteExec(self._hostname, cmd)
                result = re.search(expect, res)
                if not result:
                    self._problem_proc = proc
                    status = "start failed"
                    log._file.error("Start [" + proc[procs.name] + "] failed")
                    raise Exception("Start [" + proc[procs.name] + "] failed")
                else:
                    status = "running"
                    log._file.info("Start [" + proc[procs.name] + "] successfully")

                self._UpdateStatus(vstatus, 2, status)

        self._RunningProcList.reverse()
        procs.WriteRunningProcs(self._RunningProcList, self._snapshot)

        log._file.debug("<< StartAssistantProcessesTask End on " + self._hostname)
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
	procfd = open(self._snapshot, 'r')
        content = procfd.read()
        procfd.close()
        log._file.debug("Content of " + self._snapshot + ":\n" + content)

        log._file.debug("Remove the temporary file, which record the running services processes")
        os.remove(self._snapshot)
        pass

    def help(self):
        if not self._problem_proc:
            log._print.info("Please refer the exception information!")
        else:
            log._print.info("Please use the following steps to manually fix it on host '%s':" %(self._hostname))
            check = proc[procs.check]
            cmd = procs.GetChecker(check)
            log._print.info("[Check] # %s" %cmd)
            vstart = proc[procs.start]
            cmd = vstart
            log._print.info("[Start] # %s" %cmd)
        pass
    
    def _RemoteExec(self, hostname, command):
        ssh = sshManagerInstance().getSsh(hostname)
        ssh_util = SshUtil(ssh)
        res, _rcode = ssh_util.remote_exec(command, p_err=False, throw=False)
        return res
	
    def _UpdateStatus(self, vstatus, index, value):
        if len(vstatus) > index:
            vstatus[index] = value
        else:
            vstatus.append(value)


