import os, re, sys, time
import log, common
from sshutil import SshUtil
from sshmanager import sshManagerInstance
from cfg import cfgInstance



def hautilInstance() :
    try :
        inst = HaUtil()
    except HaUtil as e:
        inst = e
    return inst


class HaUtil :

    __instance = None

    def __init__(self) :
        if HaUtil.__instance :
            raise HaUtil.__instance
    
        self.ss_double_res = ['res-ipwss-vip', 'res-ipwss-mysql', 'res-ipwss-ss', 'res-ipwss-tomcat']
        self.ss_single_res = ['res-ipwss-vip', 'res-ipwss-fs', 'res-ipwss-mysql', 'res-ipwss-ss', 'res-ipwss-tomcat']

        self.mgm_double_res = ["res-mgmd-vip", 'res-mgmd']
        self.mgm_single_res = ["res-mgmd-vip", "res-mgmd-fs", 'res-mgmd'] 

        self.sql_double_res = ["res-sql-vip", 'res-sqlnode'] 
        self.sql_single_res = ["res-sql-vip", "res-sql-fs", 'res-sqlnode']

        self.csv_double_res = ["res-csvengine-vip", 'res-csvengine']
        self.csv_single_res = ["res-csvengine-vip", "res-csvengine-fs", 'res-csvengine']

        self.clf_double_res = ["resource-clf-cmi-nacf-pmi-racf4-umi-vip", "resource-clf-sbccops-sbce2-vip", "resource-pmal-cmipmi-soap-vip", "resource-pmal", 'resource-clf']
        self.clf_single_res = ["resource-clf-cmi-nacf-pmi-racf4-umi-vip", "resource-clf-sbccops-sbce2-vip", "resource-pmal-cmipmi-soap-vip", "resource-clf-fs", "resource-pmal", 'resource-clf']


    def checkClusterStatus(self, ssh_conn, hostname_list) :
        log._file.debug(">> Check Cluster Status: " + str(hostname_list))
        ssh_util = SshUtil(ssh_conn)
        res, code = ssh_util.remote_exec("crm_mon -1 -n |grep Node")
        status = {}
        lines = res.split('\n')
        for host in hostname_list :
            status[host] = "offline"
            for line in lines :
                if re.search("^Node ", line) :
                    x = line.split()
                    if not cmp(host+":", x[1]) and not cmp("online", x[2]) :
                        status[host] = "online"
        for host in hostname_list :
            if cmp("online", status[host]) :
                return False
        return True
        #res, code = ssh_util.remote_exec("crm_mon -1 |grep online")
        #if re.search(hostname_list[0], res) and re.search(hostname[1], res) :
        #    return True
        #return False


    def cleanupResources(self, ssh_conn, resource_list) :
        log._file.debug(">> Cleanup Resources: " + str(resource_list)) 
        ssh_util = SshUtil(ssh_conn)
        for resource in resource_list :
            command = "crm_resource --resource " + resource + " --cleanup -f"
            res, r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
        log._file.debug("<<")


    def cleanupResource(self, ssh_util, resource) :
        log._file.debug(">> Cleanup Resource: " + str(resource)) 
        command = "crm_resource --resource " + resource + " --cleanup -f"
        res, r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
        log._file.debug("<<") 


    def cleanupError(self, ssh_util, err) :
        log._file.debug(">> Cleanup error = " + str(err)) 
        command = "T=0; while [ $T -eq 0 ]; do cibadmin -Q |grep " + err + " |head -1 |cibadmin -D -p; T=$?; done;"
        res, r_code = ssh_util.remote_exec(command, p_err=False, throw=False)
        log._file.debug("<<") 


    #return True if all resources status == Started
    def getHaResourceStatus(self, ssh_conn, resource_list) :
        log._file.debug(">> Check HA Resource status")    
        ssh_util = SshUtil(ssh_conn)
        ret = True    
        resources = {}
        for resource in resource_list :
            resources[resource] = ""
        command = "crm_mon -n -f -1"
        res, r_code = ssh_util.remote_exec(command)
        lines = res.splitlines()
        for line in lines :
            if re.search('fail-count=', line) :
                log._file.debug("line: " + line)
                resource_name = line.strip().split(":")[0]
                self.cleanupResource(ssh_util, resource_name)
                ret = False
                break
            elif re.search(', rc=', line) :
                log._file.debug("line: " + line)
                resource_name = line.strip().split()[0]
                self.cleanupError(ssh_util, resource_name)
                ret = False
                break
            else :
                for key in resource_list :
                    if re.search("(\s+)%s(\s+)"%key, line) :
                        toks = line.strip().split()
                        if len(toks) == 3:
                            resources[key] = toks[2]
                            log._file.debug("Find resource:%s, status:%s" %(key, toks[2]))
                            break
        if ret :
            for key in resources :
                if resources[key] != "Started" :
                    ret = False
                    break
        log._file.debug("<< HA Resource status all started ready: " + str(ret))    
        return ret
  

    def waitHaResourceStart(self, ssh_conn, resource_list, times=100) :
        log._file.debug(">> Wait for Resource Start: " + str(resource_list))
        retry = 0    
        while retry < times :
            time.sleep(10)    
            if self.getHaResourceStatus(ssh_conn, resource_list) :
                break
            retry += 1
        if retry == times :
            raise Exception("HA resource %s can't successfully started" %(str(resource_list)))
        log._file.debug("<<")    


    def getHaResourceStopStatus(self, ssh_conn, resource_list) :
        log._file.debug(">> Check HA Resource stop status")
        ssh_util = SshUtil(ssh_conn)
        ret = True
        resources = []
        command = "crm_mon -n -f -1"
        res, r_code = ssh_util.remote_exec(command)
        lines = res.splitlines()
        for line in lines:
            if re.search('fail-count=', line):
                resource_name = line.strip().split(":")[0]
                self.cleanupResource(ssh_util, resource_name)
                ret = False
                break
            elif re.search(', rc=', line):
                resource_name = line.strip().split()[0]
                self.cleanupError(ssh_util, resource_name)
                ret = False
                break
            for elem in resource_list:
                if re.search(elem, line):
                    resources.append(elem)
        if ret and resources:
            log._file.debug("resources still started: %s" %(resources))
            ret = False
        log._file.debug("<< HA Resource status all stopped ready: " + str(ret))
        return ret


    def waitHaResourceStop(self, ssh_conn, resource_list, times=100):
        log._file.debug(">> Wait for Resource Stop: " + str(resource_list))
        retry = 0
        while retry < times :
            time.sleep(10) 
            if self.getHaResourceStopStatus(ssh_conn, resource_list) :
                break
            retry += 1
        if retry == times :
            raise Exception("HA resource %s can't successfully stopped" %(str(resource_list)))
        log._file.debug("<<")


    def ssStartOn(self, ssh_conn):
        log._file.debug(">> Check Storage Server start on which node")
        ssh_util = SshUtil(ssh_conn)
        command = "crm_mon -1"
        hostname = ""
        res, r_code = ssh_util.remote_exec(command)
        lines = res.splitlines()
        for line in lines:
            if re.search('res-ipwss-ss', line):
                hostname = line.strip().split()[-1]
                break
        log._file.debug("group-ipwss started on " + hostname)
        log._file.debug("<<")
        return hostname


    def sqlStartOn(self, ssh_conn):
        log._file.debug(">> Check Sqlnode start on which node")
        ssh_util = SshUtil(ssh_conn)
        command = "crm_mon -1"
        hostname = ""
        res, r_code = ssh_util.remote_exec(command)
        lines = res.splitlines()
        for line in lines:
            if re.search('res-sqlnode', line):
                hostname = line.strip().split()[-1]
                break
        log._file.debug("group-sqlnode started on " + hostname)
        log._file.debug("<<")
        return hostname


    def clfStartOn(self, ssh_conn):
        log._file.debug(">> Check CLF start on which node")
        ssh_util = SshUtil(ssh_conn)
        command = "crm_mon -1"
        hostname = ""
        res, r_code = ssh_util.remote_exec(command)
        lines = res.splitlines()
        for line in lines:
            if re.search('resource-clf', line):
                hostname = line.strip().split()[-1]
                break
        log._file.debug("group-clf started on " + hostname)
        log._file.debug("<<")
        return hostname


#######################################################################

    def startHaResGrp(self, ssh_conn, res_grp):
        log._file.debug(">> Start Resource Group: " + res_grp)
        ssh_util = SshUtil(ssh_conn)
        command = "crm_resource --resource " + res_grp + " -p target-role -m -v Started"
        ssh_util.remote_exec(command)
        log._file.debug("<<")


    def stopHaResGrp(self, ssh_conn, res_grp):
        log._file.debug(">> Stop Resource Group: " + res_grp)
        ssh_util = SshUtil(ssh_conn)
        command = "crm_resource --resource " + res_grp + " -p target-role -m -v Stopped"
        ssh_util.remote_exec(command, throw=False)
        log._file.debug("<<")


######################################################################
    def startSbdResGrp(self, ssh_conn):
        self.startHaResGrp(ssh_conn, "stonith_sbd")
        

    def stopSbdResGrp(self, ssh_conn):
        self.stopHaResGrp(ssh_conn, "stonith_sbd")
        

    def waitSbdResGrpStart(self, ssh_conn):
        self.waitHaResourceStart(ssh_conn, ["stonith_sbd"])
        

    def waitSbdResGrpStop(self, ssh_conn):
        self.waitHaResourceStop(ssh_conn, ["stonith_sbd"])
        



######################################################################
    def startIpwssResGrp(self, ssh_conn):
        self.startHaResGrp(ssh_conn, "group-ipwss")
        

    def stopIpwssResGrp(self, ssh_conn):
        self.stopHaResGrp(ssh_conn, "group-ipwss")
        

    def waitIpwssResGrpStart(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.ss_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.ss_double_res
            else:
                tmp_res = self.ss_single_res

        self.waitHaResourceStart(ssh_conn,tmp_res)
        

    def waitIpwssResGrpStop(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.ss_double_res
        else :
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.ss_double_res
            else:
                tmp_res = self.ss_single_res
            
        self.waitHaResourceStop(ssh_conn,tmp_res)
        



######################################################################
    def startMgmnodeResGrp(self, ssh_conn):
        self.startHaResGrp(ssh_conn, "group-mgmnode")
        

    def stopMgmnodeResGrp(self, ssh_conn):
        self.stopHaResGrp(ssh_conn, "group-mgmnode")
        

    def waitMgmnodeResGrpStart(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.mgm_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.mgm_double_res
            else:
                tmp_res = self.mgm_single_res

        self.waitHaResourceStart(ssh_conn,tmp_res)
        

    def waitMgmnodeResGrpStop(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.mgm_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.mgm_double_res
            else:
                tmp_res = self.mgm_single_res

        self.waitHaResourceStop(ssh_conn,tmp_res)

######################################################################
    def startSqlnodeResGrp(self, ssh_conn):
        self.startHaResGrp(ssh_conn, "group-sqlnode")
        

    def stopSqlnodeResGrp(self, ssh_conn):
        self.stopHaResGrp(ssh_conn, "group-sqlnode")
        

    def waitSqlnodeResGrpStart(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.sql_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.sql_double_res
            else:
                tmp_res = self.sql_single_res

        self.waitHaResourceStart(ssh_conn,tmp_res)
        

    def waitSqlnodeResGrpStop(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.sql_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.sql_double_res
            else:
                tmp_res = self.sql_single_res

        self.waitHaResourceStop(ssh_conn,tmp_res)



######################################################################
    def startCsvResGrp(self, ssh_conn):
        self.startHaResGrp(ssh_conn, "group-csvengine")


    def stopCsvResGrp(self, ssh_conn):
        self.stopHaResGrp(ssh_conn, "group-csvengine")


    def waitCsvResGrpStart(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.csv_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.csv_double_res
            else:
                tmp_res = self.csv_single_res

        self.waitHaResourceStart(ssh_conn,tmp_res)


    def waitCsvResGrpStop(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.csv_double_res
        else:
             if common.C_EMC_MOUNT_MODE_DOUBLE:
                 tmp_res = self.csv_double_res
             else:
                 tmp_res = self.csv_single_res

        self.waitHaResourceStop(ssh_conn, tmp_res)
        

######################################################################
    def startClfResGrp(self, ssh_conn):
        self.startHaResGrp(ssh_conn, "group-clf")


    def stopClfResGrp(self, ssh_conn):
        self.stopHaResGrp(ssh_conn, "group-clf")


    def waitClfResGrpStart(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.clf_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.clf_double_res
            else:
                tmp_res = self.clf_single_res

        self.waitHaResourceStart(ssh_conn,tmp_res)


    def waitClfResGrpStop(self, ssh_conn):
        tmp_res = []
        if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
            tmp_res = self.clf_double_res
        else:
            if common.C_EMC_MOUNT_MODE_DOUBLE:
                tmp_res = self.clf_double_res
            else:
                tmp_res = self.clf_single_res
         
        self.waitHaResourceStop(ssh_conn,tmp_res)

    def waitClfResGrp(self, ssh_conn, hostname, times=100):
        log._file.debug(">> Wait for CLF Resource move to " + hostname)
        retry = 0
        while retry < times :
            time.sleep(10)
            if not cmp(hostname, self.clfStartOn(ssh_conn)) :
                break
            retry += 1
        if retry == times :
            raise Exception("CLF resource can't successfully move to " + hostname)
        log._file.debug("<<")

    def moveClfResGrp(self, host):
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        cmd = "crm_mon -1 -n | grep online | grep -v " + host.getHostName()
        ret,r_code = ssh_util.remote_exec(cmd)
        hostname = ret.split(":")[0].split()[1]
        cmd = "crm_resource -r group-clf -M -N " + hostname
        ssh_util.remote_exec(cmd)
        self.waitClfResGrp(ssh, hostname)

