#!/usr/bin/env python

import os, re, subprocess, time
import util


class Ndb :

    def __init__(self, logger) :
        self._logger = logger
        mysql_bin_path = "/usr/local/mysql/bin/"
        self._mysql = "/usr/local/mysql/bin/mysql"
        self._mgm_conf_file = '/etc/ipworks/mysql/confs/ipworks_mgm_1.conf'
        self._data_conf_file = '/etc/ipworks/mysql/confs/ipworks_datanode_my.conf'
        self._sql_conf_file = '/etc/ipworks/mysql/confs/sqlnode1.conf'
        self._master_info_file = '/etc/ipworks/mysql/confs/sqlnode_masterinfo.conf'


    def addMip(self, hostname, ip) :
        self._logger.debug(">> hostname = " + str(hostname) + ', ip = ' + str(ip))
        file_name = '/etc/hosts'
        lines = util.readfilelines(file_name)
        context = ''
        for line in lines :
            if not re.search('\s' + hostname + '\s', line) :
                context = context + line
        context = context + ip + ' ' + hostname + '\n'
        util.writefile(file_name, context)
        self._logger.debug("<<")


    # """ grant innodb privilege """
    def grant_innodb_privilege(self, ip) :
        self._logger.debug(">>")
        proc = subprocess.Popen([self._mysql, "-h", ss_vip , "-e", "grant all privileges on *.* to \'ipworks\'@\'" + ip + "\' identified by \'ipworks\';"])
        proc.wait()
        self._logger.debug("<<")



    # """ grant sqlnode privilege """
    def grant_sqlnode_privilege(self) :
        self._logger.debug(">>")
        proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "grant all privileges on *.* to \'\'@\'127.0.0.1\' identified by \'\';"])
        proc.wait()
        proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "flush privileges;"])
        proc.wait()
        self._logger.debug("<<")


##############################################################################################

    def cleanDataNode(self) :
        self._logger.debug(">> clean Data Node")
        auto_install_tag = '####################AUTO_INSTALL################' 
        lines = util.readfilelines(self._mgm_conf_file)
        context = ''
        for line in lines :
            if re.search(auto_install_tag, line) : 
                break
            context = context + line
        # ignore the lines after the auto_install_tag
        context = context + '\n' + auto_install_tag + '\n'
        util.writefile(self._mgm_conf_file, context)
        self._logger.debug("<<")



    def addDataNode(self, datanode_id, datanode_ip) :
        self._logger.debug(">> add datanode_ip = " + datanode_ip + ", id = " + str(datanode_id))
        fd = open(self._mgm_conf_file, 'a') 
        context = "\n[NDBD]\nHostName=" + datanode_ip + "\nId=" + str(datanode_id) + "\nDataDir=/var/lib/mysql-cluster/datanode\n\n"
        fd.write(context)
        fd.close()
        self._logger.debug("<<")


    # """ config mgmnode """
    def configMgmd(self, mgm_mip, data_size, index_size, replicas_no) :
        self._logger.debug(">> config mgmnode")
        lines = util.readfilelines(self._mgm_conf_file)
        context = ''
        for line in lines :
            # find the first line of HostName=
            if re.search('^HostName=', line) : 
                #index = line.find("HostName=")
                #context += line[0:index] + 'HostName=' + mgm_mip + '\n'
                context += 'HostName=' + mgm_mip + '\n'
            elif re.search('^NoOfReplicas=', line) :
                #index = line.find("NoOfReplicas=")
                #context += line[0:index] + 'NoOfReplicas=' + replicas_no + '\n'
                context += 'NoOfReplicas=' + replicas_no + '\n'
            elif re.search('^DataMemory=', line):
                #index = line.find("DataMemory=")
                #context += line[0:index] + 'DataMemory=' + data_size + 'M\n'
                context += 'DataMemory=' + data_size + 'M\n'
            elif re.search('^IndexMemory=', line):
                #index = line.find("IndexMemory=")
                #context += line[0:index] + 'IndexMemory=' + index_size + 'M\n'
                context += 'IndexMemory=' + index_size + 'M\n'
            else :
                context = context + line
        util.writefile(self._mgm_conf_file, context)
        self._logger.debug("<<")


    # """ config datanode """
    def configDataNode(self, mgm_ip):
        self._logger.debug(">> config datanode")
        lines = util.readfilelines(self._data_conf_file)
        isFind = False
        context = ''
        for line in lines :
            if isFind:
                if re.search('^ndb-connectstring=', line):
                    #index = line.find("ndb-connectstring=")
                    #context += line[0:index] + 'ndb-connectstring=' + mgm_ip + ':1186\n'
                    context += 'ndb-connectstring=' + mgm_ip + ':1186\n'
                    isFind = False
                else :
                    contest += line
            else:
                if re.search('^\[MYSQL_CLUSTER\]', line):
                    isFind = True
                context = context + line
        util.writefile(self._data_conf_file, context)
        self._logger.debug("<<")


    # """ config sqlnode """
    def configSqlNode(self, ss_vip, mgm_mip, server_id) :
        self._logger.debug(">> config sqlnode")
        lines = util.readfilelines(self._sql_conf_file)
        context = ''
        for line in lines :
            if re.search('^ndb-connectstring=', line) :
                #index = line.find("ndb-connectstring=")
                #context += line[0:index] + 'ndb-connectstring=' + mgm_mip + ':1186\n'
                context += 'ndb-connectstring=' + mgm_mip + ':1186\n'
            elif re.search('master-host=', line) : 
                index = line.find("master-host=")
                context += line[0:index] + 'master-host=' + ss_vip + '\n'
                #context += 'master-host=' + ss_vip + '\n'
            elif re.search('^server-id=', line) :
                #index = line.find("server-id=")
                #context += line[0:index] + 'server-id=' + server_id + '\n'
                context += 'server-id=' + server_id + '\n'
            else :
                context = context + line
        util.writefile(self._sql_conf_file, context)
        self._logger.debug("<<")


    def configMasterInfo(self, ss_vip) :
        self._logger.debug(">> config sqlnode in masterinfo")
        context = ''
        if os.path.exists(self._master_info_file) :
            lines = util.readfilelines(self._master_info_file)
            for line in lines :
                if re.search('master-host=', line) :
                    self._logger.debug("find master-host in sqlnode_masterinfo.conf: " + line)
                    index = line.find("master-host=")
                    context += line[0:index] + 'master-host=' + ss_vip + '\n'
                else :
                    context = context + line
        util.writefile(self._master_info_file, context)
        self._logger.debug("<<")


##############################################################################################

    # """ start mgmd """
    def startMgmd(self) :
        self._logger.debug(">> start mgmd")
        #proc = subprocess.Popen(["/etc/init.d/ipworks.mysql", "start-mgmd", "-f", "/etc/ipworks/mysql/confs/ipworks_mgm_1.conf"])
        self._logger.debug("command: \n%s start-mgmd -f %s" %(self._mysql, self._mgm_conf_file))
        proc = subprocess.Popen(["/etc/init.d/ipworks.mysql", "start-mgmd", "-f", self._mgm_conf_file])
        proc.wait()
        if not util.check_process("/usr/local/mysql/sbin/ndb_mgmd", "start") :
            raise Exception("can't find the process /usr/local/mysql/sbin/ndb_mgmd..... The ndb_mgmd is not started")
        self._logger.debug("<<")


    # """ start ndbmtd """
    def startDataNode(self) :
        self._logger.debug(">> start datanode")
        self._logger.debug("command: \n%s start-ndbd-initial" %self._mysql)
        proc = subprocess.Popen(["/etc/init.d/ipworks.mysql", "start-ndbd-initial"])
        proc.wait()
        if not util.check_process("/usr/local/mysql/sbin/ndbmtd", "start") :
            raise Exception("can't find the process /usr/local/mysql/sbin/ndbmtd..... The ndbmtd is not started")
        self._logger.debug("<<")


    # """ check ndbmtd """
    def checkDataNode(self) :
        self._logger.debug(">> check datanode status")
        connected = False
        for i in range(1, 60) :
            print "start to check the ndb status. i = " + str(i)
            proc = subprocess.Popen(["/usr/local/mysql/bin/ndb_mgm", "-e", "show"], stdout=subprocess.PIPE)
            proc.wait()
            #self._logger.debug("Mysql cluster info:\n%s" %proc.stdout.readlines())
            line = proc.stdout.readline()
            while line :
                self._logger.debug(line)
                if re.search("ndbd.*NDB", line) :
                    line = proc.stdout.readline()
                    print "i = " + str(i) + ", " + line
                    if not re.search("accepting|starting", line) :
                        connected = True
                        self._logger.debug("datanode has running")
                        break
                line = proc.stdout.readline()
            if not connected :
                time.sleep(2)
            else :
                break
        if not connected :
            raise Exception("the ndbmtd is not correctly started!")
        self._logger.debug("<<")




    # """ start sqlnode """
    def startSqlNode(self, master_ip) :
        self._logger.debug(">> start sqlnode")
        self._logger.debug("command: \n%s start-sqlnode %s" %(self._mysql, self._sql_conf_file))
        proc = subprocess.Popen(["/etc/init.d/ipworks.mysql", "start-sqlnode", "/etc/ipworks/mysql/confs/sqlnode1.conf"])
        proc.wait()
        #proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "stop slave;"])
        #proc.wait()
        #proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "change master to master_host='" + master_ip + "';"])
        #proc.wait()
        #proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "drop database if exists ipworks;"])
        #proc.wait()
        #proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "create database ipworks;"])
        #proc.wait()
        #proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "reset slave;"])
        #proc.wait()
        #proc = subprocess.Popen([self._mysql, "-P", "3307", "--protocol=tcp", "-e", "start slave;"])
        #proc.wait()
        time.sleep(10)
        self._logger.debug("<<")

                







