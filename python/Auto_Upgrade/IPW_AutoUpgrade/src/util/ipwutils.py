import os, re, sys, time
import log, common
import StringIO
import utils

from sshutil import SshUtil
from sshmanager import sshManagerInstance
from cfg import cfgInstance
from hautil import hautilInstance


####################### Storage Server #################################

def stopSS(host):
    log._file.debug(">>> Begin to stop SS on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.ss stop"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "ipwss", "stop"):
        log._file.error("Stop SS failed")
        raise Exception("Stop SS failed")
    log._file.debug("Stop SS Succeed!")

def startSS(host):
    log._file.debug(">>> Begin to start SS on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.ss start"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "ipwss", "start"):
        log._file.error("Start SS Failed")
        raise Exception("Start SS Failed")
    log._file.debug("Start SS Succeed!")


def stopInnodb(host):
    log._file.debug(">>> Begin to stop Innodb on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql stop-master-innodb"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "innodbnode", "stop"):
        log._file.error("Stop Innodb Failed")
        raise Exception("Stop Innodb Failed")
    log._file.debug("Stop Innodb Succeed!")

def startInnodb(host):
    log._file.debug(">>> Begin to start Innodb on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql start-master-innodb"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    res,r_code = ssh_util.remote_exec(cmd)
    log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
    result = re.search("started successful", res)
    if not result:
        log._file.error("Start Innodb Failed")
        raise Exception("Start Innodb Failed")
    log._file.debug("Start Innodb Succeed!")


def stopTomcat(host):
    log._file.debug(">>> Begin to stop Tomcat on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.tomcat stop"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "org.apache.juli", "stop"):
        log._file.error("Stop Tomcat Failed")
        raise Exception("Stop Tomcat Failed")
    log._file.debug("Stop Tomcat Succeed!")

def startTomcat(host):
    log._file.debug(">>> Begin to start Tomcat on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.tomcat start"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    res,r_code = ssh_util.remote_exec(cmd, p_err=False, throw=False)
    log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))
    result1 = re.search("Tomcat started", res)
    result2 = re.search("Tomcat successfully running", res)
    if not result1 and not result2:
        log._file.error("Start Tomcat Failed")
        raise Exception("Start Tomcat Failed")
    log._file.debug("Start Tomcat Succeed!")	


def stopSSResource(host):
    log._file.debug(">>> Begin to stop SS Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().stopIpwssResGrp(ssh)
    hautilInstance().waitIpwssResGrpStop(ssh)
    log._file.debug("<<<")

def startSSResource(host):
    log._file.debug(">>> Begin to start SS Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().startIpwssResGrp(ssh)
    hautilInstance().waitIpwssResGrpStart(ssh)
    log._file.debug("<<<") 


################################ NDB #####################################

def stopNDBCluster(host):
    log._file.debug(">> Stop NDB cluster begin on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql stop-ndbcluster localhost 1186"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "ndbmtd", "stop"):
        log._file.error("Stop DataNode failed")
        raise Exception("Stop DataNode failed")
    log._file.debug("Stop DataNode Succeed!")
    if not utils.check_process(ssh, "ndb_mgmd", "stop"):
        log._file.error("Stop MgmNode failed")
        raise Exception("Stop MgmNode failed")
    log._file.debug("Stop MgmNode Succeed!")


def stopMgmNode(host):
    log._file.debug(">> Stop MgmNode begin on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql stop-mgmd localhost 1186"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "ndb_mgmd", "stop"):
        log._file.error("Stop MgmNode failed")
        raise Exception("Stop MgmNode failed")
    log._file.debug("Stop MgmNode Succeed!")

def startMgmNode(host):
    log._file.debug(">> Start MgmNode begin on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql start-mgmd -f /etc/ipworks/mysql/confs/ipworks_mgm_1.conf"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "ndb_mgmd", "start"):
        log._file.error("Start MgmNode failed")
        raise Exception("Start MgmNode failed")
    log._file.debug("Start MgmNode Succeed!")


def stopMgmResource(host):
    log._file.debug(">>> Begin to stop MGM Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().stopMgmnodeResGrp(ssh)
    hautilInstance().waitMgmnodeResGrpStop(ssh)
    log._file.debug("<<<")

def startMgmResource(host):
    log._file.debug(">>> Begin to start MGM Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().startMgmnodeResGrp(ssh)
    hautilInstance().waitMgmnodeResGrpStart(ssh)
    log._file.debug("<<<")


def stopDataNode(host):
    log._file.debug(">> Stop DataNode begin on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    if not utils.check_process(ssh, "ndbmtd", "stop", 1):
        cmd = "grep ndb-connectstring /etc/ipworks/mysql/confs/ipworks_datanode_my.conf | tail -n 1"
        ssh_util = SshUtil(ssh)
        ret,r_code = ssh_util.remote_exec(cmd)
        ndbconnectstring = ret[ret.find("=")+1:]
        ndbip = ndbconnectstring.split(":")[0]
        log._file.debug("Stopping DataNode: ndbconnectstring is " + ndbconnectstring)
        cmd = "t=`tracepath -n " + ndbip + " | head -1 | /usr/bin/awk '{print $2}'`;l=`/etc/init.d/ipworks.mysql show-ndb-status | grep -n ndb_mgmd | cut -d: -f1`;id=`/etc/init.d/ipworks.mysql show-ndb-status | head -$l | grep $t | cut -f1 | cut -d= -f2`;/etc/init.d/ipworks.mysql stop-ndbd $id " + ndbconnectstring
        ssh_util.remote_exec(cmd)
        if not utils.check_process(ssh, "ndbmtd", "stop"):
            log._file.error("Stop DataNode failed")
            raise Exception("Stop DataNode failed")
        log._file.debug("Stop DataNode Succeed!")
    else:
        log._file.debug("DataNode already stopped!")

def startDataNode(host):
    log._file.debug(">> Start DataNode begin on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql start-ndbd-initial"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "ndbmtd", "start"):
        log._file.error("Start DataNode failed")
        raise Exception("Start DataNode failed")
    log._file.debug("Start DataNode Succeed!")


def isDataNodeInRunning(nodeIP, nodeStatus):
    if not nodeStatus: return False
        
    for line in nodeStatus:
        log._file.debug(line)
        if re.search(nodeIP, line) and not re.search("accepting|starting", line) :
            log._file.debug("datanode of "+nodeIP+ " is in running state.")
            return True
        
    return False

def checkDataNode(host, max_retry=3600):
    log._file.debug(">> Check DataNode begin on host " + host.getHostName())
    cmd = "grep ndb-connectstring /etc/ipworks/mysql/confs/ipworks_datanode_my.conf | tail -n 1"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ret,r_code = ssh_util.remote_exec(cmd)
    log._file.info("Return code: %d, Return info:\n%s" %(r_code, ret))
    
    ndbconnectstring = ret[ret.find("=")+1:]
    ndbMgmNodeIP = ndbconnectstring.split(":")[0]
    log._file.debug("ndbconnectstring is " + ndbconnectstring)
    log._file.debug("ndbMgmNodeIP is " + ndbMgmNodeIP)

    # get ip used by the ndb node in local host
    cmd = "tracepath -n " + ndbMgmNodeIP + " | head -1 | /usr/bin/awk '{print $2}'"
    ret,r_code = ssh_util.remote_exec(cmd)
    ndbDataNodeIP = ret.strip()

    connected = False
    for i in xrange(0, max_retry) :
        #TR HU47463  
        #"ndb_mgm -e show ndb-connectstring" return status of all data nodes.  
        #   ---------------------
        #    [ndbd(NDB)]    2 node(s)
        #    id=27    @10.175.161.164  (mysql-5.5.31 ndb-7.2.13, Nodegroup: 0, *)
        #    id=28    @10.175.161.166  (mysql-5.6.24 ndb-7.4.6, starting, Nodegroup: 0)
        #
        #checkDataNode() returns true only if the data node in the host is in running. 
        #For example, if host is 10.175.161.164, it only check status of data node with id 27.
        #     

        cmd = "/usr/local/mysql/bin/ndb_mgm -e show " + ndbconnectstring
        res,r_code = ssh_util.remote_exec(cmd)
        log._file.info("Return code: %d, Return info:\n%s" %(r_code, res))

        # extract ndb data nodes status string
        isDataNodeStatus=False
        dataNodeStatus=[]        
        buf = StringIO.StringIO(res)
        line = buf.readline()       
        while line :
            if not isDataNodeStatus:
                if re.search("ndbd.*NDB", line) :
                    isDataNodeStatus = True
            else:
                if not line.strip(): break
                dataNodeStatus.append(line)
                
            line = buf.readline()
        
        connected = isDataNodeInRunning(ndbDataNodeIP, dataNodeStatus)
        if not connected :
            time.sleep(2)
        else :
            break
    if not connected :
        raise Exception("the ndbmtd is not correctly started!")
    log._file.debug("<<")

def stopSQLNode(host):
    log._file.debug(">> Stop SQLNode begin on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql stop-sqlnode shutdown --protocol=tcp -h localhost -P 3307"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "sqlnode1", "stop"):
        log._file.error("Stop SQLNode failed")
        raise Exception("Stop SQLNode failed")
    log._file.debug("Stop SQLNode Succeed!")

def startSqlNode(host):
    log._file.debug(">> Start SqlNode begin on host " + host.getHostName())
    cmd = "/etc/init.d/ipworks.mysql start-sqlnode /etc/ipworks/mysql/confs/sqlnode1.conf "
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ssh_util.remote_exec(cmd)
    if not utils.check_process(ssh, "sqlnode1", "start"):
        log._file.error("Start SqlNode failed")
        raise Exception("Start SqlNode failed")
    log._file.debug("Start SqlNode Succeed!")


def stopSQLResource(host):
    log._file.debug(">>> Begin to stop SQL Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().stopSqlnodeResGrp(ssh)
    hautilInstance().waitSqlnodeResGrpStop(ssh)
    log._file.debug("<<<")

def startSQLResource(host):
    log._file.debug(">>> Begin to start SQL Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().startSqlnodeResGrp(ssh)
    hautilInstance().waitSqlnodeResGrpStart(ssh)
    log._file.debug("<<<")


def stopCsvResource(host):
    log._file.debug(">>> Begin to stop CSV Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().stopCsvResGrp(ssh)
    hautilInstance().waitCsvResGrpStop(ssh)
    log._file.debug("<<<")

def startCsvResource(host):
    log._file.debug(">>> Begin to start CSV Resource Group on host " + host.getHostName())
    ssh = sshManagerInstance().getSsh(host.getHostName())
    hautilInstance().startCsvResGrp(ssh)
    hautilInstance().waitCsvResGrpStart(ssh)
    log._file.debug("<<<")


def changeMaster(host):
    log._file.debug(">>> Change Master on " + host.getHostName())
    cmd = "grep master-host /etc/ipworks/mysql/confs/sqlnode_masterinfo.conf"
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    ret, r_code = ssh_util.remote_exec(cmd)
    innodb_ip = ret[ret.find("=")+1:]
    cmd = '/usr/local/mysql/bin/mysql -P 3307 --protocol=tcp -e "stop slave;change master to master_host=\'' + innodb_ip + '\', master_user=\'ipworks\', master_password=\'ipworks\';start slave;"'
    ssh_util.remote_exec(cmd)

def mountDir(host, dir):
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    res, r_code = ssh_util.remote_exec("mount")
    if not re.search("on "+dir+" type nfs", res):
        ssh_util.remote_exec("mount "+dir)
    else:
        log._file.debug("Dir "+dir+" already mounted")

def unmountDir(host, dir):
    ssh = sshManagerInstance().getSsh(host.getHostName())
    ssh_util = SshUtil(ssh)
    res, r_code = ssh_util.remote_exec("mount")
    if re.search("on "+dir+" type nfs", res):
        ssh_util.remote_exec("umount "+dir)
    else:
        log._file.debug("Dir "+dir+" not mounted")

def mountShareDir(host):
    if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
      or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2 with NFS
        if not cmp(common.C_EMC_MODE_NFS, cfgInstance().getHaCfg().getEmcMode()) :
            if not cmp(common.C_IPW_HOSTROLE_SS, host.getHostRole()):
                mountDir(host, "/global/ipworks")
                if common.g_isInstall_AAA:
                    mountDir(host, "/global/sqlnode")
                    mountDir(host, "/global/mgmnode")
                if cfgInstance().getHaCfg().useCsvGrp():
                    mountDir(host, "/global/csvengine")
            else:
                if common.g_isInstall_CLF:
                    mountDir(host, "/global/clf")

def unmountShareDir(host):
    if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
      or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :  # medium1/2 with NFS
        if not cmp(common.C_EMC_MODE_NFS, cfgInstance().getHaCfg().getEmcMode()) :
            if not cmp(common.C_IPW_HOSTROLE_SS, host.getHostRole()):
                unmountDir(host, "/global/ipworks")
                if common.g_isInstall_AAA:
                    unmountDir(host, "/global/sqlnode")
                    unmountDir(host, "/global/mgmnode")
                if cfgInstance().getHaCfg().useCsvGrp():
                    unmountDir(host, "/global/csvengine")
            else:
                if common.g_isInstall_CLF:
                    unmountDir(host, "/global/clf")

def moveClfResource(host):
    ssh = sshManagerInstance().getSsh(host.getHostName())
    if not cmp(host.getHostName(), hautilInstance().clfStartOn(ssh)) :
        hautilInstance().moveClfResGrp(host)
    else:
        log._file.debug("CLF resource is not running on this Node...")

