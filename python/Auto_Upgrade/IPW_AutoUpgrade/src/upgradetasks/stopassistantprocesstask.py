import os,re,subprocess
import log, common, procs
import time

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class StopAssistantProcessTask(object) :
    """
    Stop Assistant Process
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
        self._problem_proc = None
        self._hostip = node.getOamIp()
        self._hostname = node.getHostName()
        self._snapshot = self._hostname + "_" + "running_assistant_proc.tmp"

        if os.path.exists(self._snapshot):
            log._file.info("Snapshot '" + self._snapshot +"' already there, load it!")
            self._RunningProcList = procs.ReadRunningProcs(self._snapshot)
        else:
            '''
            Once the object is initialized, take the snapshot.
            '''
            self._Snapshot()


    def precheck(self):
        pass
    

    def execute(self, node = None):
        log._file.debug(">> StopAssistantProcessTask Begin")

        self._initial(node)

        for proc in self._RunningProcList:
            if proc[procs.status][0] != "running":
                continue

            # 1. Stop process
            '''
            Didn't care about the process status, just stop it!
            '''
            cmd = proc[procs.stop]
            self._RemoteExec(self._hostname, cmd)
            # 2. Check status
            time.sleep(5) # delays for 5 seconds
            check = proc[procs.check]
            cmd = ' '.join(check)
            expect = check[1]
            res = self._RemoteExec(self._hostname, cmd)
            result = re.search(expect, res)
            status = ""
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

        procs.WriteRunningProcs(self._RunningProcList, self._snapshot)

        log._file.debug("<< StopAssistantProcessTask End")
        
    

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
    
    
    def _RemoteExec(self, hostname, command):
        ssh = sshManagerInstance().getSsh(hostname)
        ssh_util = SshUtil(ssh)
        res, _rcode = ssh_util.remote_exec(command, p_err=False, throw=False)
        return res
    
    
    def _Snapshot(self):
        log._file.debug("Take snapshot for running assistant process on %s", self._hostname)
        for proc in procs.ASSISTANTPROCS:
            check = proc[procs.check]
            cmd = ' '.join(check)
            expect = check[1]
            res = self._RemoteExec(self._hostname, cmd)
            result = re.search(expect, res)
            proc[procs.status] = []
            if result:
                proc[procs.status].append("running")
                log._file.debug(proc["name"] + " is running!")
            else:
                proc[procs.status].append("not running")
            self._RunningProcList.append(proc)
        procs.WriteRunningProcs(self._RunningProcList, self._snapshot)



