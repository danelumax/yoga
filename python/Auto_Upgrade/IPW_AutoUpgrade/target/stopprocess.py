import os, subprocess, sys
import log
log.Init(True)

class StopProcess:

    def __init__(self) :
        self.assistant_process_dict = {
                                        'snmpd':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],                # SNMP Agent
                                        'ipwdns-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],          # SNMP DNS Subagent
                                        'ipwdhcpv4-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],       # SNMP DHCPv4 Subagent
                                        'ipwenum-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],         # SNMP ENUM Subagent
                                        'ipwem-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],           # SNMP EM Subagent
                                        'ipwcommon-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],       # SNMP Common Subagent
                                        'ipwerh-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],          # SNMP ERH Subagent
                                        'ipwaaa-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],          # SNMP AAA Radius Subagent
                                        'ipwxsnmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],             # SNMP AAA Diameter Subagent
                                        'ipwxboss-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],        # SNMP CLF Subagent
                                        'ipwha-snmp':['/etc/init.d/ipworks.snmpd stop', '/etc/init.d/ipworks.snmpd start', 'false'],           # SNMP Cluster Subagent
                                        'snmptrapd':['/etc/init.d/ipworks.snmptrapd stop', '/etc/init.d/ipworks.snmptrapd start', 'false'],    # SNMP Trap Handler
                                        'ipwcnoss':['/etc/init.d/ipworks.cnoss stop', '/etc/init.d/ipworks.cnoss start', 'false']              # Statistics Collection
                                    }
    

    def execute(self):
        log._file.debug(">> StopProcess Begin")
        for process in self.assistant_process_dict.keys() :
            status = self.getProcessStatus(process)
            if status :
                # Record running processes
                self.recordRunningProcess(process)
                cmd = self.assistant_process_dict[process][0]
                log._cons.debug ("%s" %cmd)
                # Stop processes
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                ret = proc.communicate()
                if (ret[1] != None):
                    log._cons.debug ("%s can't be executed. It will be stopped forcely!" %cmd)
                else:
                    log._file.debug(">> %s was executed successfully!" %cmd)
        log._file.debug(">> Assistant process list is %s!" %self.assistant_process_dict)
        log._file.debug("<< StopSSProcessTask End")
        return 0


    def getProcessStatus(self, process):
        log._file.debug(">> Get process [" + process + "] status")
        cmd = "/bin/ps -e -o \"pid=\" -o \"ppid=\" -o \"comm=\"  | /usr/bin/awk '{if ($NF == \"" + process + "\" && $2 == \"1\") print $1}'"
        ret = True
        pid = os.popen(cmd)
        try :
                id = pid.read().strip()
        finally :
                pid.close()
        if id:
                ret = True
        else:
                ret = False
        log._file.debug(">> Process [" + process + "] status running: " + str(ret))
        return ret


    def recordRunningProcess(self, process):
        self.assistant_process_dict[process][2]="true"
        log._file.debug(">> Process [" + process + "] status recorded...")
        return 0
        
def main() :
    log._cons.debug(">> Stop process remote Call Start")
    task = StopProcess()
    task.execute()
    log._cons.debug(">> Stop process remote Call End")

if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        log._cons.error(e)
        sys.exit(2)
