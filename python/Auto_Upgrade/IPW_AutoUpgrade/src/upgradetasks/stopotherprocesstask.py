import os,re,subprocess 
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class StopOtherProcessTask(object) :
    """
    Stop Other Process 
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StopOtherProcessTask Begin")
        if self._getRunningProcess(cfg) :
            print "\n        Please check if they are IPWorks related processes."
            print "\n        Do you want to kill these proceses?"
            ret = raw_input('        [Yes (Kill these processes) | No (Ignore these processes) | Quit (Quit auto upgrade)]')
            while(1):
                if not cmp(ret.lower(), 'yes') \
                  or not cmp(ret.lower(), 'y') :
                    print "        Killing processes..."
                    self._killProcess(cfg)
                    while self._getRunningProcess(cfg) :
                        print "\n        Kill again..."
                        self._killProcess(cfg)
                    print "\n        All processes killed..."
                    break
                elif not cmp(ret.lower(), 'no') \
                  or not cmp(ret.lower(), 'n') :
                    print "        Ignore these processes..."
                    break
                elif not cmp(ret.lower(), 'quit') \
                  or not cmp(ret.lower(), 'q') :
                    log._file.debug("Stop the auto upgrade progress manually!")
                    sys.exit(0)
                else :
                    print "        Input error..."
                    ret = raw_input('        [Yes (Kill these processes)|No (Ignore these processes)|Quit (Quit auto upgrade)]')
        else :
            print "        No other process running..."
        print "\n        Stop Other Process [Done]\n"
        log._file.debug("<< StopOtherProcessTask End")
    

    def verify(self):
        pass
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass

    def help(self):
        pass

    def _getRunningProcess(self, host) :
        log._file.debug(">> Check IPWorks related processes on host " + host.getHostName())
        cmd = 'ps -ef | grep -v grep | grep ipw | grep -v ss7 | grep -v ipw_upgrade'
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        res,r_code = ssh_util.remote_exec(cmd, p_err=False, throw=False)
        if res :
            print "\nFollowing processes are still running :"
            print res
            ret = True
        else :
            ret = False
        return ret

    def _killProcess(self, host) :
        log._file.debug(">> Kill IPWorks related processes on host " + host.getHostName())
        cmd = "IPW_PS=`ps -ef | grep -v grep | grep ipw | grep -v ss7 | grep -v ipw_upgrade | awk '{print $2}'`; kill -9 $IPW_PS"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd, p_err=False, throw=False)

